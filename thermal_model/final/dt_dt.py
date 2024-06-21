import numpy as np


def dt_dt(mdot_sal, Rho_Tanque, Vol_TK, N_tubos, Cp_Tanque, temp_salida, temp_tanque, temp_amb, U_g, L_int_TK, D_int_TK):
  """
  Función que estima la variación de la temperatura en un intervalo de tiempo [C/s]

  Parámetros:
  mdot_sal : float
      Flujo másico de agua caliente que sale del tubo al vacío [kg/s]
  Rho_Tanque : float
      Densidad del agua a la temperatura del tanque [kg/m3]
  Vol_TK : float
      Volumen de agua en el termotanque [m3]
  N_tubos : int
      Número de tubos
  Cp_Tanque : float
      Calor específico del agua a la temperatura del tanque [J/kg K]
  temp_salida : float
      Temperatura media del agua caliente a la salida del tubo al vacío [C]
  temp_tanque : float
      Temperatura del tanque del tiempo pasado [C]
  temp_amb : float
      Temperatura ambiente [C]
  U_g : float
      Coeficiente global de transferencia de calor [W/m2 K]
  L_int_TK : float
      Longitud interna del termotanque [m]
  D_int_TK : float
      Diámetro interno del termotanque [m]

  Retorna:
  float
      Variación de la temperatura dentro del termotanque [C/s]
  """

  # Volumen de agua que calienta un tubo al vacío [m3]
  Vol_N = Vol_TK / N_tubos
  # Generatriz de la sección del cilindro que representa un tubo al vacío [m]
  Long_N = L_int_TK / N_tubos
  # Área de la generatriz externa del termotanque que representa un tubo al vacío [m2]
  Area_N = np.pi * D_int_TK * Long_N

  VariacionTemperatura = (mdot_sal / (Rho_Tanque * Vol_N)) * (temp_salida - temp_tanque) - \
                         (U_g * Area_N) / (Rho_Tanque * Vol_N *
                                           Cp_Tanque) * (temp_tanque - temp_amb)

  return VariacionTemperatura
