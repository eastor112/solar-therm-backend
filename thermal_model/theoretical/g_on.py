import numpy as np

def extraterrestrial_radiation(n):
    """
    Calculate extraterrestrial radiation.

    Parameters:
    - n (int): The n-th day of the year (1-365).

    Returns:
    - extraterrestrial_radiation (float): Extraterrestrial radiation [W/m2].
    """
    G_sc = 1367  # Solar Constant [W/m2] (Duffie & Beckam, 2020)

    extraterrestrial_radiation = G_sc * (1 + 0.033 * np.cos(np.deg2rad(360 * n / 365)))  # Extraterrestrial Radiation [W/m2] (Duffie & Beckam, 2020)

    return extraterrestrial_radiation

if __name__ == '__main__':
    print(extraterrestrial_radiation(10))
