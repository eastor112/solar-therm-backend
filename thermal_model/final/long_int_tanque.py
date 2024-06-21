def long_int_tanque(S_sep, N_tubos):
  """
  Función que calcula la longitud interna del tanque [m]

  Parámetros:
  S_sep : float
      Separación entre centros de los tubos al vacío [m]
  N_tubos : int
      Número total de tubos al vacío

  Retorna:
  float
      Longitud interna del tanque [m]
  """

  Longitud_TK = S_sep * N_tubos

  return Longitud_TK
