def diffuse_radiation_horizontal(Go, tau_d):
    """
    Calculate diffuse radiation on a horizontal surface.

    Parameters:
    - Go (float): Extraterrestrial horizontal radiation [W/m2].
    - tau_d (float): Diffuse atmospheric transmissivity [-].

    Returns:
    - diffuse_radiation_horizontal (float): Diffuse radiation on a horizontal surface [W/m2].
    """
    diffuse_radiation_horizontal = Go * tau_d  # Diffuse radiation on a horizontal surface [W/m2] (Duffie & Beckam, 2020)

    return diffuse_radiation_horizontal

if __name__ == '__main__':
    print(diffuse_radiation_horizontal(10,  3))
