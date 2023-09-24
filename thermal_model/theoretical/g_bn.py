def beam_radiation(g_on, tau_b):
    """
    Calculate beam radiation in the direction of the sun.

    Parameters:
    - g_on (float): Direct normal radiation [W/m2].
    - tau_b (float): Sky transmissivity [-].

    Returns:
    - beam_radiation (float): Beam radiation in the direction of the sun [W/m2].
    """
    beam_radiation = g_on * tau_b  # Beam radiation in the direction of the sun [W/m2] (Duffie & Beckam, 2020)

    return beam_radiation

if __name__ == '__main__':
    print(beam_radiation(10,  3))
