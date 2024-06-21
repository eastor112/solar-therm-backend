def eficiencia_1(Rho_Tanque, Vol_TK, N_tubos, Cp_Tanque, DT_Dt, HoraSTD_i1, HoraSTD_i2, potenciatotal1T, D_int, L_tubo):
  """
  Función que calcula la eficiencia instantánea de una terma solar en un instante dado

  Parámetros:
  Rho_Tanque : float
      Densidad a la temperatura del tanque [kg/m3]
  Vol_TK : float
      Volumen del tanque [m3]
  N_tubos : int
      Número de tubos [-]
  Cp_Tanque : float
      Calor específico a la temperatura del tanque [J/kg K]
  DT_Dt : float
      Tasa instantánea de cambio de temperatura [C/s]
  HoraSTD_i1 : float
      Instante de tiempo inicial [s]
  HoraSTD_i2 : float
      Instante de tiempo final [s]
  potenciatotal1T : float
      Potencia total que incide sobre la superficie interna de 1 tubo al vacío [W]
  D_int : float
      Diámetro interno del tubo al vacío [m]
  L_tubo : float
      Longitud del tubo al vacío [m]

  Retorna:
  eficiencia1 : float
      Eficiencia instantánea de la terma solar en el instante dado
  """

  if potenciatotal1T < 0:
    potenciatotal1T = 0  # Asegura que la potencia total siempre sea positiva

  # Incremento de energía de todo el tanque en Dt segundos
  Incremento_Energia = Rho_Tanque * Vol_TK * \
      Cp_Tanque * DT_Dt * (HoraSTD_i2 - HoraSTD_i1) * 3600

  # Energía absorbida por los N tubos en Dt segundos
  # Utilizamos 1e-9 para manejar números muy pequeños
  Calor_Absorbido = (potenciatotal1T + 1e-9) * N_tubos * \
      (HoraSTD_i2 - HoraSTD_i1) * 3600

  # Eficiencia térmica según la primera ley de la termodinámica
  eficiencia1 = Incremento_Energia / Calor_Absorbido

  if eficiencia1 < 0 or potenciatotal1T <= 0:
    eficiencia1 = 0  # Asegura que la eficiencia térmica siempre sea positiva

  return eficiencia1
