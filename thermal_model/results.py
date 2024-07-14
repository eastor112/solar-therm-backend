import numpy as np
import thermal_model.theoretical as tm
import thermal_model.final as tf
import thermal_model.utils as tu


def get_therma_results(params):
  thermal_data = params.get('thermal_data')
  date_time = params.get('date_time')
  longitud_local = params.get('longitud')
  latitud_local = params.get('latitud')
  altitud_local = params.get('altitud')
  inclinacion = params.get('inclinacion')
  azimuth = params.get('azimuth')
  t_amb = params.get('t_amb')
  v_viento = params.get('v_viento')
  d_int = params.get('d_int')
  d_ext = params.get('d_ext')
  lon_tubo = params.get('longitud_tubo')
  s_sep = params.get('s_sep')
  vol_tank = params.get('vol_tank')
  num_tubos = params.get('num_tubos')
  e_tank = params.get('e_tank')
  e_aisl = params.get('e_aisl')
  e_cub = params.get('e_cub')
  tau_glass = params.get('tau_glass')
  alfa_glass = params.get('alfa_glass')
  h_int = params.get('h_int')
  h_ext = params.get('h_ext')
  k_tank = params.get('k_tank')
  k_aisl = params.get('k_aisl')
  k_cub = params.get('k_cub')
  f_flujo = params.get('f_flujo')
  beta_coef = params.get('beta_coef')
  nn = params.get('nn')
  n_div = params.get('n_div')

  year, month, day, hour, minute = tu.split_date(date_time)
  day_number = tm.day_number(day, month)
  gon = tm.extraterrestrial_radiation(day_number)
  sun_hour = tm.solar_time(day_number, hour, minute, longitud_local)
  ang_delta = tm.declination_angle(day_number)
  ang_omega = tm.hour_angle(sun_hour)
  ang_omega_s = tm.sunset_hour_angle(latitud_local, ang_delta)
  sunrise_hour = tm.sunrise(ang_omega_s)
  sunset_hour = tm.sunset(ang_omega_s)
  ang_theta = tm.incidence_angle(ang_delta, latitud_local,
                                 inclinacion, azimuth, ang_omega)
  ang_theta_z = tm.zenith_angle(ang_delta, latitud_local, azimuth, ang_omega)
  ang_alpha_s = tm.solar_altitude_angle(ang_theta_z)
  ang_gamma_s = tm.solar_azimuth_angle(
      ang_theta_z, latitud_local, ang_delta, ang_omega)
  standard_hour = tm.standard_time(day_number, sun_hour, longitud_local)

  # Cálculos angulares horarios
  hourly_sun_time = np.zeros(nn)
  hourly_standard_time = np.zeros(nn)
  hourly_omega_angle = np.zeros(nn)
  hourly_theta_angle = np.zeros(nn)
  hourly_theta_z_angle = np.zeros(nn)
  hourly_alpha_s_angle = np.zeros(nn)
  hourly_gamma_s_angle = np.zeros(nn)

  for i in range(nn):
    hourly_sun_time[i] = sunrise_hour + (sunset_hour - sunrise_hour) / nn * i
    hourly_standard_time[i] = tm.standard_time(
        day_number, hourly_sun_time[i], longitud_local)
    hourly_omega_angle[i] = tm.hour_angle(hourly_sun_time[i])
    hourly_theta_angle[i] = tm.incidence_angle(ang_delta, latitud_local,
                                               inclinacion, azimuth, hourly_omega_angle[i])
    hourly_theta_z_angle[i] = tm.zenith_angle(
        ang_delta, latitud_local, azimuth, hourly_omega_angle[i])
    hourly_alpha_s_angle[i] = tm.solar_altitude_angle(hourly_theta_z_angle[i])
    hourly_gamma_s_angle[i] = tm.solar_azimuth_angle(
        hourly_theta_z_angle[i], latitud_local, ang_delta, hourly_omega_angle[i])

  # CALCULOS DE RADIACION HORIZONTAL INSTANTANEA E IRRADIACION HORIZONTAL DIARIA
  # ============================================================================

  # Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
  go = tm.extraterrestrial_horizontal_radiation(gon, ang_theta_z)

  # Irradiacion diaria en el n dia [J/m2 dia]
  ho = tm.daily_extraterrestrial_irradiance(
      gon, latitud_local, ang_delta, ang_omega_s)

  # -------------------------------------------------------------------------------

  # CALCULO DE LA RADIACION HORARIA EXTRATERRESTRE HORIZONTAL (en el n dia) [W/m2]
  # ========================================================

  go_m = np.zeros(nn)

  for i in range(nn):
    # Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
    go_m[i] = tm.extraterrestrial_horizontal_radiation(
        gon, hourly_theta_angle[i])

  # CALCULO DE DISTRIBUCION DE LA IRRADIACION EXTRATERRESTRE HORIZONTAL EN INTERVALOS DE TIEMPO (en el n dia) [J/m2 h]
  # ==========================================================================================

  # Division de intervalos de tiempo en el dia (12: horaria, 24: cada media hora)
  # n_div = 12
  # Espaciamiento horario entre el amanecer y el ocaso del sol [deg]
  ang_omega_var = np.linspace(-ang_omega_s, ang_omega_s, n_div + 1)

  hour_m = np.zeros(n_div)
  io_m = np.zeros(n_div)

  for j in range(n_div):
    # La hora donde se inicia el conteo de la irradiacion horaria
    hour_m[j] = sunrise_hour + \
        (sunset_hour - sunrise_hour) / n_div * j
    io_m[j] = tm.extraterrestrial_irradiance_hourly(gon,
                                                    latitud_local, ang_delta, ang_omega_var[j],
                                                    ang_omega_var[j + 1])  # Irradiacion horaria [J/m2 h]

  # ESTIMACION DE LA RADIACION DE HAZ EN CIELO DESPEJADO EN DIRECCION DEL SOL G_bn(Duffie, 2023)
# ==============================================================================

  # trasmisividad del cielo de radiacion de haz
  tau_b = tm.sky_transmissivity(ang_theta_z, altitud_local)

  # Radiación de haz en dirección del sol [W/m2]
  gbn = tm.beam_radiation(gon, tau_b)

  # ESTIMACION DE LA RADIACION DIFUSA HORIZONTAL EN CIELO DESPEJADO (Duffie, 2023)
  # ===============================================================

  # trasmisividad del cielo de radiacion difusa
  tau_d = tm.diffuse_transmissivity(tau_b)

  # Radiación difusa sobre superficie horizontal [W/m2]
  gd = tm.diffuse_radiation_horizontal(go, tau_d)

  # ESTIMACION DE LA RADIACION HORARIA DE HAZ Y DIFUSA EN CIELO DESPEJADO EN DIRECCION DEL SOL G_BEAM_n(Duffie, 2023)
  # ==============================================================================

  TAU_BEAM = np.zeros(nn)
  g_beam_n = np.zeros(nn)
  TAU_DIF = np.zeros(nn)
  G_OO = np.zeros(nn)
  G_DIFUS = np.zeros(nn)

  for i in range(nn):
    # trasmisividad horaria del cielo de radiacion de haz
    TAU_BEAM[i] = tm.sky_transmissivity(hourly_theta_z_angle[i], altitud_local)
    # Radiación horaria de haz en dirección del sol [W/m2]
    g_beam_n[i] = tm.beam_radiation(gon, TAU_BEAM[i])

    # trasmisividad horaria del cielo de radiacion difusa
    TAU_DIF[i] = tm.diffuse_transmissivity(TAU_BEAM[i])
    # Radiacion horaria extraterrestre horizontal (instantanea) en n dia y h hora y m minutos [W/m2]
    G_OO[i] = tm.extraterrestrial_horizontal_radiation(
        gon, hourly_theta_z_angle[i])
    # Radiación horaria difusa sobre superficie horizontal [W/m2]
    G_DIFUS[i] = tm.diffuse_radiation_horizontal(G_OO[i], TAU_DIF[i])

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

  # D_int = 0.048    # Diametro interno del tubo al vacio [m]
  # D_ext = 0.058    # Diametro externo del tubo al vacio [m]
  # L_tubo = 1.80    # Longitud efectivo del tubo al vacio expuesto al sol [m]
  # S_sep = 0.056    # Distancia de separacion entre centro de tubos [m]

  # # ---  Datos para la rutina terma solar ---
  # Vol_TK = 0.300   # Volumen de agua en el termotanque [m3].
  # N_tubos = 30     # Es el numero de tubos al vacio que tiene la terms solar
  # e_TK = 0.0004    # Espesor del termotanque (acero inoxidable) [m]
  # e_aisl = 0.005   # Espesor del aislante (poliuretano) [m]
  # e_cub = 0.0004   # Espesor de la cubierta (acero inoxidable) [m]

  # SISTEMA DE COORDENADA DE LA POSICIÓN DEL SOL (NATURALES Y MODIFICADAS) (Tang, 2009)
  # ======================================================================

  n_x, n_y, n_z = tm.sun_position(
      ang_delta, latitud_local, ang_omega)  # Coordenadas originales
  nn_x, nn_y, nn_z = tm.sun_position_prima(
      n_x, n_y, n_z, inclinacion, azimuth)  # Coordenadas modificadas

  # Angulo Theta_t, ángulo que se forma del rayo solar y la proyecion del rayo solar en el tubo [deg]
  ang_theta_t = np.degrees(np.arccos(np.sqrt(nn_x**2 + nn_y**2)))

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA RADIANTE DE HAZ QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # ===================================================================

  ang_OMEGA = tm.omega_angle(nn_x, nn_y)  # Calcula el ángulo OMEGA

  # Determina la función aceptancia
  f_ac = tm.acceptance_function(d_int, d_ext, s_sep, ang_OMEGA)

  # Potencia radiante de haz en 1 tubo al vacio [W]
  pot_haz_1t = tm.direct_radiant_power(gbn, d_int, lon_tubo, ang_theta_t, f_ac)

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA DIFUSA QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # ===================================================================

  # Radiación difusa sobre superficie inclinada [W/m2]
  gd_beta = tm.diffuse_radiation_inclined_surface(gd, inclinacion)

  # Función de forma para radiación difusa
  f_forma = tm.diffuse_radiation_shape_function(d_int, d_ext, s_sep)

  # Potencia radiante difuso en 01 tubo al vacio [W]
  pot_dif_1t = tm.diffuse_radiant_power(gd_beta, d_int, lon_tubo, f_forma)

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA TOTAL QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # =================================================================

  # Potencia radiante total en 1 tubo al vacío [W]
  pot_tot_1t = pot_haz_1t + pot_dif_1t

  # Imprimir resultados o realizar otras operaciones necesarias

  # CALCULO DE LAS POTENCIAS HORARIAS QUE INCIDEN SOBRE UN TUBO AL VACIO [W] (Tang, 2009)
  # =========================================================================

  n_x = np.zeros(nn)
  n_y = np.zeros(nn)
  n_z = np.zeros(nn)
  nn_x = np.zeros(nn)
  nn_y = np.zeros(nn)
  nn_z = np.zeros(nn)
  ANGULO_OMEGA = np.zeros(nn)
  theta_t_angle = np.zeros(nn)
  FUNC_ACCEP = np.zeros(nn)
  POTENCIA_HAZ_1T = np.zeros(nn)
  G_DIFUS_BETA = np.zeros(nn)
  POTENCIA_DIFUS_1T = np.zeros(nn)

  for i in range(nn):  # nn es el número de divisiones del array durante los horarios de sunshine y sunset
    # Array de coordenadas originales durante el dia.
    n_x[i], n_y[i], n_z[i] = tm.sun_position(
        ang_delta, latitud_local, hourly_omega_angle[i])
    # Array de Coordenadas modificadas durante el dia
    nn_x[i], nn_y[i], nn_z[i] = tm.sun_position_prima(
        n_x[i], n_y[i], n_z[i], inclinacion, azimuth)
    # Calcula el ángulo OMEGA durante el dia
    ANGULO_OMEGA[i] = tm.omega_angle(nn_x[i], nn_y[i])
    # Angulo Theta_t, ángulo que se forma del rayo solar y la proyecion del rayo solar en el tubo [deg]
    theta_t_angle[i] = tm.acosd(np.sqrt(nn_x[i]**2 + nn_y[i]**2)).real
    # Determina la función aceptancia
    FUNC_ACCEP[i] = tm.acceptance_function(
        d_int, d_ext, s_sep, ANGULO_OMEGA[i])
    # Potencia radiante horaria de haz en 1 tubo al vacio [W]
    POTENCIA_HAZ_1T[i] = tm.direct_radiant_power(
        g_beam_n[i], d_int, lon_tubo, theta_t_angle[i], FUNC_ACCEP[i])

    # Radiación difusa sobre superficie inclinada [W/m2]
    G_DIFUS_BETA[i] = tm.diffuse_radiation_inclined_surface(
        G_DIFUS[i], inclinacion)
    # Potencia radiante horaria difusa en 01 tubo al vacio [W]
    POTENCIA_DIFUS_1T[i] = tm.diffuse_radiant_power(
        G_DIFUS_BETA[i], d_int, lon_tubo, f_forma)

  # Potencia Total horaria que incide sobre 1 tubo al vacio
  # Matria de potencia horaria total en 01 tubo al vacio [W]
  POTENCIA_TOTAL_1T = POTENCIA_HAZ_1T + POTENCIA_DIFUS_1T

  # Cálculo de la energía disponible para ser absorbida por 01 tubo al vacío durante el "n"-esimo dia
  # Energía disponible a ser absorbida durante el n-esimo dia [kW-hora]
  energia_total_1t = np.trapz(POTENCIA_TOTAL_1T, x=hourly_standard_time) / 1000

  # Cálculo de la energía disponible para ser absorbida por los N tubos al vacío
  # Energía disponible a ser absorbida durante el n-esimo dia [kW-hora]
  energia_total_nt = energia_total_1t * num_tubos

  # -----------------------------------------------------------------------------
  # -----------------------------------------------------------------------------
  # -------------------ENERGIA TERMA SOLAR FILE----------------------------------
  # -----------------------------------------------------------------------------
  # -----------------------------------------------------------------------------

  # TERMASOLAR
  # Script que realiza el cálculo térmico de terma solar de tubos al vacío
  # Desarrollado por : Elder Marino Mendoza Orbegoso
  # Fecha 17 de setiembre del 2023

  # DATOS DE ENTRADA
  # ================

  # Datos ambientales - CASO TEORICO (Caso se considere T_amb=cte y v_viento = cte)
  # --------------------------------
  # Temperatura del medio ambiente en [C]  (CASO TEORICO asmuido cte)
  # T_amb = 20
  # Velocidad del viento [m/s]             (CASO TEORICO asumido cte)
  # v_viento = 3

  # Datos ambientales - DATOS CLIMATICOS
  # ------------------------------------
  # Carga los vectores de datos climaticos segun el dia, mes y año escogido
  dato_hora, dato_radiacion, dato_temp_amb, dato_v_viento = tf.split_data_by_datetime(
      thermal_data, date_time)
  # NOTA
  # ----
  # Caso se considere parametros ambientales, solamente se tiene almacenado los datos
  # ambientales de Trujillo (radiacion, temperatura ambiente y velocidad del viento) durante el año 2022

  # Datos opticos de tubos al vacio
  # -------------------------------
  # Tau_glass = 0.93  # Transmisividad del tubo al vacio [-]
  # Alfa_glass = 0.89  # Absortividad del tubo al vacio [-]

  # Datos relevantes a transferencia de calor a través de termotanque
  # -----------------------------------------------------------------
  # Coeficiente convectivo de transferencia de calor en el interior de termotanque [W/m2 K]
  # h_int = 10
  # Coeficiente convectivo de transferencia de calor en el exterior del termotanque [W/m2 K]
  # h_ext = 25
  # Conductividad térmica del termotanque (acero inoxidable) [W/m K]
  # k_TK = 14.9
  # k_aisl = 0.06  # Conductividad térmica del aislante (poliuretano) [W/m K]
  # Conductividad térmica de la cubierta (acero inoxidable) [W/m K]
  # k_cub = 14.9

  # Datos adicionales
  # -----------------
  # F_flujo = 0.45  # Es el factor de flujo - Razon de area transversal - area total donde sale agua caliente

  # CALCULO DE LAS PROPIEDADES DEL AGUA (Cengel, 2015)
  # ==================================================

  rho_t = tf.rho_t(t_amb)      # Densidad de agua en [kg/m3]
  k_t = tf.kt(t_amb)          # Conductividad Térmica de agua [W/m K]
  cp_T = tf.cp_t(t_amb)        # Calor Específico del Agua [J / kg K]
  mu_T = tf.mu_t(t_amb)        # Viscosidad del agua [Pa s]
  # Beta_Coef = 0.000257     # Coeficiente de expansión volumétrica [1/K]

  # CALCULO DE GEOMETRIA INTERNA DEL TERMOTANQUE
  # ============================================

  # Longitud interna del termotanque [m]
  l_int_tank = tf.long_int_tanque(s_sep, num_tubos)
  # Diámetro interno del termotanque [m]
  d_int_tank = tf.diam_int_tanque(vol_tank, l_int_tank)
  # Diámetro externo del termotanque [m]
  d_ext_tank = d_int_tank + 2 * (e_tank + e_aisl + e_cub)

  # CALCULO DEL COEFICIENTE GLOBAL DE TRANFERENCIA DE CALOR DEL TERMOTANQUE (CON REFERENCIA AL AREA INTERNA)
  # =======================================================================================================

  u_g = 1 / (1/h_int + (d_int_tank / (2 * k_tank)) * np.log((d_int_tank + 2 * e_tank) / d_int_tank) +
             (d_int_tank / (2 * k_aisl)) * np.log((d_int_tank + 2 * (e_tank + e_aisl)) / (d_int_tank + 2 * e_tank)) +
             (d_int_tank / (2 * k_cub)) * np.log((d_int_tank + 2 * (e_tank + e_aisl + e_aisl)) / (d_int_tank + 2 * (e_tank + e_aisl))) +
             1/h_ext)  # Coeficiente global de transferencia de calor del termotanque [W/m2 K] (A CALCULAR)

  # ESTABLECIMIENTO DE LA MATRIZ DE LOS PARAMETROS AMBIENTALES - CASO TEORICO
  # ==========================================================

  # TEMP_AMB = T_amb * np.ones(nn)        # Matriz de temperatura de ambiente [C] - CASO TEORICO
  # VEL_VIENTO = v_viento * np.ones(nn)   # Matriz de velocidad del viento [m/s] - CASO TEORICO

  # ESTABLECIMIENTO DE LA MATRIZ DE LOS PARAMETROS AMBIENTALES - CASO AMBIENTAL (TRUJILLO_2022)
  # ==========================================================

  TEMP_AMB = np.zeros(nn)
  VEL_VIENTO = np.zeros(nn)

  for i in range(nn):
    # Matriz de temperatura de ambiente [C] - CASO AMBIENTAL
    TEMP_AMB[i] = np.interp(hourly_standard_time[i], dato_hora, dato_temp_amb)
    # Matriz de velocidad del viento [m/s] - CASO AMBIENTAL
    VEL_VIENTO[i] = np.interp(hourly_standard_time[i],
                              dato_hora, dato_v_viento)

  # ASIGNACION DE LOS VECTORES Y CONDICIONES INICIALES
  # ==================================================
  # Asignación de los vectores
  # --------------------------

  # Creación del vector densidad de mezcla
  RHO_MEZCLA = np.zeros(nn)  # Creación del vector densidad [kg/m3]
  RHO_MEZCLA_2 = np.zeros(nn)  # Creación del vector densidad [kg/m3]

  # Creación del vector conductividad térmica de mezcla
  K_MEZCLA = np.zeros(nn)  # Creación del vector conductividad térmica [W/m K]
  # Creación del vector conductividad térmica [W/m K]
  K_MEZCLA_2 = np.zeros(nn)

  # Creación del vector calor específico de mezcla
  CP_MEZCLA = np.zeros(nn)  # Creación del vector calor específico [J/kg K]
  CP_MEZCLA_2 = np.zeros(nn)  # Creación del vector calor específico [J/kg K]

  # Creación del vector viscosidad dinámica de mezcla
  MU_MEZCLA = np.zeros(nn)  # Creación del vector viscosidad dinámica [Pa.s]
  MU_MEZCLA_2 = np.zeros(nn)  # Creación del vector viscosidad dinámica [Pa.s]

  # Creación del vector densidad del tanque
  RHO_TANQUE = np.zeros(nn)  # Creación del vector densidad [kg/m3]
  RHO_TANQUE_2 = np.zeros(nn)  # Creación del vector densidad [kg/m3]

  # Creación del vector calor específico del tanque
  CP_TANQUE = np.zeros(nn)  # Creación del vector calor específico [J/kg K]
  CP_TANQUE_2 = np.zeros(nn)  # Creación del vector calor específico [J/kg K]

  # Creación del vector Número de Prandtl
  NU_GR = np.zeros(nn)  # Creación del vector Nusselt por Grasshof
  NU_GR_2 = np.zeros(nn)  # Creación del vector Nusselt por Grasshof

  # Creación del vector Número de Prandtl
  PR = np.zeros(nn)  # Creación del vector Número de Prandtl
  PR_2 = np.zeros(nn)  # Creación del vector Número de Prandtl

  # Creación del vector Número de Reynolds
  RE = np.zeros(nn)  # Creación del vector Número de Reynolds
  RE_2 = np.zeros(nn)  # Creación del vector Número de Reynolds

  # Creación del vector velocidad de Salida [m/s]
  VEL_SAL = np.zeros(nn)  # Creación del vector velocidad de Salida [m/s]
  VEL_SAL_2 = np.zeros(nn)  # Creación del vector velocidad de Salida [m/s]

  # Creación del vector Flujo Másico a la Salida [kg/s]
  # Creación del vector Flujo Másico a la Salida [kg/s]
  MDOT_SAL = np.zeros(nn)
  # Creación del vector Flujo Másico a la Salida [kg/s]
  MDOT_SAL_2 = np.zeros(nn)

  # Creación del vector Flujo de Calor
  # Creación de la Temperatura de mezcla en el tubo [C]
  FLUJO_CALOR_1T = np.zeros(nn)

  # Creación del vector temperatura de mezcla
  # Creación de la Temperatura de mezcla en el tubo [C]
  TEMP_MEZCLA = np.zeros(nn)
  # Creación de la Temperatura de mezcla en el tubo [C] - correlación de Mendoza 1800
  TEMP_MEZCLA_2 = np.zeros(nn)

  # Creación del vector temperatura de agua en la salida del tubo
  # Creación de la Temperatura del agua en la salida del tubo [C]
  TEMP_SALIDA = np.zeros(nn)
  # Creación de la Temperatura del agua en la salida del tubo [C] - correlación de Mendoza 1800
  TEMP_SALIDA_2 = np.zeros(nn)

  # Creación del vector temperatura del agua en el tanque
  # Creación de la Temperatura del agua en el tanque [C]
  TEMP_TANQUE = np.zeros(nn)
  # Creación de la Temperatura del agua en el tanque [C] - correlación de Mendoza 1800
  TEMP_TANQUE_2 = np.zeros(nn)

  # Creación del vector derivada de la temperatura
  # Creación del vector variación de temperatura en el tanque [C/s]
  dtem_dt = np.zeros(nn)
  # Creación del vector variación de temperatura en el tanque [C/s] - correlación de Mendoza 1800
  dtem_dt_2 = np.zeros(nn)

  # Creación del vector Eficiencia Térmica basado en la primera ley
  # Creación de la matriz eficiencia térmica en estado transitorio
  ETA_I = np.zeros(nn)
  # Creación de la matriz eficiencia térmica en estado transitorio - correlación de Mendoza 1800
  ETA_I_2 = np.zeros(nn)

  # Creación del vector energía térmica diaria almacenada por la terma solar en horas de sol
  # Creación de la matriz energía diaria almacenada por la terma solar en horas de sol
  ENERGIA_TK = np.zeros(nn)
  # Creación de la matriz energía diaria almacenada por la terma solar en horas de sol - correlación de Mendoza 1800
  ENERGIA_TK_2 = np.zeros(nn)

  # Asignación de las condiciones iniciales
  # ---------------------------------------
  # Inicialmente la densidad de la mezcla es calculada a la temperatura ambiente
  RHO_MEZCLA[0] = tf.rho_t(TEMP_AMB[0])

  # Inicialmente la densidad de la mezcla es calculada a la temperatura ambiente - correlación de Mendoza 1800
  RHO_MEZCLA_2[0] = tf.rho_t(TEMP_AMB[0])

  # Inicialmente la conductividad térmica de la mezcla es calculada a la temperatura ambiente
  K_MEZCLA[0] = tf.kt(TEMP_AMB[0])
  # Inicialmente la conductividad térmica de la mezcla es calculada a la temperatura ambiente - correlación de Mendoza 1800
  K_MEZCLA_2[0] = tf.kt(TEMP_AMB[0])

  # Inicialmente el calor específico de la mezcla es calculado a la temperatura ambiente
  CP_MEZCLA[0] = tf.cp_t(TEMP_AMB[0])
  # Inicialmente el calor específico de la mezcla es calculado a la temperatura ambiente - correlación de Mendoza 1800
  CP_MEZCLA_2[0] = tf.cp_t(TEMP_AMB[0])

  # Inicialmente la viscosidad dinámica de la mezcla es calculada a la temperatura ambiente
  MU_MEZCLA[0] = tf.mu_t(TEMP_AMB[0])
  # Inicialmente la viscosidad dinámica de la mezcla es calculada a la temperatura ambiente - correlación de Mendoza 1800
  MU_MEZCLA_2[0] = tf.mu_t(TEMP_AMB[0])

  # Inicialmente la densidad del tanque es calculada a la temperatura ambiente
  RHO_TANQUE[0] = tf.rho_t(TEMP_AMB[0])
  # Inicialmente la densidad del tanque es calculada a la temperatura ambiente - correlación de Mendoza 1800
  RHO_TANQUE_2[0] = tf.rho_t(TEMP_AMB[0])

  # Inicialmente la conductividad térmica del tanque es calculada a la temperatura ambiente
  CP_TANQUE[0] = tf.cp_t(TEMP_AMB[0])
  # Inicialmente la conductividad térmica del tanque es calculada a la temperatura ambiente - correlación de Mendoza 1800
  CP_TANQUE_2[0] = tf.cp_t(TEMP_AMB[0])

  NU_GR[0] = tf.nu_gr(FLUJO_CALOR_1T[0], beta_coef, d_int, RHO_MEZCLA[0],
                      K_MEZCLA[0], MU_MEZCLA[0])  # Producto de Nusselt y Grasshof
  NU_GR_2[0] = tf.nu_gr(FLUJO_CALOR_1T[0], beta_coef, d_int, RHO_MEZCLA_2[0], K_MEZCLA_2[0],
                        MU_MEZCLA_2[0])  # Producto de Nusselt y Grasshof - correlación de Mendoza 1800

  PR[0] = tf.prandtl(CP_MEZCLA[0], MU_MEZCLA[0],
                     K_MEZCLA[0])  # Número de Prandtl
  # Número de Prandtl - correlación de Mendoza 1800
  PR_2[0] = tf.prandtl(CP_MEZCLA_2[0], MU_MEZCLA_2[0], K_MEZCLA_2[0])

  RE[0] = tf.budihardjo(NU_GR[0], PR[0], inclinacion, lon_tubo,
                        d_int)  # Correlación de Budihardjo
  # Correlación de Mendoza 1800
  RE_2[0] = tf.mendoza_1800(NU_GR_2[0], PR_2[0], inclinacion)

  # Velocidad media de salida del flujo de agua caliente [m/s] - correlación de Budihardjo
  VEL_SAL[0] = tf.vel_sal(RE[0], MU_MEZCLA[0], RHO_MEZCLA[0], d_int, f_flujo)
  # Velocidad media de salida del flujo de agua caliente [m/s] - correlación de Mendoza 1800
  VEL_SAL_2[0] = tf.vel_sal(RE_2[0], MU_MEZCLA_2[0],
                            RHO_MEZCLA_2[0], d_int, f_flujo)

  # Flujo másico del flujo de agua caliente que sale del tubo al vacío [kg/s] - correlación de Budihardjo
  MDOT_SAL[0] = tf.mdot_sal(RE[0], MU_MEZCLA[0], d_int, f_flujo)
  # Flujo másico del flujo de agua caliente que sale del tubo al vacío [kg/s] - correlación de Mendoza 1800
  MDOT_SAL_2[0] = tf.mdot_sal(RE_2[0], MU_MEZCLA_2[0], d_int, f_flujo)

  # Inicialización de vectores adicionales
  # Inicialmente el flujo de calor es igual a cero [W/m2]
  FLUJO_CALOR_1T[0] = 0

  # Inicialmente asignado a la temperatura ambiente [C] - correlación de Budihardjo
  TEMP_MEZCLA[0] = TEMP_AMB[0]
  # Inicialmente asignado a la temperatura ambiente [C] - correlación de Mendoza1800
  TEMP_MEZCLA_2[0] = TEMP_AMB[0]

  # Inicialmente asignado a la temperatura ambiente [C] - correlación de Budihardjo
  TEMP_SALIDA[0] = TEMP_AMB[0]
  # Inicialmente asignado a la temperatura ambiente [C] - correlación de Mendoza1800
  TEMP_SALIDA_2[0] = TEMP_AMB[0]

  # Inicialmente asignado a la temperatura ambiente [C] - correlación de Budihardjo
  TEMP_TANQUE[0] = TEMP_AMB[0]
  # Inicialmente asignado a la temperatura ambiente [C] - correlación de Mendoza1800
  TEMP_TANQUE_2[0] = TEMP_AMB[0]

  # Inicialmente la derivada temporal de la temperatura es igual a cero [C/s] - correlación de Budihardjo
  dtem_dt[0] = 0
  # Inicialmente la derivada temporal de la temperatura es igual a cero [C/s] - correlación de Mendoza 1800
  dtem_dt_2[0] = 0

  # Inicialmente la energía almacenada en el tanque es igual a cero [J] - correlación de Budihardjo
  ENERGIA_TK[0] = 0
  # Inicialmente la energía almacenada en el tanque es igual a cero [J] - correlación de Mendoza 1800
  ENERGIA_TK_2[0] = 0

  # CALCULO DE LA TERMOFLUIDICA DEL TUBO AL VACIO
  # =============================================

  for i in range(1, nn):  # nn es el número de divisiones del array durante los horarios de sunshine y sunset

    if POTENCIA_TOTAL_1T[i] >= 0:  # La potencia total debe ser positivo [W]

      # Calculo del vector Flujo de calor sobre el diámetro interno de 01 tubo al vacío [W/m2]
      FLUJO_CALOR_1T[i] = 2 * POTENCIA_TOTAL_1T[i] * \
          (tau_glass * alfa_glass) / (np.pi * d_int * lon_tubo)

    else:

      FLUJO_CALOR_1T[i] = 0

  for i in range(1, nn):  # nn es el número de divisiones del array durante los horarios de sunshine y sunset

      # Calculo de las propiedades del agua a la temperatura de mezcla
      # --------------------------------------------------------------
    # Densidad del agua a la temperatura de mezcla [kg/m3] - correlacion de Budihardjo
    RHO_MEZCLA[i] = tf.rho_t(TEMP_MEZCLA[i])
    # Densidad del agua a la temperatura de mezcla [kg/m3] - correlacion de Mendoza 1800
    RHO_MEZCLA_2[i] = tf.rho_t(TEMP_MEZCLA_2[i])

    # Conductividad térmica del agua a la temperatura de mezcla [W/m K] - correlacion de Budihardjo
    K_MEZCLA[i] = tf.kt(TEMP_MEZCLA[i])
    # Conductividad térmica del agua a la temperatura de mezcla [W/m K] - correlacion de Mendoza 1800
    K_MEZCLA_2[i] = tf.kt(TEMP_MEZCLA_2[i])

    # Calor específico del agua a la temperatura de mezcla [J/kg K] - correlacion de Budihardjo
    CP_MEZCLA[i] = tf.cp_t(TEMP_MEZCLA[i])
    # Calor específico del agua a la temperatura de mezcla [J/kg K] - correlacion de Mendoza 1800
    CP_MEZCLA_2[i] = tf.cp_t(TEMP_MEZCLA_2[i])

    # Viscosidad del agua a la temperatura de mezcla [Pa s] - correlacion de Budihardjo
    MU_MEZCLA[i] = tf.mu_t(TEMP_MEZCLA[i])
    # Viscosidad del agua a la temperatura de mezcla [Pa s] - correlacion de Mendoza 1800
    MU_MEZCLA_2[i] = tf.mu_t(TEMP_MEZCLA_2[i])

    # Calculo del producto NuGr
    # -------------------------
    NU_GR[i] = tf.nu_gr(FLUJO_CALOR_1T[i], beta_coef, d_int, RHO_MEZCLA[i], K_MEZCLA[i],
                        MU_MEZCLA[i])  # Producto de Nusselt y Grasshof - correlacion de Budihardjo
    NU_GR_2[i] = tf.nu_gr(FLUJO_CALOR_1T[i], beta_coef, d_int, RHO_MEZCLA_2[i], K_MEZCLA_2[i],
                          MU_MEZCLA_2[i])  # Producto de Nusselt y Grasshof - correlacion de Mendoza 1800

    # Calculo del número de Prandtl
    # -----------------------------
    # Número de Prandtl- correlacion de Budihardjo
    PR[i] = tf.prandtl(CP_MEZCLA[i], MU_MEZCLA[i], K_MEZCLA[i])
    # Número de Prandtl - correlacion de Mendoza 1800
    PR_2[i] = tf.prandtl(
        CP_MEZCLA_2[i], MU_MEZCLA_2[i], K_MEZCLA_2[i])

    # Calculo del Número de Reynolds - CORRELACION DE BUDIHARDJO Y MENDOZA 1800
    # -------------------------------------------------------------------------
    RE[i] = tf.budihardjo(NU_GR[i], PR[i], inclinacion,
                          lon_tubo, d_int)  # Correlacion de Budihardjo
    # Correlacion de Mendoza1800
    RE_2[i] = tf.mendoza_1800(NU_GR_2[i], PR_2[i], inclinacion)

    # Calculo de la velocidad media de la salida del agua caliente del tubo al vacío
    # ------------------------------------------------------------------------------
    # Con correlacion de Budiharjo
    VEL_SAL[i] = tf.vel_sal(RE[i], MU_MEZCLA[i],
                            RHO_MEZCLA[i], d_int, f_flujo)
    # Con correlacion de Mendoza 1800
    VEL_SAL_2[i] = tf.vel_sal(RE_2[i], MU_MEZCLA_2[i],
                              RHO_MEZCLA_2[i], d_int, f_flujo)

    # Calculo del flujo masico en la salida del agua caliente del tubo al vacío
    # ------------------------------------------------------------------------
    MDOT_SAL[i] = tf.mdot_sal(RE[i], MU_MEZCLA[i], d_int, f_flujo)
    # Con correlacion de Mendoza1800
    MDOT_SAL_2[i] = tf.mdot_sal(
        RE_2[i], MU_MEZCLA_2[i], d_int, f_flujo)

    # Calculo de la temperatura de mezcla inicial en función de la temperatura del tanque
    # -----------------------------------------------------------------------------------
    TEMP_MEZCLA[i] = tf.temp_mezcla(FLUJO_CALOR_1T[i], lon_tubo, RHO_MEZCLA[i],
                                    CP_MEZCLA[i], VEL_SAL[i], d_int, TEMP_TANQUE[i-1])
    TEMP_MEZCLA_2[i] = tf.temp_mezcla(FLUJO_CALOR_1T[i], lon_tubo, RHO_MEZCLA_2[i], CP_MEZCLA_2[i],
                                      VEL_SAL_2[i], d_int, TEMP_TANQUE_2[i-1])  # Con correlacion de Mendoza1800

    # Calculo de la temperatura media de agua caliente a la salida del tubo al vacío
    # ------------------------------------------------------------------------------
    TEMP_SALIDA[i] = tf.temp_salida(
        TEMP_MEZCLA[i], TEMP_TANQUE[i-1], f_flujo, VEL_SAL[i])
    # Con correlacion de Mendoza1800
    TEMP_SALIDA_2[i] = tf.temp_salida(
        TEMP_MEZCLA_2[i], TEMP_TANQUE_2[i-1], f_flujo, VEL_SAL_2[i])

    # CALCULOS TERMICOS EN EL TERMOTANQUE
    # ===================================

    # Calculo de la variación de la temperatura dentro del termotanque
    # -----------------------------------------------------------------
    dtem_dt[i] = tf.dt_dt(MDOT_SAL[i], RHO_TANQUE[i-1], vol_tank, num_tubos, CP_TANQUE[i-1],
                          TEMP_SALIDA[i], TEMP_TANQUE[i-1], TEMP_AMB[i-1], u_g, l_int_tank, d_int_tank)
    dtem_dt_2[i] = tf.dt_dt(MDOT_SAL_2[i], RHO_TANQUE_2[i-1], vol_tank, num_tubos, CP_TANQUE_2[i-1], TEMP_SALIDA_2[i],
                            TEMP_TANQUE_2[i-1], TEMP_AMB[i-1], u_g, l_int_tank, d_int_tank)  # Con correlacion de Mendoza1800

    # Calculo de la Temperatura del agua en el Tanque ACTUALIZADO
    # -----------------------------------------------------------
    TEMP_TANQUE[i] = TEMP_TANQUE[i-1] + \
        dtem_dt[i] * (hourly_standard_time[i] -
                      hourly_standard_time[i-1]) * 3600
    TEMP_TANQUE_2[i] = TEMP_TANQUE_2[i-1] + dtem_dt_2[i] * \
        (hourly_standard_time[i] - hourly_standard_time[i-1]) * \
        3600  # Con correlacion de Mendoza1800

    # Asignación de las propiedades del agua en el tanque ACTUALIZADO
    # ---------------------------------------------------------------
    # Densidad del agua a la temperatura del tanque [kg/m3]

    # Densidad del agua a la temperatura del tanque [kg/m3]
    RHO_TANQUE[i] = tf.rho_t(TEMP_TANQUE[i])
    # Densidad del agua a la temperatura del tanque [kg/m3] con correlacion de Mendoza 1800
    RHO_TANQUE_2[i] = tf.rho_t(TEMP_TANQUE_2[i])

    # Calor específico del agua a la temperatura del tanque [J/kg K]
    CP_TANQUE[i] = tf.cp_t(TEMP_TANQUE[i])
    # Calor específico del agua a la temperatura del tanque [J/kg K] con correlacion de Mendoza 1800
    CP_TANQUE_2[i] = tf.cp_t(TEMP_TANQUE_2[i])

  for i in range(1, nn):  # nn es el número de divisiones del array durante los horarios de sunshine y sunset

    # Calculo de la eficiencia termica segun la primera ley de la termodinamica.
    # -------------------------------------------------------------------------
    ETA_I[i] = tf.eficiencia_1(RHO_TANQUE[i], vol_tank, num_tubos, CP_TANQUE[i], dtem_dt[i], hourly_standard_time[i-1], hourly_standard_time[i],
                               POTENCIA_TOTAL_1T[i], d_int, lon_tubo)  # Eficiencia térmica en estado transitorio de acuerdo a la primera ley de la termodinamica
    ETA_I_2[i] = tf.eficiencia_1(RHO_TANQUE_2[i], vol_tank, num_tubos, CP_TANQUE_2[i], dtem_dt_2[i], hourly_standard_time[i-1], hourly_standard_time[i],
                                 POTENCIA_TOTAL_1T[i], d_int, lon_tubo)  # Eficiencia térmica en estado transitorio de acuerdo a la primera ley de la termodinamica

    # Calculo de la energia termica almacenada en cada paso de tiempo Delta_t [MJ]
    # ----------------------------------------------------------------------------
    ENERGIA_TK[i] = ENERGIA_TK[i-1] + RHO_TANQUE[i] * vol_tank * CP_TANQUE[i] * dtem_dt[i] * \
        (hourly_standard_time[i] - hourly_standard_time[i-1]) * 3600 / \
        1e6  # Energia térmica acumulada en el tanque [MJ]
    ENERGIA_TK_2[i] = ENERGIA_TK_2[i-1] + RHO_TANQUE_2[i] * vol_tank * CP_TANQUE_2[i] * dtem_dt_2[
        i] * (hourly_standard_time[i] - hourly_standard_time[i-1]) * 3600 / 1e6  # Energia térmica acumulada en el tanque [MJ]

  # Calculo de la energia almacenada en el dia por la terma solar en [kW-h]
  # ----------------------------------------------------------------------
  # energia almacenada en el dia por la terma solar en [kW-h]
  energia_Almacenada = ENERGIA_TK[nn-1] / 3.6
  # energia almacenada en el dia por la terma solar en [kW-h] - Correlacion de Mendoza 1800
  energia_almacenada_2 = ENERGIA_TK_2[nn-1] / 3.6

  # Calculo de la eficiencia global de la terma solar en 1 dia (segun la 1ra ley)
  # ----------------------------------------------------------------------------
  # Eficiencia global de la terma solar en 1 dia
  eficiencia_1_dia = energia_Almacenada / energia_total_nt
  # Eficiencia global de la terma solar en 1 dia  - Correlacion de Mendoza 1800
  eficienciaI_dia_2 = energia_almacenada_2 / energia_total_nt

  return {
      "hora_std": hourly_standard_time,
      "hora_m": hour_m,
      "inclinacion_solar": hourly_alpha_s_angle,
      "azimuth_solar": hourly_gamma_s_angle,
      "radiacion_extraterrestre": go_m,
      "irradiacion_extraterrestre": io_m,
      "potencia_tubo": pot_tot_1t,
      "potencia_haz": POTENCIA_HAZ_1T,
      "potencia_difusa": POTENCIA_DIFUS_1T,
      "potencia_total": POTENCIA_TOTAL_1T,
      "energia_tubo": energia_total_1t,
      "energia_n_tubo": energia_total_nt,
      "energia_acumulado_dia": energia_Almacenada,
      "eficiencia_dia": eficiencia_1_dia,
      "energia_acumulado_dia_mendoza": energia_almacenada_2,
      "eficiencia_dia_mendoza": eficienciaI_dia_2,
      "evolucion_nu_gr_pr": NU_GR / PR,
      "evolucion_reynolds": RE_2,
      "flujo_masico": MDOT_SAL_2 * 1000,
      "velocidad_salida": VEL_SAL_2 * 1000,
      "temperatura_mezcla": TEMP_MEZCLA_2,
      "temperatura_salida": TEMP_SALIDA_2,
      "temperatura_tanque": TEMP_TANQUE_2,
      "temperatura_ambiente": TEMP_AMB,
      "eficiencia_1": ETA_I_2,
      "energia_acumulada": ENERGIA_TK_2,
  }
