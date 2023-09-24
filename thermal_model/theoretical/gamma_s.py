import numpy as np
from thermal_model.theoretical.utils import acosd


def solar_azimuth_angle(zenith_angle, local_latitude, delta_angle, omega_angle):
  """
  Calculate the solar azimuth angle (decimal format).

  Parameters:
  - zenith_angle (float): Zenith angle (decimal format).
  - local_latitude (float): Latitude of the location where information is desired (decimal format).
  - delta_angle (float): Local declination angle (decimal format).
  - omega_angle (float): Hour angle (decimal format).

  Returns:
  - solar_azimuth_angle (float): Solar azimuth angle (decimal format).
  """
  zenith_angle_rad = np.deg2rad(zenith_angle)
  local_latitude_rad = np.deg2rad(local_latitude)
  delta_angle_rad = np.deg2rad(delta_angle)
  omega_angle_rad = np.deg2rad(omega_angle)

  expression = (np.cos(zenith_angle_rad) * np.sin(local_latitude_rad) - np.sin(delta_angle_rad)) / (
      np.sin(zenith_angle_rad) * np.cos(delta_angle_rad)
  )

  arccos_dec = acosd(expression)
  solar_azimuth_angle = np.sign(omega_angle_rad) * np.abs(arccos_dec)

  return solar_azimuth_angle


if __name__ == '__main__':
  print(solar_azimuth_angle(30, 90, 100, 70))
