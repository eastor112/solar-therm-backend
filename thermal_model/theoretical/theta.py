import numpy as np


def incidence_angle(delta, phi, beta, gamma, omega):
  angulo_incidencia = np.degrees(np.arccos(
      np.sin(np.radians(delta)) * np.sin(np.radians(phi)) * np.cos(np.radians(beta)) -
      np.sin(np.radians(delta)) * np.cos(np.radians(phi)) * np.sin(np.radians(beta)) * np.cos(np.radians(gamma)) +
      np.cos(np.radians(delta)) * np.cos(np.radians(phi)) * np.cos(np.radians(beta)) * np.cos(np.radians(omega)) +
      np.cos(np.radians(delta)) * np.sin(np.radians(phi)) * np.sin(np.radians(beta)) * np.cos(np.radians(gamma)) * np.cos(np.radians(omega)) +
      np.cos(np.radians(delta)) * np.sin(np.radians(beta)) *
      np.sin(np.radians(gamma)) * np.sin(np.radians(omega))
  ))

  return angulo_incidencia


if __name__ == '__main__':
  print(incidence_angle(50, 70, 20, 40, 50))
