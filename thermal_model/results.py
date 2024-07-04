import numpy as np
import thermal_model.theoretical as tm
import thermal_model.final as tf
import thermal_model.utils as tu


def get_therma_results(thermal_data, datetime, longitud_local, latitud_local, altitud_local,
                       inclinacion, azimuth, nn=361, n_div=12):
  anho, mes, dia, hora, minuto = tu.split_date(datetime)
  n = tm.day_number(dia, mes)
  gon = tm.extraterrestrial_radiation(n)
  hora_solar = tm.solar_time(n, hora, minuto, longitud_local)
  ang_delta = tm.declination_angle(n)
  ang_omega = tm.hour_angle(hora_solar)
  ang_omega_s = tm.sunset_hour_angle(latitud_local, ang_delta)
  hora_aparec_sol = tm.sunrise(ang_omega_s)
  hora_puesta_sol = tm.sunset(ang_omega_s)
  ang_theta = tm.incidence_angle(ang_delta, latitud_local,
                                 inclinacion, azimuth, ang_omega)
  ang_theta_z = tm.zenith_angle(ang_delta, latitud_local, azimuth, ang_omega)
  ang_alpha_s = tm.solar_altitude_angle(ang_theta_z)
  ang_gamma_s = tm.solar_azimuth_angle(
      ang_theta_z, latitud_local, ang_delta, ang_omega)
  hora_estandar = tm.standard_time(n, hora_solar, longitud_local)

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
    HoraStd[i] = tm.standard_time(n, HoraSol[i], longitud_local)
    AngOmega[i] = tm.hour_angle(HoraSol[i])
    AngTheta[i] = tm.incidence_angle(ang_delta, latitud_local,
                                     inclinacion, azimuth, AngOmega[i])
    AngThetaZ[i] = tm.zenith_angle(
        ang_delta, latitud_local, azimuth, AngOmega[i])
    AngAlphaS[i] = tm.solar_altitude_angle(AngThetaZ[i])
    AngGammaS[i] = tm.solar_azimuth_angle(
        AngThetaZ[i], latitud_local, ang_delta, AngOmega[i])

  # CALCULOS DE RADIACION HORIZONTAL INSTANTANEA E IRRADIACION HORIZONTAL DIARIA
  # ============================================================================

  # Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
  Go = tm.extraterrestrial_horizontal_radiation(gon, ang_theta_z)

  # Irradiacion diaria en el n dia [J/m2 dia]
  Ho = tm.daily_extraterrestrial_irradiance(
      gon, latitud_local, ang_delta, ang_omega_s)

  # -------------------------------------------------------------------------------

  # CALCULO DE LA RADIACION HORARIA EXTRATERRESTRE HORIZONTAL (en el n dia) [W/m2]
  # ========================================================

  Go_m = np.zeros(nn)

  for i in range(nn):
    # Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
    Go_m[i] = tm.extraterrestrial_horizontal_radiation(gon, AngTheta[i])

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
    Io_m[j] = tm.extraterrestrial_irradiance_hourly(gon,
                                                    latitud_local, ang_delta, ang_omega_var[j],
                                                    ang_omega_var[j + 1])  # Irradiacion horaria [J/m2 h]

  # ESTIMACION DE LA RADIACION DE HAZ EN CIELO DESPEJADO EN DIRECCION DEL SOL G_bn(Duffie, 2023)
# ==============================================================================

  # trasmisividad del cielo de radiacion de haz
  tau_b = tm.sky_transmissivity(ang_theta_z, altitud_local)

  # Radiación de haz en dirección del sol [W/m2]
  Gbn = tm.beam_radiation(gon, tau_b)

  # ESTIMACION DE LA RADIACION DIFUSA HORIZONTAL EN CIELO DESPEJADO (Duffie, 2023)
  # ===============================================================

  # trasmisividad del cielo de radiacion difusa
  tau_d = tm.diffuse_transmissivity(tau_b)

  # Radiación difusa sobre superficie horizontal [W/m2]
  Gd = tm.diffuse_radiation_horizontal(Go, tau_d)

  # ESTIMACION DE LA RADIACION HORARIA DE HAZ Y DIFUSA EN CIELO DESPEJADO EN DIRECCION DEL SOL G_BEAM_n(Duffie, 2023)
  # ==============================================================================

  TAU_BEAM = np.zeros(nn)
  G_BEAMn = np.zeros(nn)
  TAU_DIF = np.zeros(nn)
  G_OO = np.zeros(nn)
  G_DIFUS = np.zeros(nn)

  for i in range(nn):
    # trasmisividad horaria del cielo de radiacion de haz
    TAU_BEAM[i] = tm.sky_transmissivity(AngThetaZ[i], altitud_local)
    # Radiación horaria de haz en dirección del sol [W/m2]
    G_BEAMn[i] = tm.beam_radiation(gon, TAU_BEAM[i])

    # trasmisividad horaria del cielo de radiacion difusa
    TAU_DIF[i] = tm.diffuse_transmissivity(TAU_BEAM[i])
    # Radiacion horaria extraterrestre horizontal (instantanea) en n dia y h hora y m minutos [W/m2]
    G_OO[i] = tm.extraterrestrial_horizontal_radiation(gon, AngThetaZ[i])
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

  n_x, n_y, n_z = tm.sun_position(ang_delta, latitud_local,
                                  ang_omega)  # Coordenadas originales
  nn_x, nn_y, nn_z = tm.sun_position_prima(
      n_x, n_y, n_z, inclinacion, azimuth)  # Coordenadas modificadas

  # Angulo Theta_t, ángulo que se forma del rayo solar y la proyecion del rayo solar en el tubo [deg]
  ang_theta_t = np.degrees(np.arccos(np.sqrt(nn_x**2 + nn_y**2)))

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA RADIANTE DE HAZ QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # ===================================================================

  ang_OMEGA = tm.omega_angle(nn_x, nn_y)  # Calcula el ángulo OMEGA

  # Determina la función aceptancia
  F_ac = tm.acceptance_function(D_int, D_ext, S_sep, ang_OMEGA)

  # Potencia radiante de haz en 1 tubo al vacio [W]
  Pot_Haz_1T = tm.direct_radiant_power(Gbn, D_int, L_tubo, ang_theta_t, F_ac)

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA DIFUSA QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # ===================================================================

  # Radiación difusa sobre superficie inclinada [W/m2]
  Gdbeta = tm.diffuse_radiation_inclined_surface(Gd, inclinacion)

  # Función de forma para radiación difusa
  F_forma = tm.diffuse_radiation_shape_function(D_int, D_ext, S_sep)

  # Potencia radiante difuso en 01 tubo al vacio [W]
  Pot_Dif_1T = tm.diffuse_radiant_power(Gdbeta, D_int, L_tubo, F_forma)

  # -------------------------------------------------------------------------------

  # CÁLCULO DE POTENCIA TOTAL QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
  # =================================================================

  # Potencia radiante total en 1 tubo al vacío [W]
  Pot_Tot_1T = Pot_Haz_1T + Pot_Dif_1T

  # Imprimir resultados o realizar otras operaciones necesarias

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
    Nx[i], Ny[i], Nz[i] = tm.sun_position(
        ang_delta, latitud_local, AngOmega[i])
    # Array de Coordenadas modificadas durante el dia
    NNx[i], NNy[i], NNz[i] = tm.sun_position_prima(
        Nx[i], Ny[i], Nz[i], inclinacion, azimuth)
    # Calcula el ángulo OMEGA durante el dia
    ANGULO_OMEGA[i] = tm.omega_angle(NNx[i], NNy[i])
    # Angulo Theta_t, ángulo que se forma del rayo solar y la proyecion del rayo solar en el tubo [deg]
    AngThetaT[i] = tm.acosd(np.sqrt(NNx[i]**2 + NNy[i]**2)).real
    # Determina la función aceptancia
    FUNC_ACCEP[i] = tm.acceptance_function(
        D_int, D_ext, S_sep, ANGULO_OMEGA[i])
    # Potencia radiante horaria de haz en 1 tubo al vacio [W]
    POTENCIA_HAZ_1T[i] = tm.direct_radiant_power(
        G_BEAMn[i], D_int, L_tubo, AngThetaT[i], FUNC_ACCEP[i])

    # Radiación difusa sobre superficie inclinada [W/m2]
    G_DIFUS_BETA[i] = tm.diffuse_radiation_inclined_surface(
        G_DIFUS[i], inclinacion)
    # Potencia radiante horaria difusa en 01 tubo al vacio [W]
    POTENCIA_DIFUS_1T[i] = tm.diffuse_radiant_power(
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
  T_amb = 20
  # Velocidad del viento [m/s]             (CASO TEORICO asumido cte)
  v_viento = 3

  # Datos ambientales - DATOS CLIMATICOS
  # ------------------------------------
  # Carga los vectores de datos climaticos segun el dia, mes y año escogido
  datohora, datoradiacion, datotamb, datovviento = tf.split_data_by_datetime(
      thermal_data, "2020-01-01T06:00:00-05:00")
  # NOTA
  # ----
  # Caso se considere parametros ambientales, solamente se tiene almacenado los datos
  # ambientales de Trujillo (radiacion, temperatura ambiente y velocidad del viento) durante el año 2022

  # Datos opticos de tubos al vacio
  # -------------------------------
  Tau_glass = 0.93  # Transmisividad del tubo al vacio [-]
  Alfa_glass = 0.89  # Absortividad del tubo al vacio [-]

  # Datos relevantes a transferencia de calor a través de termotanque
  # -----------------------------------------------------------------
  # Coeficiente convectivo de transferencia de calor en el interior de termotanque [W/m2 K]
  h_int = 10
  # Coeficiente convectivo de transferencia de calor en el exterior del termotanque [W/m2 K]
  h_ext = 25
  # Conductividad térmica del termotanque (acero inoxidable) [W/m K]
  k_TK = 14.9
  k_aisl = 0.06  # Conductividad térmica del aislante (poliuretano) [W/m K]
  # Conductividad térmica de la cubierta (acero inoxidable) [W/m K]
  k_cub = 14.9

  # Datos adicionales
  # -----------------
  F_flujo = 0.45  # Es el factor de flujo - Razon de area transversal - area total donde sale agua caliente

  # CALCULO DE LAS PROPIEDADES DEL AGUA (Cengel, 2015)
  # ==================================================

  Rho_T = tf.rho_t(T_amb)      # Densidad de agua en [kg/m3]
  K_T = tf.kt(T_amb)          # Conductividad Térmica de agua [W/m K]
  Cp_T = tf.cp_t(T_amb)        # Calor Específico del Agua [J / kg K]
  Mu_T = tf.mu_t(T_amb)        # Viscosidad del agua [Pa s]
  Beta_Coef = 0.000257     # Coeficiente de expansión volumétrica [1/K]

  # CALCULO DE GEOMETRIA INTERNA DEL TERMOTANQUE
  # ============================================

  # Longitud interna del termotanque [m]
  L_int_TK = tf.long_int_tanque(S_sep, N_tubos)
  # Diámetro interno del termotanque [m]
  D_int_TK = tf.diam_int_tanque(Vol_TK, L_int_TK)
  # Diámetro externo del termotanque [m]
  D_ext_TK = D_int_TK + 2 * (e_TK + e_aisl + e_cub)

  # CALCULO DEL COEFICIENTE GLOBAL DE TRANFERENCIA DE CALOR DEL TERMOTANQUE (CON REFERENCIA AL AREA INTERNA)
  # =======================================================================================================

  U_g = 1 / (1/h_int + (D_int_TK / (2 * k_TK)) * np.log((D_int_TK + 2 * e_TK) / D_int_TK) +
             (D_int_TK / (2 * k_aisl)) * np.log((D_int_TK + 2 * (e_TK + e_aisl)) / (D_int_TK + 2 * e_TK)) +
             (D_int_TK / (2 * k_cub)) * np.log((D_int_TK + 2 * (e_TK + e_aisl + e_aisl)) / (D_int_TK + 2 * (e_TK + e_aisl))) +
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
    TEMP_AMB[i] = np.interp(HoraStd[i], datohora, datotamb)
    # Matriz de velocidad del viento [m/s] - CASO AMBIENTAL
    VEL_VIENTO[i] = np.interp(HoraStd[i], datohora, datovviento)

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
  DT_Dt = np.zeros(nn)
  # Creación del vector variación de temperatura en el tanque [C/s] - correlación de Mendoza 1800
  DT_Dt_2 = np.zeros(nn)

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

  NU_GR[0] = tf.nu_gr(FLUJO_CALOR_1T[0], Beta_Coef, D_int, RHO_MEZCLA[0],
                      K_MEZCLA[0], MU_MEZCLA[0])  # Producto de Nusselt y Grasshof
  NU_GR_2[0] = tf.nu_gr(FLUJO_CALOR_1T[0], Beta_Coef, D_int, RHO_MEZCLA_2[0], K_MEZCLA_2[0],
                        MU_MEZCLA_2[0])  # Producto de Nusselt y Grasshof - correlación de Mendoza 1800

  PR[0] = tf.prandtl(CP_MEZCLA[0], MU_MEZCLA[0],
                     K_MEZCLA[0])  # Número de Prandtl
  # Número de Prandtl - correlación de Mendoza 1800
  PR_2[0] = tf.prandtl(CP_MEZCLA_2[0], MU_MEZCLA_2[0], K_MEZCLA_2[0])

  RE[0] = tf.budihardjo(NU_GR[0], PR[0], inclinacion, L_tubo,
                        D_int)  # Correlación de Budihardjo
  # Correlación de Mendoza 1800
  RE_2[0] = tf.mendoza_1800(NU_GR_2[0], PR_2[0], inclinacion)

  # Velocidad media de salida del flujo de agua caliente [m/s] - correlación de Budihardjo
  VEL_SAL[0] = tf.vel_sal(RE[0], MU_MEZCLA[0], RHO_MEZCLA[0], D_int, F_flujo)
  # Velocidad media de salida del flujo de agua caliente [m/s] - correlación de Mendoza 1800
  VEL_SAL_2[0] = tf.vel_sal(RE_2[0], MU_MEZCLA_2[0],
                            RHO_MEZCLA_2[0], D_int, F_flujo)

  # Flujo másico del flujo de agua caliente que sale del tubo al vacío [kg/s] - correlación de Budihardjo
  MDOT_SAL[0] = tf.mdot_sal(RE[0], MU_MEZCLA[0], D_int, F_flujo)
  # Flujo másico del flujo de agua caliente que sale del tubo al vacío [kg/s] - correlación de Mendoza 1800
  MDOT_SAL_2[0] = tf.mdot_sal(RE_2[0], MU_MEZCLA_2[0], D_int, F_flujo)

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

  DT_Dt[0] = 0  # Inicialmente la derivada temporal de la temperatura es igual a cero [C/s] - correlación de Budihardjo
  # Inicialmente la derivada temporal de la temperatura es igual a cero [C/s] - correlación de Mendoza 1800
  DT_Dt_2[0] = 0

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
          (Tau_glass * Alfa_glass) / (np.pi * D_int * L_tubo)

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
    NU_GR[i] = tf.nu_gr(FLUJO_CALOR_1T[i], Beta_Coef, D_int, RHO_MEZCLA[i], K_MEZCLA[i],
                        MU_MEZCLA[i])  # Producto de Nusselt y Grasshof - correlacion de Budihardjo
    NU_GR_2[i] = tf.nu_gr(FLUJO_CALOR_1T[i], Beta_Coef, D_int, RHO_MEZCLA_2[i], K_MEZCLA_2[i],
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
                          L_tubo, D_int)  # Correlacion de Budihardjo
    # Correlacion de Mendoza1800
    RE_2[i] = tf.mendoza_1800(NU_GR_2[i], PR_2[i], inclinacion)

    # Calculo de la velocidad media de la salida del agua caliente del tubo al vacío
    # ------------------------------------------------------------------------------
    # Con correlacion de Budiharjo
    VEL_SAL[i] = tf.vel_sal(RE[i], MU_MEZCLA[i],
                            RHO_MEZCLA[i], D_int, F_flujo)
    # Con correlacion de Mendoza 1800
    VEL_SAL_2[i] = tf.vel_sal(RE_2[i], MU_MEZCLA_2[i],
                              RHO_MEZCLA_2[i], D_int, F_flujo)

    # Calculo del flujo masico en la salida del agua caliente del tubo al vacío
    # ------------------------------------------------------------------------
    MDOT_SAL[i] = tf.mdot_sal(RE[i], MU_MEZCLA[i], D_int, F_flujo)
    # Con correlacion de Mendoza1800
    MDOT_SAL_2[i] = tf.mdot_sal(
        RE_2[i], MU_MEZCLA_2[i], D_int, F_flujo)

    # Calculo de la temperatura de mezcla inicial en función de la temperatura del tanque
    # -----------------------------------------------------------------------------------
    TEMP_MEZCLA[i] = tf.temp_mezcla(FLUJO_CALOR_1T[i], L_tubo, RHO_MEZCLA[i],
                                    CP_MEZCLA[i], VEL_SAL[i], D_int, TEMP_TANQUE[i-1])
    TEMP_MEZCLA_2[i] = tf.temp_mezcla(FLUJO_CALOR_1T[i], L_tubo, RHO_MEZCLA_2[i], CP_MEZCLA_2[i],
                                      VEL_SAL_2[i], D_int, TEMP_TANQUE_2[i-1])  # Con correlacion de Mendoza1800

    # Calculo de la temperatura media de agua caliente a la salida del tubo al vacío
    # ------------------------------------------------------------------------------
    TEMP_SALIDA[i] = tf.temp_salida(
        TEMP_MEZCLA[i], TEMP_TANQUE[i-1], F_flujo, VEL_SAL[i])
    # Con correlacion de Mendoza1800
    TEMP_SALIDA_2[i] = tf.temp_salida(
        TEMP_MEZCLA_2[i], TEMP_TANQUE_2[i-1], F_flujo, VEL_SAL_2[i])

    # CALCULOS TERMICOS EN EL TERMOTANQUE
    # ===================================

    # Calculo de la variación de la temperatura dentro del termotanque
    # -----------------------------------------------------------------
    DT_Dt[i] = tf.dt_dt(MDOT_SAL[i], RHO_TANQUE[i-1], Vol_TK, N_tubos, CP_TANQUE[i-1],
                        TEMP_SALIDA[i], TEMP_TANQUE[i-1], TEMP_AMB[i-1], U_g, L_int_TK, D_int_TK)
    DT_Dt_2[i] = tf.dt_dt(MDOT_SAL_2[i], RHO_TANQUE_2[i-1], Vol_TK, N_tubos, CP_TANQUE_2[i-1], TEMP_SALIDA_2[i],
                          TEMP_TANQUE_2[i-1], TEMP_AMB[i-1], U_g, L_int_TK, D_int_TK)  # Con correlacion de Mendoza1800

    # Calculo de la Temperatura del agua en el Tanque ACTUALIZADO
    # -----------------------------------------------------------
    TEMP_TANQUE[i] = TEMP_TANQUE[i-1] + \
        DT_Dt[i] * (HoraStd[i] - HoraStd[i-1]) * 3600
    TEMP_TANQUE_2[i] = TEMP_TANQUE_2[i-1] + DT_Dt_2[i] * \
        (HoraStd[i] - HoraStd[i-1]) * \
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
    ETA_I[i] = tf.eficiencia_1(RHO_TANQUE[i], Vol_TK, N_tubos, CP_TANQUE[i], DT_Dt[i], HoraStd[i-1], HoraStd[i],
                               POTENCIA_TOTAL_1T[i], D_int, L_tubo)  # Eficiencia térmica en estado transitorio de acuerdo a la primera ley de la termodinamica
    ETA_I_2[i] = tf.eficiencia_1(RHO_TANQUE_2[i], Vol_TK, N_tubos, CP_TANQUE_2[i], DT_Dt_2[i], HoraStd[i-1], HoraStd[i],
                                 POTENCIA_TOTAL_1T[i], D_int, L_tubo)  # Eficiencia térmica en estado transitorio de acuerdo a la primera ley de la termodinamica

    # Calculo de la energia termica almacenada en cada paso de tiempo Delta_t [MJ]
    # ----------------------------------------------------------------------------
    ENERGIA_TK[i] = ENERGIA_TK[i-1] + RHO_TANQUE[i] * Vol_TK * CP_TANQUE[i] * DT_Dt[i] * \
        (HoraStd[i] - HoraStd[i-1]) * 3600 / \
        1e6  # Energia térmica acumulada en el tanque [MJ]
    ENERGIA_TK_2[i] = ENERGIA_TK_2[i-1] + RHO_TANQUE_2[i] * Vol_TK * CP_TANQUE_2[i] * DT_Dt_2[
        i] * (HoraStd[i] - HoraStd[i-1]) * 3600 / 1e6  # Energia térmica acumulada en el tanque [MJ]

  # Calculo de la energia almacenada en el dia por la terma solar en [kW-h]
  # ----------------------------------------------------------------------
  # energia almacenada en el dia por la terma solar en [kW-h]
  Energia_Almacenada = ENERGIA_TK[nn-1] / 3.6
  # energia almacenada en el dia por la terma solar en [kW-h] - Correlacion de Mendoza 1800
  Energia_Almacenada_2 = ENERGIA_TK_2[nn-1] / 3.6

  # Calculo de la eficiencia global de la terma solar en 1 dia (segun la 1ra ley)
  # ----------------------------------------------------------------------------
  # Eficiencia global de la terma solar en 1 dia
  eficienciaI_dia = Energia_Almacenada / Energia_total_NT
  # Eficiencia global de la terma solar en 1 dia  - Correlacion de Mendoza 1800
  eficienciaI_dia_2 = Energia_Almacenada_2 / Energia_total_NT

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
      "energia_acumulado_dia": Energia_Almacenada,
      "eficiencia_dia": eficienciaI_dia,
      "energia_acumulado_dia_mendoza": Energia_Almacenada_2,
      "eficiencia_dia_mendoza": eficienciaI_dia_2,
      "eficiencia_1": ETA_I_2,
      "energia_acumulada": ENERGIA_TK_2,
  }
