import numpy as np
from thermal_model.theoretical import utils


def acceptance_function(D_int, D_ext, S_sep, ang_OMEGA):
  # Calcular los ángulos críticos OMEGA_0 y OMEGA_1
  # Angulo crítico mayor [deg]
  OMEGA_0 = utils.acosd((D_ext + D_int) / (2 * S_sep))
  # Angulo crítico menor [deg]
  OMEGA_1 = utils.acosd(((D_ext - D_int) / (2 * S_sep)))

  # Encontrar la función de aceptancia
  if ang_OMEGA <= OMEGA_0:
    f_aceptancia = 1  # Pasa toda la radiación solar
  elif OMEGA_0 < ang_OMEGA <= OMEGA_1:
    f_aceptancia = (S_sep / D_int) * np.cos(np.radians(ang_OMEGA)) + 0.5 * \
        (1 - (D_ext / D_int))  # Pasa una fracción de la radiación solar
  elif ang_OMEGA > OMEGA_1:
    f_aceptancia = 0  # No pasa ninguna radiación solar
  else:
    f_aceptancia = 1  # Caso no contemplado

  return f_aceptancia


if __name__ == '__main__':
  print(acceptance_function(0.5, 0.5, 0.5, 10))
