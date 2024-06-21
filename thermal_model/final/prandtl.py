def prandtl(Cp_T, Mu_T, K_T):
  """
  Función que entrega el número de Prandtl [-]

  Parámetros:
  Cp_T : float
      Calor específico del agua [J/kg K]
  Mu_T : float
      Viscosidad dinámica del agua [Pa.s]
  K_T : float
      Conductividad térmica del agua [W/m K]

  Retorna:
  float
      Número de Prandtl [-]
  """

  NumeroPrandtl = Cp_T * Mu_T / K_T

  return NumeroPrandtl
