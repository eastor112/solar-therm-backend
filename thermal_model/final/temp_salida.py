def temp_salida(temp_mezcla, temp_tanque, F_flujo, vel_sal):
  """
  Función que entrega la temperatura media del agua caliente a la salida del tubo al vacío [C]

  Parámetros:
  temp_mezcla : float
      Temperatura de mezcla en el tubo al vacío [C]
  temp_tanque : float
      Temperatura del tanque del tiempo pasado [C]
  F_flujo : float
      Factor adimensional que relaciona el área del flujo de salida con el área interna del tubo al vacío [-]
  vel_sal : float
      Velocidad media de salida del agua caliente del tubo al vacío [m/s]

  Retorna:
  float
      Temperatura media del agua caliente a la salida del tubo al vacío [C]
  """

  if vel_sal == 0:
    TemperaturaSalida = temp_mezcla  # Caso no existe flujo másico (Re = 0)
  else:
    TemperaturaSalida = (temp_mezcla - temp_tanque * (1 - F_flujo)) / F_flujo

  return TemperaturaSalida
