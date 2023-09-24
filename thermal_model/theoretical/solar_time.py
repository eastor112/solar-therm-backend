import numpy as np

def solar_time(n, standard_hour, standard_minute, local_longitude):
    """
    Calculate solar time for a given standard time.

    Parameters:
    - n (int): The day of the year (n-th day).
    - standard_hour (int): The hour to calculate.
    - standard_minute (int): The additional minutes to add to the hour.
    - local_longitude (float): The longitude of the location in Peru being evaluated.

    Returns:
    - solar_time (float): Solar time in decimal hours.
    """
    standard_longitude = -75  # Standard longitude in Peru is 75 degrees west

    B = (n - 1) * 360 / 365

    standard_time = standard_hour + standard_minute / 60  # Hour expressed in decimal

    E = 229.2 * (0.000075 + 0.001868 * np.cos(np.deg2rad(B)) - 0.032077 * np.sin(np.deg2rad(B)) - 0.014615 * np.cos(np.deg2rad(2 * B)) - 0.04089 * np.sin(np.deg2rad(2 * B)))

    solar_time = standard_time + 4 * (standard_longitude - local_longitude) / 60 + E / 60  # Solar time expressed in decimal hours

    return solar_time


if __name__ == '__main__':
    print(solar_time(50, 8, 2, 60))
