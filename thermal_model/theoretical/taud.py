def diffuse_transmissivity(tau_b):
    """
    Calculate the diffuse transmissivity of the atmosphere.

    Parameters:
    - tau_b (float): Beam transmissivity of the atmosphere.

    Returns:
    - diffuse_transmissivity (float): Diffuse transmissivity of the atmosphere.
    """
    diffuse_transmissivity = 0.271 - 0.294 * tau_b  # Diffuse transmissivity of the atmosphere

    return diffuse_transmissivity

if __name__ == '__main__':
    print(diffuse_transmissivity(50))
