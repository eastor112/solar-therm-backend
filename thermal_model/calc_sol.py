import thermal_model.theoretical as m
import thermal_model.final as n
import numpy as np

# Datos
anho = 2022
mes = 1
dia = 1
hora = 12
minuto = 0
longitud_local = -79.0286
latitud_local = -8.11167
altitud_local = 33
inclinacion = 15
azimuth = 180


# Calculos
n = m.n_dia(dia, mes)
gon = m.g_on(n)
hora_solar = m.solar_time(n, hora, minuto, longitud_local)
ang_delta = m.delta(n)
ang_omega = m.omega(hora_solar)
ang_omega_s = m.omega_s(latitud_local, ang_delta)
hora_aparec_sol = m.sunrise(ang_omega_s)
hora_puesta_sol = m.sunset(ang_omega_s)
ang_theta = m.theta(ang_delta, latitud_local, inclinacion, azimuth, ang_omega)
ang_theta_z = m.theta_z(ang_delta, latitud_local, azimuth, ang_omega)
ang_alpha_s = m.alpha_s(ang_theta_z)
ang_gamma_s = m.gamma_s(ang_theta_z, latitud_local, ang_delta, ang_omega)
hora_estandar = m.standard_time(n, hora_solar, longitud_local)


# Cálculos angulares horarios
nn = 361
HoraSol = np.zeros(nn)
HoraStd = np.zeros(nn)
AngOmega = np.zeros(nn)
AngTheta = np.zeros(nn)
AngThetaZ = np.zeros(nn)
AngAlphaS = np.zeros(nn)
AngGammaS = np.zeros(nn)

for i in range(nn):
  HoraSol[i] = hora_aparec_sol + (hora_puesta_sol - hora_aparec_sol) / nn * i
  HoraStd[i] = np.standard_time(n, HoraSol[i], longitud_local)
  AngOmega[i] = np.omega(HoraSol[i])
  AngTheta[i] = np.theta(ang_delta, latitud_local,
                         inclinacion, azimuth, AngOmega[i])
  AngThetaZ[i] = np.theta_z(ang_delta, latitud_local, azimuth, AngOmega[i])
  AngAlphaS[i] = np.alpha_s(AngThetaZ[i])
  AngGammaS[i] = np.gamma_s(
      AngThetaZ[i], latitud_local, ang_delta, AngOmega[i])

# Charts
# figure(1)
# plot(HoraStd,AngAlphaS);
# title("Inclinación Solar");
# xlabel("Hora Estandar");
# ylabel("\\alpha_s [deg]");

# figure(2)
# plot(HoraStd,AngGammaS)
# title("Azimuth Solar");
# xlabel("Hora Estandar");
# ylabel("\\gamma_s [deg]");


# CALCULOS DE RADIACION HORIZONTAL INSTANTANEA E IRRADIACION HORIZONTAL DIARIA
# ============================================================================

# Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
Go = m.g_o(gon, ang_theta_z)

# Irradiacion diaria en el n dia [J/m2 dia]
Ho = m.h_o(gon, latitud_local, ang_delta, ang_omega_s)

# -------------------------------------------------------------------------------

# CALCULO DE LA RADIACION HORARIA EXTRATERRESTRE HORIZONTAL (en el n dia) [W/m2]
# ========================================================

Go_m = np.zeros(nn)

for i in range(nn):
  # Radiacion extraterrestre horizontal (instantanea) en  n dia y h hora y m minutos [W/m2]
  Go_m[i] = m.g_o(gon, AngTheta[i])

# figure(3)
# plot(HoraStd, Go_m, 'r');
# title("Intensidad de la Radiación Extraterrestre sobre Superficie Horizontal [W/m2]");
# xlabel("Hora Estandar");
# ylabel("Go [W/m^2]");

# CALCULO DE DISTRIBUCION DE LA IRRADIACION EXTRATERRESTRE HORIZONTAL EN INTERVALOS DE TIEMPO (en el n dia) [J/m2 h]
# ==========================================================================================

# Division de intervalos de tiempo en el dia (12: horaria, 24: cada media hora)
n_div = 12
# Espaciamiento horario entre el amanecer y el ocaso del sol [deg]
ang_omega_var = np.linspace(-ang_omega_s, ang_omega_s, n_div + 1)

Hora_m = np.zeros(n_div)
Io_m = np.zeros(n_div)

for j in range(n_div):
  # La hora donde se inicia el conteo de la irradiacion horaria
  Hora_m[j] = hora_aparec_sol + (hora_puesta_sol - hora_aparec_sol) / n_div * j
  Io_m[j] = m.l_o(gon, latitud_local, ang_delta, ang_omega_var[j],
                  ang_omega_var[j + 1])  # Irradiacion horaria [J/m2 h]


# figure(4)
# bar(Hora_m,Io_m, 'y')
# title("Irradiación Extraterrestre sobre Superficie Horizontal por Intervalo de Tiempo [J/m2 \\Deltat]");
# xlabel("Hora Estandar");
# ylabel("Io [J/m^2 \\Deltat]");


# ESTIMACION DE LA RADIACION DE HAZ EN CIELO DESPEJADO EN DIRECCION DEL SOL G_bn(Duffie, 2023)
# ==============================================================================

# trasmisividad del cielo de radiacion de haz
tau_b = m.taub(ang_theta_z, altitud_local)

Gbn = m.g_bn(gon, tau_b)  # Radiación de haz en dirección del sol [W/m2]

# ESTIMACION DE LA RADIACION DIFUSA HORIZONTAL EN CIELO DESPEJADO (Duffie, 2023)
# ===============================================================

tau_d = m.taud(tau_b)  # trasmisividad del cielo de radiacion difusa

Gd = m.g_d(Go, tau_d)  # Radiación difusa sobre superficie horizontal [W/m2]

# ESTIMACION DE LA RADIACION HORARIA DE HAZ Y DIFUSA EN CIELO DESPEJADO EN DIRECCION DEL SOL G_BEAM_n(Duffie, 2023)
# ==============================================================================

TAU_BEAM = np.zeros(nn)
G_BEAMn = np.zeros(nn)
TAU_DIF = np.zeros(nn)
G_OO = np.zeros(nn)
G_DIFUS = np.zeros(nn)

for i in range(nn):
  # trasmisividad horaria del cielo de radiacion de haz
  TAU_BEAM[i] = m.taub(AngThetaZ[i], altitud_local)
  # Radiación horaria de haz en dirección del sol [W/m2]
  G_BEAMn[i] = m.g_bn(gon, TAU_BEAM[i])

  # trasmisividad horaria del cielo de radiacion difusa
  TAU_DIF[i] = m.taud(TAU_BEAM[i])
  # Radiacion horaria extraterrestre horizontal (instantanea) en n dia y h hora y m minutos [W/m2]
  G_OO[i] = m.g_o(gon, AngThetaZ[i])
  # Radiación horaria difusa sobre superficie horizontal [W/m2]
  G_DIFUS[i] = m.g_d(G_OO[i], TAU_DIF[i])

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

ang_OMEGA = m.omega_o(nn_x, nn_y)  # Calcula el ángulo OMEGA

# Determina la función aceptancia
F_ac = m.f_acceptance(D_int, D_ext, S_sep, ang_OMEGA)

# Potencia radiante de haz en 1 tubo al vacio [W]
Pot_Haz_1T = m.direct_radiant_power(Gbn, D_int, L_tubo, ang_theta_t, F_ac)

# -------------------------------------------------------------------------------

# CÁLCULO DE POTENCIA DIFUSA QUE INCIDE EN UN TUBO AL VACIO [W] (Tang, 2009)
# ===================================================================

# Radiación difusa sobre superficie inclinada [W/m2]
Gdbeta = m.g_dbeta(Gd, inclinacion)

F_forma = m.f_ts(D_int, D_ext, S_sep)  # Función de forma para radiación difusa

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
  Nx[i], Ny[i], Nz[i] = m.sun_pos(ang_delta, latitud_local, AngOmega[i])
  # Array de Coordenadas modificadas durante el dia
  NNx[i], NNy[i], NNz[i] = m.sun_pos_prima(
      Nx[i], Ny[i], Nz[i], inclinacion, azimuth)
  # Calcula el ángulo OMEGA durante el dia
  ANGULO_OMEGA[i] = m.omega_o(NNx[i], NNy[i])
  # Angulo Theta_t, ángulo que se forma del rayo solar y la proyecion del rayo solar en el tubo [deg]
  AngThetaT[i] = np.degrees(np.arccos(np.sqrt(NNx[i]**2 + NNy[i]**2)))

  # Determina la función aceptancia
  FUNC_ACCEP[i] = m.f_acceptance(D_int, D_ext, S_sep, ANGULO_OMEGA[i])
  # Potencia radiante horaria de haz en 1 tubo al vacio [W]
  POTENCIA_HAZ_1T[i] = m.pot_rad_b_t(
      G_BEAMn[i], D_int, L_tubo, AngThetaT[i], FUNC_ACCEP[i])

  # Radiación difusa sobre superficie inclinada [W/m2]
  G_DIFUS_BETA[i] = m.g_dbeta(G_DIFUS[i], inclinacion)
  # Potencia radiante horaria difusa en 01 tubo al vacio [W]
  POTENCIA_DIFUS_1T[i] = m.pot_rad_d_t(G_DIFUS_BETA[i], D_int, L_tubo, F_forma)

# Potencia Total horaria que incide sobre 1 tubo al vacio
# Matria de potencia horaria total en 01 tubo al vacio [W]
POTENCIA_TOTAL_1T = POTENCIA_HAZ_1T + POTENCIA_DIFUS_1T


# plt.figure(5)
# plt.plot(HoraStd, POTENCIA_HAZ_1T, 'r', label='Potencia de Haz')
# plt.plot(HoraStd, POTENCIA_DIFUS_1T, 'g', label='Potencia Difusa')
# plt.plot(HoraStd, POTENCIA_TOTAL_1T, 'b', label='Potencia Total')
# plt.title(
#     "Potencia de Haz, Difusa y Total que absorbe 1 Tubo al vacío durante el día [W]")
# plt.xlabel("Hora Estandar")
# plt.ylabel("Pb, Pd, Pt [W]")
# plt.legend()
# plt.show()

# -----------------------------------------------------------------------------


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
T_amb = 20  # Temperatura del medio ambiente en [C]  (CASO TEORICO asmuido cte)
# Velocidad del viento [m/s]             (CASO TEORICO asumido cte)
v_viento = 3

# Datos ambientales - DATOS CLIMATICOS
# ------------------------------------
# Carga los vectores de datos climaticos segun el dia, mes y año escogido
datohora, datoradiacion, datotamb, datovviento = n.datoclimadiario(
    anho, mes, dia)
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
k_TK = 14.9  # Conductividad térmica del termotanque (acero inoxidable) [W/m K]
k_aisl = 0.06  # Conductividad térmica del aislante (poliuretano) [W/m K]
k_cub = 14.9  # Conductividad térmica de la cubierta (acero inoxidable) [W/m K]

# Datos adicionales
# -----------------
F_flujo = 0.45  # Es el factor de flujo - Razon de area transversal - area total donde sale agua caliente


print("Resultados de TERMASOLAR \n")
print("---------------------- \n")

# CALCULO DE LAS PROPIEDADES DEL AGUA (Cengel, 2015)
# ==================================================

Rho_T = m.rho_t(T_amb)      # Densidad de agua en [kg/m3]
K_T = m.kt(T_amb)          # Conductividad Térmica de agua [W/m K]
Cp_T = m.cp_t(T_amb)        # Calor Específico del Agua [J / kg K]
Mu_T = m.mu_t(T_amb)        # Viscosidad del agua [Pa s]
Beta_Coef = 0.000257     # Coeficiente de expansión volumétrica [1/K]

# CALCULO DE GEOMETRIA INTERNA DEL TERMOTANQUE
# ============================================

# Longitud interna del termotanque [m]
L_int_TK = n.long_int_tanque(S_sep, N_tubos)
# Diámetro interno del termotanque [m]
D_int_TK = n.diam_int_tanque(Vol_TK, L_int_TK)
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
K_MEZCLA_2 = np.zeros(nn)  # Creación del vector conductividad térmica [W/m K]

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
MDOT_SAL = np.zeros(nn)  # Creación del vector Flujo Másico a la Salida [kg/s]
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
RHO_MEZCLA[0] = n.rho_t(TEMP_AMB[0])

# Inicialmente la densidad de la mezcla es calculada a la temperatura ambiente - correlación de Mendoza 1800
RHO_MEZCLA_2[0] = n.rho_t(TEMP_AMB[0])

# Inicialmente la conductividad térmica de la mezcla es calculada a la temperatura ambiente
K_MEZCLA[0] = n.kt(TEMP_AMB[0])
# Inicialmente la conductividad térmica de la mezcla es calculada a la temperatura ambiente - correlación de Mendoza 1800
K_MEZCLA_2[0] = n.kt(TEMP_AMB[0])

# Inicialmente el calor específico de la mezcla es calculado a la temperatura ambiente
CP_MEZCLA[0] = n.cp_t(TEMP_AMB[0])
# Inicialmente el calor específico de la mezcla es calculado a la temperatura ambiente - correlación de Mendoza 1800
CP_MEZCLA_2[0] = n.cp_t(TEMP_AMB[0])

# Inicialmente la viscosidad dinámica de la mezcla es calculada a la temperatura ambiente
MU_MEZCLA[0] = n.mu_t(TEMP_AMB[0])
# Inicialmente la viscosidad dinámica de la mezcla es calculada a la temperatura ambiente - correlación de Mendoza 1800
MU_MEZCLA_2[0] = n.mu_t(TEMP_AMB[0])

# Inicialmente la densidad del tanque es calculada a la temperatura ambiente
RHO_TANQUE[0] = n.rho_t(TEMP_AMB[0])
# Inicialmente la densidad del tanque es calculada a la temperatura ambiente - correlación de Mendoza 1800
RHO_TANQUE_2[0] = n.rho_t(TEMP_AMB[0])

# Inicialmente la conductividad térmica del tanque es calculada a la temperatura ambiente
CP_TANQUE[0] = n.cp_t(TEMP_AMB[0])
# Inicialmente la conductividad térmica del tanque es calculada a la temperatura ambiente - correlación de Mendoza 1800
CP_TANQUE_2[0] = n.cp_t(TEMP_AMB[0])

NU_GR[0] = n.nu_gr(FLUJO_CALOR_1T[0], Beta_Coef, D_int, RHO_MEZCLA[0],
                   K_MEZCLA[0], MU_MEZCLA[0])  # Producto de Nusselt y Grasshof
NU_GR_2[0] = n.nu_gr(FLUJO_CALOR_1T[0], Beta_Coef, D_int, RHO_MEZCLA_2[0], K_MEZCLA_2[0],
                     MU_MEZCLA_2[0])  # Producto de Nusselt y Grasshof - correlación de Mendoza 1800

PR[0] = n.prandtl(CP_MEZCLA[0], MU_MEZCLA[0], K_MEZCLA[0])  # Número de Prandtl
# Número de Prandtl - correlación de Mendoza 1800
PR_2[0] = n.prandtl(CP_MEZCLA_2[0], MU_MEZCLA_2[0], K_MEZCLA_2[0])

RE[0] = n.budihardjo(NU_GR[0], PR[0], inclinacion, L_tubo,
                     D_int)  # Correlación de Budihardjo
# Correlación de Mendoza 1800
RE_2[0] = n.mendoza_1800(NU_GR_2[0], PR_2[0], inclinacion)

# Velocidad media de salida del flujo de agua caliente [m/s] - correlación de Budihardjo
VEL_SAL[0] = n.vel_sal(RE[0], MU_MEZCLA[0], RHO_MEZCLA[0], D_int, F_flujo)
# Velocidad media de salida del flujo de agua caliente [m/s] - correlación de Mendoza 1800
VEL_SAL_2[0] = n.vel_sal(RE_2[0], MU_MEZCLA_2[0],
                         RHO_MEZCLA_2[0], D_int, F_flujo)

# Flujo másico del flujo de agua caliente que sale del tubo al vacío [kg/s] - correlación de Budihardjo
MDOT_SAL[0] = n.mdot_sal(RE[0], MU_MEZCLA[0], D_int, F_flujo)
# Flujo másico del flujo de agua caliente que sale del tubo al vacío [kg/s] - correlación de Mendoza 1800
MDOT_SAL_2[0] = n.mdot_sal(RE_2[0], MU_MEZCLA_2[0], D_int, F_flujo)

# Inicialización de vectores adicionales
FLUJO_CALOR_1T[0] = 0  # Inicialmente el flujo de calor es igual a cero [W/m2]

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

  if POTENCIA_TOTAL_1T[0, i] >= 0:  # La potencia total debe ser positivo [W]

    # Calculo del vector Flujo de calor sobre el diámetro interno de 01 tubo al vacío [W/m2]
    FLUJO_CALOR_1T[0, i] = 2 * POTENCIA_TOTAL_1T[0, i] * \
        (Tau_glass * Alfa_glass) / (np.pi * D_int * L_tubo)

  else:

    FLUJO_CALOR_1T[0, i] = 0


for i in range(1, nn):  # nn es el número de divisiones del array durante los horarios de sunshine y sunset

    # Calculo de las propiedades del agua a la temperatura de mezcla
    # --------------------------------------------------------------
  # Densidad del agua a la temperatura de mezcla [kg/m3] - correlacion de Budihardjo
  RHO_MEZCLA[0, i] = n.rho_t(TEMP_MEZCLA[0, i])
  # Densidad del agua a la temperatura de mezcla [kg/m3] - correlacion de Mendoza 1800
  RHO_MEZCLA_2[0, i] = n.rho_t(TEMP_MEZCLA_2[0, i])

  # Conductividad térmica del agua a la temperatura de mezcla [W/m K] - correlacion de Budihardjo
  K_MEZCLA[0, i] = n.kt(TEMP_MEZCLA[0, i])
  # Conductividad térmica del agua a la temperatura de mezcla [W/m K] - correlacion de Mendoza 1800
  K_MEZCLA_2[0, i] = n.kt(TEMP_MEZCLA_2[0, i])

  # Calor específico del agua a la temperatura de mezcla [J/kg K] - correlacion de Budihardjo
  CP_MEZCLA[0, i] = n.cp_t(TEMP_MEZCLA[0, i])
  # Calor específico del agua a la temperatura de mezcla [J/kg K] - correlacion de Mendoza 1800
  CP_MEZCLA_2[0, i] = n.cp_t(TEMP_MEZCLA_2[0, i])

  # Viscosidad del agua a la temperatura de mezcla [Pa s] - correlacion de Budihardjo
  MU_MEZCLA[0, i] = n.mu_t(TEMP_MEZCLA[0, i])
  # Viscosidad del agua a la temperatura de mezcla [Pa s] - correlacion de Mendoza 1800
  MU_MEZCLA_2[0, i] = n.mu_t(TEMP_MEZCLA_2[0, i])

  # Calculo del producto NuGr
  # -------------------------
  NU_GR[0, i] = n.nu_gr(FLUJO_CALOR_1T[0, i], Beta_Coef, D_int, RHO_MEZCLA[0, i], K_MEZCLA[0, i],
                        MU_MEZCLA[0, i])  # Producto de Nusselt y Grasshof - correlacion de Budihardjo
  NU_GR_2[0, i] = n.nu_gr(FLUJO_CALOR_1T[0, i], Beta_Coef, D_int, RHO_MEZCLA_2[0, i], K_MEZCLA_2[0, i],
                          MU_MEZCLA_2[0, i])  # Producto de Nusselt y Grasshof - correlacion de Mendoza 1800

  # Calculo del número de Prandtl
  # -----------------------------
  # Número de Prandtl- correlacion de Budihardjo
  PR[0, i] = n.prandtl(CP_MEZCLA[0, i], MU_MEZCLA[0, i], K_MEZCLA[0, i])
  # Número de Prandtl - correlacion de Mendoza 1800
  PR_2[0, i] = n.prandtl(
      CP_MEZCLA_2[0, i], MU_MEZCLA_2[0, i], K_MEZCLA_2[0, i])

  # Calculo del Número de Reynolds - CORRELACION DE BUDIHARDJO Y MENDOZA 1800
  # -------------------------------------------------------------------------
  RE[0, i] = n.budihardjo(NU_GR[0, i], PR[0, i], inclinacion,
                          L_tubo, D_int)  # Correlacion de Budihardjo
  # Correlacion de Mendoza1800
  RE_2[0, i] = n.mendoza1800(NU_GR_2[0, i], PR_2[0, i], inclinacion)

  # Calculo de la velocidad media de la salida del agua caliente del tubo al vacío
  # ------------------------------------------------------------------------------
  # Con correlacion de Budiharjo
  VEL_SAL[0, i] = n.vel_sal(RE[0, i], MU_MEZCLA[0, i],
                            RHO_MEZCLA[0, i], D_int, F_flujo)
  # Con correlacion de Mendoza 1800
  VEL_SAL_2[0, i] = n.vel_sal(RE_2[0, i], MU_MEZCLA_2[0, i],
                              RHO_MEZCLA_2[0, i], D_int, F_flujo)

  # Calculo del flujo masico en la salida del agua caliente del tubo al vacío
  # ------------------------------------------------------------------------
  MDOT_SAL[0, i] = n.mdot_sal(RE[0, i], MU_MEZCLA[0, i], D_int, F_flujo)
  # Con correlacion de Mendoza1800
  MDOT_SAL_2[0, i] = n.mdot_sal(RE_2[0, i], MU_MEZCLA_2[0, i], D_int, F_flujo)

  # Calculo de la temperatura de mezcla inicial en función de la temperatura del tanque
  # -----------------------------------------------------------------------------------
  TEMP_MEZCLA[0, i] = n.temp_mezcla(FLUJO_CALOR_1T[0, i], L_tubo, RHO_MEZCLA[0, i],
                                    CP_MEZCLA[0, i], VEL_SAL[0, i], D_int, TEMP_TANQUE[0, i-1])
  TEMP_MEZCLA_2[0, i] = n.temp_mezcla(FLUJO_CALOR_1T[0, i], L_tubo, RHO_MEZCLA_2[0, i], CP_MEZCLA_2[0, i],
                                      VEL_SAL_2[0, i], D_int, TEMP_TANQUE_2[0, i-1])  # Con correlacion de Mendoza1800

  # Calculo de la temperatura media de agua caliente a la salida del tubo al vacío
  # ------------------------------------------------------------------------------
  TEMP_SALIDA[0, i] = n.temp_salida(
      TEMP_MEZCLA[0, i], TEMP_TANQUE[0, i-1], F_flujo, VEL_SAL[0, i])
  # Con correlacion de Mendoza1800
  TEMP_SALIDA_2[0, i] = n.temp_salida(
      TEMP_MEZCLA_2[0, i], TEMP_TANQUE_2[0, i-1], F_flujo, VEL_SAL_2[0, i])

  # CALCULOS TERMICOS EN EL TERMOTANQUE
  # ===================================

  # Calculo de la variación de la temperatura dentro del termotanque
  # -----------------------------------------------------------------
  DT_Dt[0, i] = n.dt_dt(MDOT_SAL[0, i], RHO_TANQUE[0, i-1], Vol_TK, N_tubos, CP_TANQUE[0, i-1],
                        TEMP_SALIDA[0, i], TEMP_TANQUE[0, i-1], TEMP_AMB[0, i-1], U_g, L_int_TK, D_int_TK)
  DT_Dt_2[0, i] = n.dt_dt(MDOT_SAL_2[0, i], RHO_TANQUE_2[0, i-1], Vol_TK, N_tubos, CP_TANQUE_2[0, i-1], TEMP_SALIDA_2[0, i],
                          TEMP_TANQUE_2[0, i-1], TEMP_AMB[0, i-1], U_g, L_int_TK, D_int_TK)  # Con correlacion de Mendoza1800

  # Calculo de la Temperatura del agua en el Tanque ACTUALIZADO
  # -----------------------------------------------------------
  TEMP_TANQUE[0, i] = TEMP_TANQUE[0, i-1] + \
      DT_Dt[0, i] * (HoraStd[0, i] - HoraStd[0, i-1]) * 3600
  TEMP_TANQUE_2[0, i] = TEMP_TANQUE_2[0, i-1] + DT_Dt_2[0, i] * \
      (HoraStd[0, i] - HoraStd[0, i-1]) * \
      3600  # Con correlacion de Mendoza1800

  # Asignación de las propiedades del agua en el tanque ACTUALIZADO
  # ---------------------------------------------------------------
  # Densidad del agua a la temperatura del tanque [kg/m3]

  # Densidad del agua a la temperatura del tanque [kg/m3]
  RHO_TANQUE[0, i] = n.rho_t(TEMP_TANQUE[0, i])
  # Densidad del agua a la temperatura del tanque [kg/m3] con correlacion de Mendoza 1800
  RHO_TANQUE_2[0, i] = n.rho_t(TEMP_TANQUE_2[0, i])

  # Calor específico del agua a la temperatura del tanque [J/kg K]
  CP_TANQUE[0, i] = n.cp_t(TEMP_TANQUE[0, i])
  # Calor específico del agua a la temperatura del tanque [J/kg K] con correlacion de Mendoza 1800
  CP_TANQUE_2[0, i] = n.cp_t(TEMP_TANQUE_2[0, i])


# ---------------------------SALIDAS----------------------------
# figure(6)
# plot(HoraStd, NU_GR./PR, 'b')
# title("Evolucion del Numero de Nu.Gr/Pr");
# xlabel("Hora Estandar");
# ylabel("Nu.Gr/Pr");


# figure(7)
# plot(HoraStd, RE_2, 'r')
# title("Evolucion del Numero de Reynolds");
# xlabel("Hora Estandar");
# ylabel("Re");


# figure(8)
# plot(HoraStd, MDOT_SAL_2*1000, 'g')
# title("Flujo Masico de Agua Caiente que Sale del Tubo al Vacio");
# xlabel("Hora Estandar");
# ylabel("\dot{m} [g/s]");


# figure(9)
# plot(HoraStd, VEL_SAL_2*1000, 'b')
# title("Velocidad Media Agua Caiente que Sale del Tubo al Vacio");
# xlabel("Hora Estandar");
# ylabel("u_z [mm/s]");


# figure(10)
# plot(HoraStd, TEMP_MEZCLA_2, 'g', HoraStd, TEMP_SALIDA_2, 'b', HoraStd, TEMP_TANQUE_2, 'r', HoraStd, TEMP_AMB,'--m')
# title("Temperaturas de Mezcla, de Salida y del Tanque de la Terma Solar [C] - Correlacion de Mendoza (2023)");
# xlabel("Hora Estandar");
# ylabel("T_m, T_s_a_l, T_t_k, T_a_m_b [C]");


# CALCULO DE LA EFICIENCIA TERMICA (1RA LEY) Y DE LA ENERGIA ALMACENADA
# =====================================================================

for i in range(1, nn):  # nn es el número de divisiones del array durante los horarios de sunshine y sunset

    # Calculo de la eficiencia termica segun la primera ley de la termodinamica.
    # -------------------------------------------------------------------------
  ETA_I[0, i] = n.eficiencia_1(RHO_TANQUE[0, i], Vol_TK, N_tubos, CP_TANQUE[0, i], DT_Dt[0, i], HoraStd[0, i-1], HoraStd[0, i],
                               POTENCIA_TOTAL_1T[0, i], D_int, L_tubo)  # Eficiencia térmica en estado transitorio de acuerdo a la primera ley de la termodinamica
  ETA_I_2[0, i] = n.eficiencia_1(RHO_TANQUE_2[0, i], Vol_TK, N_tubos, CP_TANQUE_2[0, i], DT_Dt_2[0, i], HoraStd[0, i-1], HoraStd[0, i],
                                 POTENCIA_TOTAL_1T[0, i], D_int, L_tubo)  # Eficiencia térmica en estado transitorio de acuerdo a la primera ley de la termodinamica

  # Calculo de la energia termica almacenada en cada paso de tiempo Delta_t [MJ]
  # ----------------------------------------------------------------------------
  ENERGIA_TK[0, i] = ENERGIA_TK[0, i-1] + RHO_TANQUE[0, i] * Vol_TK * CP_TANQUE[0, i] * DT_Dt[0, i] * \
      (HoraStd[0, i] - HoraStd[0, i-1]) * 3600 / \
      1e6  # Energia térmica acumulada en el tanque [MJ]
  ENERGIA_TK_2[0, i] = ENERGIA_TK_2[0, i-1] + RHO_TANQUE_2[0, i] * Vol_TK * CP_TANQUE_2[0, i] * DT_Dt_2[0,
                                                                                                        i] * (HoraStd[0, i] - HoraStd[0, i-1]) * 3600 / 1e6  # Energia térmica acumulada en el tanque [MJ]

# Calculo de la energia almacenada en el dia por la terma solar en [kW-h]
# ----------------------------------------------------------------------
# energia almacenada en el dia por la terma solar en [kW-h]
Energia_Almacenada = ENERGIA_TK[0, nn-1] / 3.6
# energia almacenada en el dia por la terma solar en [kW-h] - Correlacion de Mendoza 1800
Energia_Almacenada_2 = ENERGIA_TK_2[0, nn-1] / 3.6

# Calculo de la eficiencia global de la terma solar en 1 dia (segun la 1ra ley)
# ----------------------------------------------------------------------------
# Eficiencia global de la terma solar en 1 dia
eficienciaI_dia = Energia_Almacenada / Energia_total_NT
# Eficiencia global de la terma solar en 1 dia  - Correlacion de Mendoza 1800
eficienciaI_dia_2 = Energia_Almacenada_2 / Energia_total_NT


# ---------------------------SALIDAS----------------------------
# figure(11)
# plot(HoraStd, ETA_I_2, 'm')
# title("Eficiencia Termica de la Terma Solar (según la 1ra ley)");
# xlabel("Hora Estandar");
# ylabel("\\eta_I");


# figure(12)
# plot(HoraStd, ENERGIA_TK_2, 'c')
# title("Energia Térmica acumulada en el termotanque [MJ]");
# xlabel("Hora Estandar");
# ylabel("Energía Térmica [MJ]");


# disp("\n");
