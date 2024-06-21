def cp_t(T):
  """
  Función que entrega el calor específico del agua [J/kg K]

  Parámetros:
  T : float
      Temperatura en [C]

  Retorna:
  float
      Calor específico del agua [J/kg K]
  """

  # Calor específico como función de la temperatura [J/kg K]
  calor_especif = 4215 - 2.3787 * T + 0.0528 * T**2 - 0.0005 * T**3

  return calor_especif
