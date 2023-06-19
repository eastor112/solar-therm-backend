import pandas as pd
from datetime import datetime
import pytz
from backend.database import SessionFactory
from models import Weather
from sqlalchemy.exc import SQLAlchemyError

session = SessionFactory()


def format_date(date):
  date_str = date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
  return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.UTC)


data = pd.read_csv("data/tidy.csv")
data['date'] = pd.to_datetime(data['date'])
data['date'] = data['date'].apply(format_date)
data_dict = data.to_dict(orient='records')

weather_objects = []
for row in data_dict:
  # Transformar los nombres de columna antes de asignar los valores a los atributos
  weather_obj = Weather()
  for key, value in row.items():
    setattr(weather_obj, key.replace(' ', '_').lower(), value)
  weather_objects.append(weather_obj)

try:
  # Insertar los objetos Weather en la base de datos en una operación de bulk insert
  session.add_all(weather_objects)
  session.commit()
  print("Los datos se han guardado correctamente en la base de datos.")
except SQLAlchemyError as e:
  session.rollback()
  print("Error al guardar los datos en la base de datos:", str(e))
finally:
  session.close()
