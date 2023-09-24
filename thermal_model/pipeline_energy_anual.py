import numpy as np
from thermal_model.pipeline_energy_day import get_pipe_energy


def calculate_annual_energy(
    local_longitude,
    local_latitude,
    local_height,
    inclination,
    azimuth,
    internal_diameter,
    external_diameter,
    pipeline_length,
    pipeline_separation,
    granularity
):
  """
  Calcula la energía anual aprovechada por un colector solar.

  Args:
      local_longitude (float): Longitud geográfica local en grados.
      local_latitude (float): Latitud geográfica local en grados.
      local_altitude (float): Altitud local en metros.
      inclination (float): Ángulo de inclinación del colector en grados.
      azimuth (float): Ángulo de azimuth del colector en grados.
      inner_diameter (float): Diámetro interno del tubo al vacío en metros.
      outer_diameter (float): Diámetro externo del tubo al vacío en metros.
      pipeline_length (float): Longitud efectiva del tubo al vacío expuesto al sol en metros.
      pipeline_separation (float): Distancia de separación entre centro de tubos en metros.
      granularity (int): División de puntos que abarca todo el día.

  Returns:
      float: Energía anual aprovechada en kWh.
  """

  energia_diaria = np.zeros(365)

  for day in range(1, 366):
    energia_diaria[day - 1] = get_pipe_energy(
        day,
        local_latitude,
        inclination,
        azimuth,
        local_longitude,
        granularity,
        local_height,
        internal_diameter,
        external_diameter,
        pipeline_separation,
        pipeline_length
    )

  energia_anual = np.sum(energia_diaria)

  return energia_anual, energia_diaria
