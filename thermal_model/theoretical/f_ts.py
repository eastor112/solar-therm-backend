import numpy as np

def diffuse_radiation_shape_function(D_int, D_ext, S_sep):
    """
    Calculate the shape function for diffuse radiation.

    Parameters:
    - D_int (float): Internal diameter [m].
    - D_ext (float): External diameter [m].
    - S_sep (float): Distance between tube centers [m].

    Returns:
    - diffuse_radiation_shape_function (float): Shape function for diffuse radiation.
    """
    # Calculate critical angles OMEGA_0 and OMEGA_1
    OMEGA_0 = np.degrees(np.arccos((D_int + D_ext) / (2 * S_sep)))  # Greater critical angle [deg]
    OMEGA_1 = np.degrees(np.arccos((D_int - D_ext) / (2 * S_sep)))  # Smaller critical angle [deg]

    # Find the shape function for diffuse radiation
    diffuse_radiation_shape_function = (
        (OMEGA_0 * np.pi / 180 + 0.5 * (1 - (D_ext / D_int)) * (OMEGA_1 * np.pi / 180 - OMEGA_0 * np.pi / 180) +
         (S_sep / D_int) * (np.sin(np.radians(OMEGA_1)) - np.sin(np.radians(OMEGA_0))))
    ) / np.pi  # Shape function for diffuse radiation

    return diffuse_radiation_shape_function


if __name__ == '__main__':
    print(diffuse_radiation_shape_function(0.5, 0.5, 10))
