import numpy as np

def standard_time(n, solar_time, local_longitude):
    """
    Calculate standard time for a given solar time and location.

    Parameters:
    - n (int): The n-th day of the year.
    - solar_time (float): The solar time in decimal format.
    - local_longitude (float): The longitude of the location in Peru.

    Returns:
    - float: The standard time in decimal format.
    """

    standard_longitude = -75

    B = (n - 1) * 360 / 365
    E = 229.2 * (0.000075 + 0.001868 * np.cos(np.radians(B)) - 0.032077 * np.sin(np.radians(B)) -
                 0.014615 * np.cos(np.radians(2 * B)) - 0.04089 * np.sin(np.radians(2 * B)))

    tiempo_estandar = solar_time - 4 * (standard_longitude - local_longitude) / 60 - E / 60

    return tiempo_estandar

if __name__ == '__main__':
    print(standard_time(50, 8, 2))
