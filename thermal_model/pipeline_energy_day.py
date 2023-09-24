import math
import numpy as np
import thermal_model.theoretical as m


def get_pipe_energy(
    day,
    local_latitude,
    inclination,
    azimuth,
    longitud_local,
    granularity,
    local_height,
    internal_diameter,
    external_diameter,
    pipeline_separation,
    pipeline_length
):

  # CALCULOS PUNTUALES INSTANTÁNEOS
  # ===============================
  gon = m.extraterrestrial_radiation(day)
  ang_delta = m.declination_angle(day)
  ang_omega_s = m.sunset_hour_angle(local_latitude, ang_delta)
  hora_aparec_sol = m.sunrise(ang_omega_s)
  hora_puesta_sol = m.sunset(ang_omega_s)

  # CALCULOS ANGULARES HORARIOS (manteniendo desde "hora_aparec_sol" hasta "hora_puesta_sol")
  # ==========================
  hora_sol = np.zeros(granularity)
  hora_std = np.zeros(granularity)
  ang_omega = np.zeros(granularity)
  ang_theta = np.zeros(granularity)
  ang_theta_z = np.zeros(granularity)

  for i in range(granularity):
    hora_sol[i] = hora_aparec_sol + \
        (hora_puesta_sol - hora_aparec_sol) / granularity * (i)
    hora_std[i] = m.standard_time(day, hora_sol[i], longitud_local)
    ang_omega[i] = m.hour_angle(hora_sol[i])
    ang_theta[i] = m.incidence_angle(
        ang_delta, local_latitude, inclination, azimuth, ang_omega[i])
    ang_theta_z[i] = m.zenith_angle(
        ang_delta, local_latitude, azimuth, ang_omega[i])

  # CALCULO DE LA RADIACION HORARIA EXTRATERRESTRE HORIZONTAL (en el n dia) [W/m2]
  # ========================================================
  go_m = np.zeros(granularity)

  for i in range(granularity):
    go_m[i] = m.extraterrestrial_horizontal_radiation(gon, ang_theta[i])

  # ESTIMACION DE LA RADIACION HORARIA DE HAZ Y DIFUSA EN CIELO DESPEJADO EN DIRECCION DEL SOL G_BEAM_n(Duffie, 2023)
  # ==============================================================================
  tau_beam = np.zeros(granularity)
  g_beam_n = np.zeros(granularity)
  tau_dif = np.zeros(granularity)
  g_oo = np.zeros(granularity)
  g_difus = np.zeros(granularity)

  for i in range(granularity):
    tau_beam[i] = m.sky_transmissivity(ang_theta_z[i], local_height)
    g_beam_n[i] = m.beam_radiation(gon, tau_beam[i])
    tau_dif[i] = m.diffuse_transmissivity(tau_beam[i])
    g_oo[i] = m.extraterrestrial_horizontal_radiation(gon, ang_theta_z[i])
    g_difus[i] = m.diffuse_radiation_horizontal(g_oo[i], tau_dif[i])

  f_forma = m.diffuse_radiation_shape_function(
      internal_diameter, external_diameter, pipeline_separation)

  # CALCULO DE LAS POTENCIAS HORARIAS QUE INCIDEN SOBRE UN TUBO AL VACIO [W] (Tang, 2009)
  # =========================================================================
  nx = np.zeros(granularity)
  ny = np.zeros(granularity)
  nz = np.zeros(granularity)
  nnx = np.zeros(granularity)
  nny = np.zeros(granularity)
  nnz = np.zeros(granularity)
  angulo_omega = np.zeros(granularity)
  ang_theta_t = np.zeros(granularity)
  func_accep = np.zeros(granularity)
  potencia_haz_1t = np.zeros(granularity)
  g_difus_beta = np.zeros(granularity)
  potencia_difus_1t = np.zeros(granularity)

  for i in range(granularity):
    nx[i], ny[i], nz[i] = m.sun_position(
        ang_delta, local_latitude, ang_omega[i])
    nnx[i], nny[i], nnz[i] = m.sun_position_prima(
        nx[i], ny[i], nz[i], inclination, azimuth)
    angulo_omega[i] = m.omega_angle(nnx[i], nny[i])
    ang_theta_t[i] = np.degrees(math.acos(math.sqrt(nnx[i]**2 + nny[i]**2)))
    func_accep[i] = m.acceptance_function(
        internal_diameter, external_diameter, pipeline_separation, angulo_omega[i])
    potencia_haz_1t[i] = m.direct_radiant_power(
        g_beam_n[i], internal_diameter, pipeline_length, ang_theta_t[i], func_accep[i])
    g_difus_beta[i] = m.diffuse_radiation_inclined_surface(
        g_difus[i], inclination)
    potencia_difus_1t[i] = m.diffuse_radiant_power(
        g_difus_beta[i], internal_diameter, pipeline_length, f_forma)

  potencia_total_1t = potencia_haz_1t + potencia_difus_1t

  return np.trapz(m.interpolate_nan_inf(potencia_total_1t), hora_std) / 1000
