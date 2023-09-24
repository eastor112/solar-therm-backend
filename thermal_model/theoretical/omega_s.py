import numpy as np

def sunset_hour_angle(local_latitude, delta_angle):
    """
    Calculate the hour angle at sunset.

    Parameters:
    - local_latitude (float): Local latitude (in decimal format).
    - delta_angle (float): Declination angle (in decimal format).

    Returns:
    - sunset_hour_angle (float): The hour angle at sunset [degrees].
    """
    sunset_hour_angle = np.arccos(-np.tan(np.deg2rad(local_latitude)) * np.tan(np.deg2rad(delta_angle)))  # Provides the hour angle at sunset [degrees]

    return np.degrees(sunset_hour_angle)


if __name__ == '__main__':
    print(sunset_hour_angle(12, 56))
