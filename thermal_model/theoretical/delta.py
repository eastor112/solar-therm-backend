import numpy as np

def declination_angle(n):
    """
    Calculate the declination angle.

    Parameters:
    - n (int): nth day of the year.

    Returns:
    - declination_angle (float): Declination angle [deg].
    """
    B = (n - 1) * 360 / 365

    declination_angle = (180 / np.pi) * (0.006918 - 0.399912 * np.cos(np.radians(B)) + 0.070257 * np.sin(np.radians(B)) -
                                          0.006758 * np.cos(np.radians(2 * B)) + 0.000907 * np.sin(np.radians(2 * B)) -
                                          0.002697 * np.cos(np.radians(3 * B)) - 0.00148 * np.sin(np.radians(3 * B)))  # Declination angle [deg] (Iqbal, 1983)
    return declination_angle

if __name__ == '__main__':
    print(declination_angle(100))
