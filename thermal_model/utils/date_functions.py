from datetime import datetime


def split_date(date_time):
  date_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M')

  year = date_obj.year
  month = date_obj.month
  day = date_obj.day
  hour = date_obj.hour
  minutes = date_obj.minute

  return year, month, day, hour, minutes
