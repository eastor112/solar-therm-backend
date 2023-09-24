import numpy as np

def extraterrestrial_horizontal_radiation(Gon, ang_theta_z):
    """
    Calculate extraterrestrial horizontal radiation.

    Parameters:
    - Gon (float): Extraterrestrial radiation [W/m2].
    - ang_theta_z (float): Zenith angle [deg].

    Returns:
    - extraterrestrial_horizontal_radiation (float): Extraterrestrial horizontal radiation [W/m2].
    """
    extraterrestrial_horizontal_radiation = Gon * np.cos(np.deg2rad(ang_theta_z))  # Extraterrestrial Horizontal Radiation [W/m2] (Duffie & Beckam, 2020)

    return extraterrestrial_horizontal_radiation

if __name__ == '__main__':
    print(extraterrestrial_horizontal_radiation(10,  3))
