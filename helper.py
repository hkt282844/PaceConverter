import math
import re

def get_seconds_to_minutes(seconds):
  return seconds / 60

def get_hours_to_seconds(hours):
  return get_minutes_to_seconds(get_hours_to_minutes(hours))

def get_minutes_to_seconds(minutes):
  return minutes * 60

def get_hours_to_minutes(hours):
  return hours * 60

def get_km_to_m(km):
  return km * 1000

def get_km_to_miles(km):
  return round(km / 1.60934, 2)

def get_miles_to_m(miles):
  km = get_miles_to_km(miles)
  return get_km_to_m(km)

def get_miles_to_km(miles):
  return round(miles * 1.60934, 2)

def get_str_to_int(string):
  try:
    value = float(string) if re.search(r'\.', string) else int(string)
  except:
    value = string
  return 0 if value == '' else value

def get_int_to_str(number):
  return f'0{number}' if number < 10 else f'{number}'

def get_lap_distance(lane):
  if lane == 1:
    return 400
  elif lane == 2:
    return 407.67
  elif lane == 3:
    return 415.33
  elif lane == 4:
    return 423
  elif lane == 5:
    return 430.66
  elif lane == 6:
    return 438.33
  elif lane == 7:
    return 446
  elif lane == 8:
    return 453.66
  elif lane == 9:
    return 461.33

def roll_over_times(hours, minutes, seconds):
  minutes += math.floor(seconds / 60)
  seconds %= 60

  hours += math.floor(minutes / 60)
  minutes %= 60
  return (hours, minutes, seconds)

def add_total_time(minutes_to_add, seconds_to_add, total_hours, total_minutes, total_seconds):
  total_minutes += minutes_to_add
  total_seconds += seconds_to_add
  return roll_over_times(total_hours, total_minutes, total_seconds)

def get_average_pace_in_seconds(hours, minutes, seconds, distance):
  total_seconds = get_hours_to_seconds(hours) + get_minutes_to_seconds(minutes) + seconds
  seconds_per_mile = total_seconds / distance
  return seconds_per_mile

def get_units(units):
  units = units.lower()
  if units == 'miles' or units == 'mile':
    units = 'mi'
  elif units == 'kilometers' or units == 'kilometer':
    units = 'km'
  elif units == 'meters' or units == 'meter':
    units = 'm'
  return units

def assert_number(number, name):
  assert isinstance(number, int) or isinstance(number, float), f'{name} must be a number!'

def assert_int(number, name):
  assert isinstance(number, int), f'{name} must be an integer!'
