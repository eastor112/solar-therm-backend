from math import sqrt


def VelSal(Re, Mu_T, Rho_T, D_int, F_flujo):
  """
  Función que entrega la velocidad media de agua caliente que sale del tubo al vacío [m/s]

  Parámetros:
  Re : float
      Número de Reynolds [-]
  Mu_T : float
      Viscosidad dinámica [Pa.s]
  Rho_T : float
      Densidad [kg/m3]
  D_int : float
      Diámetro interno del tubo al vacío [m]
  F_flujo : float
      Factor adimensional que relaciona el área del flujo de salida con el área interna del tubo al vacío [-]

  Retorna:
  float
      Velocidad media de agua caliente que sale del tubo al vacío [m/s]
  """

  VelocidadSalida = (Re * Mu_T) / (Rho_T * D_int * sqrt(F_flujo))

  return VelocidadSalida
