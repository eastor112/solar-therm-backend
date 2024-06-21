import numpy as np


def budihardjo(Nu_Gr, Pr, inclinacion, L_tubo, D_int):
  """
  Función que entrega el número de Reynolds según la correlación de Budihardjo [-]

  Parámetros:
  Nu_Gr : float
      Variable producto Número de Nusselt y Número de Grasshof [-]
  Pr : float
      Variable Número de Prandtl [-]
  inclinacion : float
      Ángulo de inclinación del tubo al vacío [deg]
  L_tubo : float
      Longitud del tubo al vacío [m]
  D_int : float
      Diámetro interno del tubo al vacío [m]

  Retorna:
  float
      Número de Reynolds según la correlación de Budihardjo [-]
  """

  # Asignación de los coeficientes de Budihardjo
  a_0 = 0.1914
  a_1 = 0.4084
  n = 1.2

  # Correlación de Budihardjo
  Reynolds = a_0 * ((Nu_Gr / Pr) * np.cos(np.deg2rad(inclinacion))
                    * (L_tubo / D_int)**n)**a_1

  return Reynolds
