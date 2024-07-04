def split_data_by_datetime(thermal_data, date_time):
  datohora = []
  datoradiacion = []
  datotamb = []
  datovviento = []

  for row in thermal_data:
    if date_time[0:10] in row['time'][0:10]:
      datohora.append(int(row['time'][11:13]))
      datoradiacion.append(row['G(i)'])
      datotamb.append(row['T2m'])
      datovviento.append(row['WS10m'])

  return datohora, datoradiacion, datotamb, datovviento
