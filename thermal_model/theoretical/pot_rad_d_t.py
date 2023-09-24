import numpy as np

def diffuse_radiant_power(g_d_beta, d_int, l_tubo, f_form):
    """
    Calculate the diffuse radiant power in 1 vacuum tube [W].

    Parameters:
    - Gdbeta (float): Diffuse radiation with sun direction [W/m2].
    - D_int (float): Internal diameter [m].
    - L_tubo (float): Effective length of the tube [m].
    - F_form (float): Shape function for diffuse radiation [-].

    Returns:
    - radiant_power_diffuse (float): Diffuse radiant power in 1 vacuum tube [W].
    """
    radiant_power_diffuse = d_int * l_tubo * np.pi * g_d_beta * f_form

    return radiant_power_diffuse

if __name__ == '__main__':
    print(diffuse_radiant_power(50, 0.3, 2, 60))
