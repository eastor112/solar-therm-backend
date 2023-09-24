import numpy as np

def extraterrestrial_irradiance_hourly(Gon, latitud_local, ang_delta, ang_omega_o, ang_omega_f):
    """
    Calculate the hourly extraterrestrial horizontal irradiance [J/m2 hour].

    Parameters:
    - Gon (float): Extraterrestrial radiation [W/m2].
    - latitud_local (float): Local latitude [deg].
    - ang_delta (float): Declination angle [deg].
    - ang_omega_o (float): Initial hour angle [deg].
    - ang_omega_f (float): Final hour angle [deg].

    Returns:
    - extraterrestrial_irradiance_hourly (float): Hourly extraterrestrial horizontal irradiance [J/m2 hour].
    """
    latitud_local_rad = np.deg2rad(latitud_local)
    ang_delta_rad = np.deg2rad(ang_delta)
    ang_omega_o_rad = np.deg2rad(ang_omega_o)
    ang_omega_f_rad = np.deg2rad(ang_omega_f)

    extraterrestrial_irradiance_hourly = (12 * 3600 / np.pi) * Gon * (
        np.cos(latitud_local_rad) * np.cos(ang_delta_rad) * (np.sin(ang_omega_f_rad) - np.sin(ang_omega_o_rad)) +
        (ang_omega_f_rad - ang_omega_o_rad) * np.sin(latitud_local_rad) * np.sin(ang_delta_rad)
    )

    return extraterrestrial_irradiance_hourly


if __name__ == '__main__':
    print(extraterrestrial_irradiance_hourly(30, 90, 50, 70, 20))
