def nu_gr(flujocalor1T, Beta_Coef, D_int, Rho_T, K_T, Mu_T):
  """
  Función que entrega el producto del número de Nusselt y el Número de Grasshof [-]

  Parámetros:
  flujocalor1T : float
      Flujo de calor sobre la pared interna del tubo al vacío [W/m2]
  Beta_Coef : float
      Coeficiente de expansión volumétrica del agua [1/K]
  D_int : float
      Diámetro interno del tubo al vacío [m]
  Rho_T : float
      Densidad del agua [kg/m3]
  K_T : float
      Conductividad térmica del agua [W/m K]
  Mu_T : float
      Viscosidad dinámica del agua [Pa.s]

  Retorna:
  float
      Producto del número de Nusselt y el número de Grasshof [-]
  """

  g = 9.81  # Aceleración de la gravedad [m/s2]

  if flujocalor1T >= 0:
    NusseltGrasshof = (flujocalor1T * g * Beta_Coef *
                       D_int**4 * Rho_T**2) / (K_T * Mu_T**2)
  else:
    NusseltGrasshof = 0

  return NusseltGrasshof
