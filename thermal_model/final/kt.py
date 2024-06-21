def kt(T):
  """
  Función que entrega la conductividad térmica del agua [W/m K]

  Parámetros:
  T : float
      Temperatura en [C]

  Retorna:
  float
      Conductividad térmica del agua [W/m K]
  """

  conduct_termica = 0.5634 + 0.002 * T - 8e-6 * T**2

  return conduct_termica
