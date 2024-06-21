def mu_t(T):
  """
  Función que entrega la viscosidad del agua [Pa s]

  Parámetros:
  T : float
      Temperatura en [C]

  Retorna:
  float
      Viscosidad del agua [Pa s]
  """

  viscosidad = 0.0018 - 5e-5 * T + 9e-7 * T**2 - 8e-9 * T**3 + 3e-11 * T**4

  return viscosidad
