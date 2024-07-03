import csv
import numpy as np


def dato_clima_diario(anho, mes, dia, data=[]):
  # file_path = 'TRUJILLO_2022.csv'
  # data = []

  # with open(file_path, newline='') as csvfile:
  #   csvreader = csv.reader(csvfile, delimiter=',')

  #   headers = next(csvreader, None)

  #   for row in csvreader:
  #     data.append(row)

  # data_array = np.array(data)

  datohora = []
  datoradiacion = []
  datotamb = []
  datovviento = []

  for row in data:
    if int(row[0]) == anho and int(row[1]) == mes and int(row[2]) == dia:
      datohora.append(float(row[3]))
      datoradiacion.append(float(row[4]))
      datotamb.append(float(row[5]))
      datovviento.append(float(row[6]))

  return np.array(datohora), np.array(datoradiacion), np.array(datotamb), np.array(datovviento)
