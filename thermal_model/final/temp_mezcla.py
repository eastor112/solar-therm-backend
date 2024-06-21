def temp_mezcla(flujocalor1T, L_tubo, Rho_T, Cp_T, vel_sal, D_int, temp_tanque):
  """
  Función que entrega la temperatura de mezcla en el tubo al vacío [C]

  Parámetros:
  flujocalor1T : float
      Flujo de calor sobre la pared interna del tubo al vacío [W/m2]
  L_tubo : float
      Longitud del tubo al vacío [m]
  Rho_T : float
      Densidad del agua [kg/m3]
  Cp_T : float
      Calor específico del agua [J/kg K]
  vel_sal : float
      Velocidad de agua caliente a la salida del tubo al vacío [m/s]
  D_int : float
      Diámetro interno del tubo al vacío [m]
  temp_tanque : float
      Temperatura del tanque del tiempo pasado [C]

  Retorna:
  float
      Temperatura de mezcla en el tubo al vacío [C]
  """

  eps = 1e-10  # Pequeño valor para evitar división por cero

  TemperaturaMezcla = (2 * flujocalor1T * L_tubo) / \
      (Rho_T * Cp_T * (vel_sal + eps) * D_int) + temp_tanque

  return TemperaturaMezcla
