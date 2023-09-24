import numpy as np

def omega_angle(nn_x, nn_y):
    """
    Calculate the OMEGA angle.

    Parameters:
    - nn_x (float): Normal direction to the inclined plane.
    - nn_y (float): Direction from east to south.

    Returns:
    - omega_angle (float): The OMEGA angle [degrees].
    """
    if(nn_x>0.0000000001):
        omega_angle = abs(np.arctan(nn_y / nn_x))
    else:
        omega_angle = abs(np.arctan(nn_y / 0.0000000001))

    return np.degrees(omega_angle)

if __name__ == '__main__':
    print(omega_angle(12, 2))
