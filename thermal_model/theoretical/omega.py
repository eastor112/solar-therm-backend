def hour_angle(solar_time):
    """
    Calculate the hour angle.

    Parameters:
    - solar_time (float): Solar time (in decimal format).

    Returns:
    - hour_angle (float): The hour angle [degrees].
    """
    hour_angle = 15 * (solar_time - 12)  # Provides the hour angle [degrees]

    return hour_angle

if __name__ == '__main__':
    print(hour_angle(56))
