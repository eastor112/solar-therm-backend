import numpy as np


def daily_extraterrestrial_irradiance(g_on, latitud_local, ang_delta, ang_omega_s):
    """
    Calculate the daily extraterrestrial horizontal irradiance [J/m2 day].

    Parameters:
    - Gon (float): Extraterrestrial radiation [W/m2].
    - latitud_local (float): Local latitude [deg].
    - ang_delta (float): Declination angle [deg].
    - ang_omega_s (float): Hour angle at sunset [deg].

    Returns:
    - daily_extraterrestrial_irradiance (float): Daily extraterrestrial horizontal irradiance [J/m2 day].
    """
    latitud_local_rad = np.deg2rad(latitud_local)
    ang_delta_rad = np.deg2rad(ang_delta)
    ang_omega_s_rad = np.deg2rad(ang_omega_s)

    daily_extraterrestrial_irradiance = (24 * 3600 / np.pi) * g_on * (
        np.cos(latitud_local_rad) * np.cos(ang_delta_rad) * np.sin(ang_omega_s_rad) +
        (ang_omega_s_rad) *
        np.sin(latitud_local_rad) * np.sin(ang_delta_rad)
    )


    return daily_extraterrestrial_irradiance


if __name__ == '__main__':
    print(daily_extraterrestrial_irradiance(30, 90, 100, 70))
