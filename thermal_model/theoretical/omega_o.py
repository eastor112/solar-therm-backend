import numpy as np


def omega_angle(nn_x, nn_y):
  """
  Calculate the OMEGA angle.

  Parameters:
  - nn_x (float): Normal direction to the inclined plane.
  - nn_y (float): Direction from east to south.

  Returns:
  - omega_angle (float): The OMEGA angle [degrees].
  """

  return np.abs(np.degrees(np.arctan(nn_y / nn_x)))


if __name__ == '__main__':
  print(omega_angle(12, 2))
