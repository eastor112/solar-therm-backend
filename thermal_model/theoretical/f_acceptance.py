import numpy as np

def acceptance_function(D_int, D_ext, S_sep, ang_omega):
    """
    Calculate the acceptance function between tube spacing.

    Parameters:
    - D_int (float): Internal diameter [m].
    - D_ext (float): External diameter [m].
    - S_sep (float): Distance between tube centers [m].
    - ang_OMEGA (float): Angle OMEGA [deg].

    Returns:
    - acceptance_function (float): Acceptance function between tube spacing.
    """
    # Calculate critical angles OMEGA_0 and OMEGA_1
    OMEGA_0 = np.degrees(np.arccos((D_int + D_ext) / (2 * S_sep)))  # Greater critical angle [deg]
    OMEGA_1 = np.degrees(np.arccos((D_int - D_ext) / (2 * S_sep)))  # Smaller critical angle [deg]

    # Find the acceptance function
    if ang_omega <= OMEGA_0:
        acceptance_function = 1
    elif OMEGA_0 < ang_omega <= OMEGA_1:
        acceptance_function = (S_sep / D_int) * np.cos(np.radians(ang_omega)) + 0.5 * (1 - (D_ext / D_int))
    else:
        acceptance_function = 0

    return acceptance_function


if __name__ == '__main__':
    print(acceptance_function(0.5, 0.5, 0.5, 10))
