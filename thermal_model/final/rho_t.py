def rho_t(T):
  """
  Función que entrega la densidad del agua [kg/m3]

  Parámetros:
  T : float
      Temperatura en [C]

  Retorna:
  float
      Densidad del agua [kg/m3]
  """

  densidad = 1001 - 0.0834 * T - 0.0035 * T**2

  return densidad
