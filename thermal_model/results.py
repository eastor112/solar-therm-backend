import numpy as np
import thermal_model.theoretical as m
from functools import lru_cache
import requests
from fastapi import HTTPException


def calcular_parametros_solares(
        anho, mes, dia, hora, minuto, longitud_local,
        latitud_local, altitud_local, inclinacion, azimuth, nn=361, n_div=12):
  n = m.day_number(dia, mes)
  gon = m.extraterrestrial_radiation(n)
  hora_solar = m.solar_time(n, hora, minuto, longitud_local)
  ang_delta = m.declination_angle(n)
  ang_omega = m.hour_angle(hora_solar)
  ang_omega_s = m.sunset_hour_angle(latitud_local, ang_delta)
  hora_aparec_sol = m.sunrise(ang_omega_s)
  hora_puesta_sol = m.sunset(ang_omega_s)
  ang_theta = m.incidence_angle(ang_delta, latitud_local,
                                inclinacion, azimuth, ang_omega)
  ang_theta_z = m.zenith_angle(ang_delta, latitud_local, azimuth, ang_omega)
  ang_alpha_s = m.solar_altitude_angle(ang_theta_z)
  ang_gamma_s = m.solar_azimuth_angle(
      ang_theta_z, latitud_local, ang_delta, ang_omega)
  hora_estandar = m.standard_time(n, hora_solar, longitud_local)

  # Cálculos angulares horarios
  HoraSol = np.zeros(nn)
  HoraStd = np.zeros(nn)
  AngOmega = np.zeros(nn)
  AngTheta = np.zeros(nn)
  AngThetaZ = np.zeros(nn)
  AngAlphaS = np.zeros(nn)
  AngGammaS = np.zeros(nn)

  for i in range(nn):
    HoraSol[i] = hora_aparec_sol + (hora_puesta_sol - hora_aparec_sol) / nn * i
    HoraStd[i] = m.standard_time(n, HoraSol[i], longitud_local)
    AngOmega[i] = m.hour_angle(HoraSol[i])
    AngTheta[i] = m.incidence_angle(ang_delta, latitud_local,
                                    inclinacion, azimuth, AngOmega[i])
    AngThetaZ[i] = m.zenith_angle(
        ang_delta, latitud_local, azimuth, AngOmega[i])
    AngAlphaS[i] = m.solar_altitude_angle(AngThetaZ[i])
    AngGammaS[i] = m.solar_azimuth_angle(
        AngThetaZ[i], latitud_local, ang_delta, AngOmega[i])

  # CALCULOS DE RADIACION HORIZONTAL INSTANTANEA E IRRADIACION HORIZONTAL DIARIA
  # ============================================================================

  # Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
  Go = m.extraterrestrial_horizontal_radiation(gon, ang_theta_z)

  # Irradiacion diaria en el n dia [J/m2 dia]
  Ho = m.daily_extraterrestrial_irradiance(
      gon, latitud_local, ang_delta, ang_omega_s)

  # -------------------------------------------------------------------------------

  # CALCULO DE LA RADIACION HORARIA EXTRATERRESTRE HORIZONTAL (en el n dia) [W/m2]
  # ========================================================

  Go_m = np.zeros(nn)

  for i in range(nn):
    # Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
    Go_m[i] = m.extraterrestrial_horizontal_radiation(gon, AngTheta[i])

  # CALCULO DE DISTRIBUCION DE LA IRRADIACION EXTRATERRESTRE HORIZONTAL EN INTERVALOS DE TIEMPO (en el n dia) [J/m2 h]
  # ==========================================================================================

  # Division de intervalos de tiempo en el dia (12: horaria, 24: cada media hora)
  # n_div = 12
  # Espaciamiento horario entre el amanecer y el ocaso del sol [deg]
  ang_omega_var = np.linspace(-ang_omega_s, ang_omega_s, n_div + 1)

  Hora_m = np.zeros(n_div)
  Io_m = np.zeros(n_div)

  for j in range(n_div):
    # La hora donde se inicia el conteo de la irradiacion horaria
    Hora_m[j] = hora_aparec_sol + \
        (hora_puesta_sol - hora_aparec_sol) / n_div * j
    Io_m[j] = m.extraterrestrial_irradiance_hourly(gon,
                                                   latitud_local, ang_delta, ang_omega_var[j],
                                                   ang_omega_var[j + 1])  # Irradiacion horaria [J/m2 h]

  # ESTIMACION DE LA RADIACION DE HAZ EN CIELO DESPEJADO EN DIRECCION DEL SOL G_bn(Duffie, 2023)
# ==============================================================================

  # trasmisividad del cielo de radiacion de haz
  tau_b = m.sky_transmissivity(ang_theta_z, altitud_local)

  # Radiación de haz en dirección del sol [W/m2]
  Gbn = m.beam_radiation(gon, tau_b)

  # ESTIMACION DE LA RADIACION DIFUSA HORIZONTAL EN CIELO DESPEJADO (Duffie, 2023)
  # ===============================================================

  # trasmisividad del cielo de radiacion difusa
  tau_d = m.diffuse_transmissivity(tau_b)

  # Radiación difusa sobre superficie horizontal [W/m2]
  Gd = m.diffuse_radiation_horizontal(Go, tau_d)

  # ESTIMACION DE LA RADIACION HORARIA DE HAZ Y DIFUSA EN CIELO DESPEJADO EN DIRECCION DEL SOL G_BEAM_n(Duffie, 2023)
  # ==============================================================================

  TAU_BEAM = np.zeros(nn)
  G_BEAMn = np.zeros(nn)
  TAU_DIF = np.zeros(nn)
  G_OO = np.zeros(nn)
  G_DIFUS = np.zeros(nn)

  for i in range(nn):
    # trasmisividad horaria del cielo de radiacion de haz
    TAU_BEAM[i] = m.sky_transmissivity(AngThetaZ[i], altitud_local)
    # Radiación horaria de haz en dirección del sol [W/m2]
    G_BEAMn[i] = m.beam_radiation(gon, TAU_BEAM[i])

    # trasmisividad horaria del cielo de radiacion difusa
    TAU_DIF[i] = m.diffuse_transmissivity(TAU_BEAM[i])
    # Radiacion horaria extraterrestre horizontal (instantanea) en n dia y h hora y m minutos [W/m2]
    G_OO[i] = m.extraterrestrial_horizontal_radiation(gon, AngThetaZ[i])
    # Radiación horaria difusa sobre superficie horizontal [W/m2]
    G_DIFUS[i] = m.diffuse_radiation_horizontal(G_OO[i], TAU_DIF[i])

  #######################################################################
  #######################################################################
  #######################################################################
  #######################################################################
  # POTTUBOS
  # Script que estima la potencia que se incide en los tubos al vacio (Tang, 2009)
  # Desarrollado por : Elder Marino Mendoza Orbegoso
  # Fecha 17 de setiembre del 2023
  #######################################################################

  # DATOS DE ENTRADA (CONFIGURACION GEOMÉTRICA)
  # ===========================================

  D_int = 0.048    # Diametro interno del tubo al vacio [m]
  D_ext = 0.058    # Diametro externo del tubo al vacio [m]
  L_tubo = 1.80    # Longitud efectivo del tubo al vacio expuesto al sol [m]
  S_sep = 0.056    # Distancia de separacion entre centro de tubos [m]

  # ---  Datos para la rutina terma solar ---
  Vol_TK = 0.300   # Volumen de agua en el termotanque [m3].
  N_tubos = 30     # Es el numero de tubos al vacio que tiene la terms solar
  e_TK = 0.0004    # Espesor del termotanque (acero inoxidable) [m]
  e_aisl = 0.005   # Espesor del aislante (poliuretano) [m]
  e_cub = 0.0004   # Espesor de la cubierta (acero inoxidable) [m]

  # SISTEMA DE COORDENADA DE LA POSICIÓN DEL SOL (NATURALES Y MODIFICADAS) (Tang, 2009)
  # ======================================================================

  n_x, n_y, n_z = m.sun_position(ang_delta, latitud_local,
                                 ang_omega)  # Coordenadas originales
  nn_x, nn_y, nn_z = m.sun_position_prima(
      n_x, n_y, n_z, inclinacion, azimuth)  # Coordenadas modificadas

  # Angulo Theta_t, ángulo que se forma del rayo solar y la proyecion del rayo solar en el tubo [deg]
  ang_theta_t = np.degrees(np.arccos(np.sqrt(nn_x**2 + nn_y**2)))

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA RADIANTE DE HAZ QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # ===================================================================

  ang_OMEGA = m.omega_angle(nn_x, nn_y)  # Calcula el ángulo OMEGA

  # Determina la función aceptancia
  F_ac = m.acceptance_function(D_int, D_ext, S_sep, ang_OMEGA)

  # Potencia radiante de haz en 1 tubo al vacio [W]
  Pot_Haz_1T = m.direct_radiant_power(Gbn, D_int, L_tubo, ang_theta_t, F_ac)

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA DIFUSA QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # ===================================================================

  # Radiación difusa sobre superficie inclinada [W/m2]
  Gdbeta = m.diffuse_radiation_inclined_surface(Gd, inclinacion)

  # Función de forma para radiación difusa
  F_forma = m.diffuse_radiation_shape_function(D_int, D_ext, S_sep)

  # Potencia radiante difuso en 01 tubo al vacio [W]
  Pot_Dif_1T = m.diffuse_radiant_power(Gdbeta, D_int, L_tubo, F_forma)

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA TOTAL QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # =================================================================

  # Potencia radiante total en 1 tubo al vacío [W]
  Pot_Tot_1T = Pot_Haz_1T + Pot_Dif_1T

  # Imprimir resultados o realizar otras operaciones necesarias
  print("\n")

  # CALCULO DE LAS POTENCIAS HORARIAS QUE INCIDEN SOBRE UN TUBO AL VACIO [W] (Tang, 2009)
  # =========================================================================

  Nx = np.zeros(nn)
  Ny = np.zeros(nn)
  Nz = np.zeros(nn)
  NNx = np.zeros(nn)
  NNy = np.zeros(nn)
  NNz = np.zeros(nn)
  ANGULO_OMEGA = np.zeros(nn)
  AngThetaT = np.zeros(nn)
  FUNC_ACCEP = np.zeros(nn)
  POTENCIA_HAZ_1T = np.zeros(nn)
  G_DIFUS_BETA = np.zeros(nn)
  POTENCIA_DIFUS_1T = np.zeros(nn)

  for i in range(nn):  # nn es el número de divisiones del array durante los horarios de sunshine y sunset
    # Array de coordenadas originales durante el dia.
    Nx[i], Ny[i], Nz[i] = m.sun_position(ang_delta, latitud_local, AngOmega[i])
    # Array de Coordenadas modificadas durante el dia
    NNx[i], NNy[i], NNz[i] = m.sun_position_prima(
        Nx[i], Ny[i], Nz[i], inclinacion, azimuth)
    # Calcula el ángulo OMEGA durante el dia
    ANGULO_OMEGA[i] = m.omega_angle(NNx[i], NNy[i])
    # Angulo Theta_t, ángulo que se forma del rayo solar y la proyecion del rayo solar en el tubo [deg]
    AngThetaT[i] = np.degrees(np.arccos(np.sqrt(NNx[i]**2 + NNy[i]**2)))

    # Determina la función aceptancia
    FUNC_ACCEP[i] = m.acceptance_function(D_int, D_ext, S_sep, ANGULO_OMEGA[i])
    # Potencia radiante horaria de haz en 1 tubo al vacio [W]
    POTENCIA_HAZ_1T[i] = m.direct_radiant_power(
        G_BEAMn[i], D_int, L_tubo, AngThetaT[i], FUNC_ACCEP[i])

    # Radiación difusa sobre superficie inclinada [W/m2]
    G_DIFUS_BETA[i] = m.diffuse_radiation_inclined_surface(
        G_DIFUS[i], inclinacion)
    # Potencia radiante horaria difusa en 01 tubo al vacio [W]
    POTENCIA_DIFUS_1T[i] = m.diffuse_radiant_power(
        G_DIFUS_BETA[i], D_int, L_tubo, F_forma)

  # Potencia Total horaria que incide sobre 1 tubo al vacio
  # Matria de potencia horaria total en 01 tubo al vacio [W]
  POTENCIA_TOTAL_1T = POTENCIA_HAZ_1T + POTENCIA_DIFUS_1T

  # Cálculo de la energía disponible para ser absorbida por 01 tubo al vacío durante el "n"-esimo dia
  # Energía disponible a ser absorbida durante el n-esimo dia [kW-hora]
  Energia_Total_1T = np.trapz(POTENCIA_TOTAL_1T, x=HoraStd) / 1000

  # Cálculo de la energía disponible para ser absorbida por los N tubos al vacío
  # Energía disponible a ser absorbida durante el n-esimo dia [kW-hora]
  Energia_total_NT = Energia_Total_1T * N_tubos

  return {
      "hora_std": HoraStd,
      "hora_m": Hora_m,
      "inclinacion_solar": AngAlphaS,
      "azimuth_solar": AngGammaS,
      "radiación_extraterrestre": Go_m,
      "irradiación_extraterrestre": Io_m,
      "potencia_tubo": Pot_Tot_1T,
      "potencia_haz": POTENCIA_HAZ_1T,
      "potencia_difusa": POTENCIA_DIFUS_1T,
      "potencia_total": POTENCIA_TOTAL_1T,
      "energia_tubo": Energia_Total_1T,
      "energia_n_tubo": Energia_total_NT,
  }


@lru_cache(maxsize=32)
def fetch_pvgis_data(
    lat: float,
    lon: float,
    raddatabase: str,
    startyear: int,
    endyear: int,
    angle: int,
    azimuth: int,
    outputformat: str
):
  params = {
      "lat": lat,
      "lon": lon,
      "raddatabase": raddatabase,
      "endyear": endyear,
      "startyear": startyear,
      "angle": angle,
      "aspect": azimuth,
      "outputformat": outputformat
  }

  url_base = f"https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?"

  url_params = "&".join(
      [f'{key}={value}' for key, value in params.items()])
  final_url = f'{url_base}&{url_params}'

  response = requests.get(final_url)

  if response.status_code == 200:
    return response.json()
  else:
    raise HTTPException(status_code=response.status_code,
                        detail=response.reason)
