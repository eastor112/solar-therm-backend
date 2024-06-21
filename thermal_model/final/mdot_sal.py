import numpy as np


def mdot_sal(Re, Mu_T, D_int, F_flujo):
  """
  Función que entrega la velocidad media de agua caliente que sale del tubo al vacío [m/s]

  Parámetros:
  Re : float
      Número de Reynolds [-]
  Mu_T : float
      Viscosidad dinámica [Pa.s]
  D_int : float
      Diámetro interno del tubo al vacío [m]
  F_flujo : float
      Factor adimensional que relaciona el área del flujo de salida con el área interna del tubo al vacío [-]

  Retorna:
  float
      Flujo másico de agua caliente que sale del tubo al vacío [kg/s]
  """

  FlujoMasicoSalida = (Re * Mu_T * np.pi * D_int / 4) * np.sqrt(F_flujo)

  return FlujoMasicoSalida
