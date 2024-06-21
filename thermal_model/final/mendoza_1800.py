import numpy as np


def mendoza_1800(Nu_Gr, Pr, inclinacion):
  """
  Función que entrega el número de Reynolds según la correlación de Mendoza para tubos de 48, 58 y 1800 mm [-]

  Parámetros:
  Nu_Gr : float
      Producto Número de Nusselt y Número de Grasshof [-]
  Pr : float
      Número de Prandtl [-]
  inclinacion : float
      Ángulo de inclinación del tubo al vacío [deg]

  Retorna:
  float
      Número de Reynolds según la correlación de Mendoza [-]
  """

  # Asignación de los coeficientes de Mendoza1800
  a_2 = 0.3662
  b_2 = 0.4286
  k_2 = 1.15

  # Correlación de Mendoza
  Reynolds1800 = a_2 * \
      ((Nu_Gr / Pr) * (1 / np.cos(np.deg2rad(k_2 * inclinacion))))**b_2

  return Reynolds1800
