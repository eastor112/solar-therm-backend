import numpy as np


def Diam_Int_Tanque(Vol_TK, L_int_TK):
  """
  Función que calcula el diámetro interno del tanque [m]

  Parámetros:
  Vol_TK : float
      Volumen del tanque lleno de agua [m3]
  L_int_TK : float
      Longitud interna del tanque [m]

  Retorna:
  float
      Diámetro interno del tanque [m]
  """

  Diametro_TK = np.sqrt(4 * Vol_TK / (np.pi * L_int_TK))

  return Diametro_TK
