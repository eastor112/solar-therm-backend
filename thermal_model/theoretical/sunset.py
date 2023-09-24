def sunset(omega_s):
    """
    Calculate the solar time of sunset.

    Parameters:
    - omega_s (float): Hour angle at sunset in degrees.

    Returns:
    - solar_time_sunset (float): Solar time of sunset (in decimal format).
    """
    solar_time_sunset = 12 + (omega_s / 15)  # Provides the solar time when the sun sets below the horizon.

    return solar_time_sunset

if __name__ == '__main__':
    print(sunset(50))
