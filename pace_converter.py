"""
TODOS:
1. Create base class for classes to inheret from.
2. Move helper functions to own file.
3. Move classes to own files.
4. Clean up long, messy, repetitive functions.
"""

import math
import re

def get_seconds_to_minutes(seconds):
  return seconds / 60

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
  return value

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

def get_average_pace(hours, minutes, seconds, distance):
  total_seconds = get_minutes_to_seconds(get_hours_to_minutes(hours)) + get_minutes_to_seconds(minutes) + seconds
  seconds_per_mile = total_seconds / distance
  total_minutes = get_seconds_to_minutes(seconds_per_mile)
  whole_minutes = math.floor(total_minutes)
  seconds = get_minutes_to_seconds(total_minutes - whole_minutes)
  return (whole_minutes, seconds)

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


class TrackSplitConverter:
  """
  Responsible for printing and converting running splits for track running
  """
  def __init__(self, distance=0, laps=0, minutes=0, seconds=0, units='mi', lane=1):
    """
    split_distance: units are assumed to be in meters for track running
    """
    self.distance = get_str_to_int(distance)
    self.laps = 0 if self.distance else get_str_to_int(laps)
    self.minutes = get_str_to_int(minutes)
    self.seconds = get_str_to_int(seconds)
    self.units = get_units(units)
    self.lane = get_str_to_int(lane)
    self.assert_input()

  def assert_input(self):
    number_inputs_map = {'Distance':self.distance, 'Laps':self.laps, 'Minutes':self.minutes, 'Seconds':self.seconds, 'Lane':self.lane}
    for key, value in number_inputs_map.items():
      assert_number(value, key)
    self.assert_units(self.units)

  def assert_units(self, units):
    assert units == 'mi' or units == 'km' or units == 'm', 'Units must either be miles, kilometers, or meters!'

  def get_input(self):
    return (self.distance, self.laps, self.minutes, self.seconds, self.units, self.lane)

  def set_input(self, distance=None, laps=None, minutes=None, seconds=None, units=None, lane=None):
    if distance is not None and distance != '':
      distance = get_str_to_int(distance)
      assert_number(distance, 'Distance')
      self.distance = distance
    if laps is not None and laps != '' and self.distance == 0:
      laps = get_str_to_int(laps)
      assert_number(laps, 'Laps')
      self.laps = laps
    if minutes is not None:
      minutes = get_str_to_int(minutes)
      assert_number(minutes, 'Minutes')
      self.minutes = minutes
    if seconds is not None:
      seconds = get_str_to_int(seconds)
      assert_number(seconds, 'Seconds')
      self.seconds = seconds
    if units is not None:
      units = get_units(units)
      self.assert_units(units)
      self.units = units
    if lane == '':
      lane = 1
    if lane is not None:
      lane = get_str_to_int(lane)
      assert_number(lane, 'Lane')
      self.lane = lane

  def convert_units(self):
    if self.units == 'm':
      return 1
    return get_miles_to_m(1) if self.units == 'mi' else get_km_to_m(1)

  def convert_pace(self, split_distance):
    total_seconds = get_minutes_to_seconds(self.minutes) + self.seconds
    units_in_meters = self.convert_units()
    total_seconds /= units_in_meters
    total_seconds *= split_distance
    return roll_over_times(0, 0, round(total_seconds))

  def get_split(self, units, distance, hours, minutes, seconds, lap_number_str=None):
    hours, minutes, seconds = roll_over_times(hours, minutes, round(seconds))
    output = f'{distance} {units}: ' if self.lane == 1 else f'{lap_number_str} lap: '
    time_units = 'sec'
    if hours > 0:
      output += f'{hours}:'
      time_units = 'hr'
    if hours > 0 or minutes > 0:
      output += get_int_to_str(minutes) if hours > 0 else f'{minutes}'
      output += ':'
      time_units = 'min'
    output += get_int_to_str(seconds) if (minutes > 0 or hours > 0) else f'{seconds}'
    output += f' {time_units}'
    return output

  def get_track_splits_per_lap(self):
    print(self.laps)
    output = ''
    units = 'm'
    lap_distance = get_lap_distance(self.lane)

    # Get time for first 1/2 lap
    lap_fraction = 1 / 2
    split_distance = lap_distance * lap_fraction
    hours, minutes, seconds = self.convert_pace(split_distance)

    curr_lap = lap_fraction
    total_hours, total_minutes, total_seconds = 0, 0, 0
    total_hours, total_minutes, total_seconds = add_total_time(minutes, seconds, hours, total_minutes, total_seconds)
    output += f'{self.get_split(units, round(split_distance), total_hours, total_minutes, total_seconds, curr_lap)}\n'

    # Get times per full laps
    hours, minutes, seconds = self.convert_pace(lap_distance)
    curr_lap = 1
    curr_distance = lap_distance
    total_hours, total_minutes, total_seconds = 0, 0, 0
    while curr_lap <= self.laps:
      print(f'curr_lap: {curr_lap}')
      print(f'self.laps: {self.laps}')
      total_hours, total_minutes, total_seconds = add_total_time(minutes, seconds, hours, total_minutes, total_seconds)
      output += f'{self.get_split(units, round(curr_distance), total_hours, total_minutes, total_seconds, curr_lap)}\n'

      curr_distance += lap_distance
      curr_lap += 1

    return f'Splits:\n{output}'

  def get_track_splits_per_meters(self):
    output = ''

    units = 'm'
    split_distance = 100
    hours, minutes, seconds = self.convert_pace(split_distance)
    curr_distance = split_distance
    total_hours, total_minutes, total_seconds = 0, 0, 0

    while curr_distance < 200:
      print(f'curr_distance: {curr_distance}')
      total_hours, total_minutes, total_seconds = add_total_time(minutes, seconds, hours, total_minutes, total_seconds)
      output += f'{self.get_split(units, round(curr_distance), total_hours, total_minutes, total_seconds)}\n'

      curr_distance += split_distance

    total_hours, total_minutes, total_seconds = add_total_time(minutes, seconds, hours, total_minutes, total_seconds)
    output += f'{self.get_split(units, round(curr_distance), total_hours, total_minutes, total_seconds)}\n'

    split_distance = 400
    hours, minutes, seconds = self.convert_pace(split_distance)
    curr_distance = split_distance
    total_hours, total_minutes, total_seconds = 0, 0, 0
    while curr_distance <= self.distance:
      print(f'curr_distance: {curr_distance}')
      total_hours, total_minutes, total_seconds = add_total_time(minutes, seconds, hours, total_minutes, total_seconds)
      output += f'{self.get_split(units, round(curr_distance), total_hours, total_minutes, total_seconds)}\n'

      curr_distance += split_distance

    remaining_distance = self.distance % split_distance
    if remaining_distance > 0:
      hrs_remaining_distance, min_remaining_distance, sec_remaining_distance = self.convert_pace(remaining_distance)
      remaining_seconds = sec_remaining_distance + get_minutes_to_seconds(min_remaining_distance)

      total_hours, total_minutes, total_seconds = add_total_time(0, remaining_seconds, total_hours, total_minutes, total_seconds)
      output += f'{self.get_split(units, self.distance, total_hours, total_minutes, total_seconds)}\n'

    return f'Splits:\n{output}'

  def get_track_splits(self):
    return self.get_track_splits_per_lap() if self.lane > 1 else self.get_track_splits_per_meters()

  def get_track_pace(self):
    distance = self.distance if self.lane == 1 else get_lap_distance(self.lane) * self.laps
    converted_hours, converted_minutes, converted_seconds = self.convert_pace(distance)

    output = 'Average Track Pace: '
    if converted_hours > 0:
      output += f'{converted_hours}:'
    if converted_minutes:
      output += f'{converted_minutes}:'
    output += f'{get_int_to_str(converted_seconds)}' if converted_minutes > 0 else f'{converted_seconds}'

    if converted_hours > 0:
      output += f' hr / '
    elif converted_minutes > 0:
      output += f' min / '
    else:
      output += f' sec / '

    output += f'{distance}m' if self.lane == 1 else f'{self.laps} laps'

  def print_track_splits(self):
    print(self.get_track_splits())

  def print_average_track_pace(self):
    print(self.get_track_pace())


class PaceConverter:
  """
  Responsible for printing and converting running splits
  """
  def __init__(self, distance=0, hours=0, minutes=0, seconds=0, units='mi'):
    """
    split_distance: units are assumed to be in meters for track running
    """
    self.distance = get_str_to_int(distance)
    self.hours = get_str_to_int(hours)
    self.minutes = get_str_to_int(minutes)
    self.seconds = get_str_to_int(seconds)
    self.units = get_units(units)
    self.assert_input()
    self.averge_pace_minutes, self.average_pace_seconds = 0, 0

  def assert_units(self, units):
    assert units == 'mi' or units == 'km', 'Units must either be miles or kilometers!'

  def assert_input(self):
    number_inputs_map = {'Distance':self.distance, 'Hours':self.hours, 'Minutes':self.minutes, 'Seconds':self.seconds}
    for key, value in number_inputs_map.items():
      assert_number(value, key)
    self.assert_units(self.units)

  def get_input(self):
    return (self.distance, self.hours, self.minutes, self.seconds, self.units)

  def set_input(self, distance=None, hours=None, minutes=None, seconds=None, units=None):
    if distance is not None:
      distance = get_str_to_int(distance)
      assert_number(distance, 'Distance')
      self.distance = distance
    if hours is not None:
      hours = get_str_to_int(hours)
      assert_number(hours, 'Hours')
      self.hours = hours
    if minutes is not None:
      minutes = get_str_to_int(minutes)
      assert_number(minutes, 'Minutes')
      self.minutes = minutes
    if seconds is not None:
      seconds = get_str_to_int(seconds)
      assert_number(seconds, 'Seconds')
      self.seconds = seconds
    if units is not None:
      units = get_units(units)
      self.assert_units(units)
      self.units = units

    self.set_average_pace()

  def set_average_pace(self):
    self.averge_pace_minutes, self.average_pace_seconds = get_average_pace(self.hours, self.minutes, self.seconds, self.distance)

  def convert_units(self):
    if self.units == 'mi':
      self.distance = get_miles_to_km(self.distance)
      self.units = 'km'
    elif self.units == 'km':
      self.distance = get_km_to_miles(self.distance)
      self.units = 'mi'
    else:
      raise Exception(self.units + ' is not a valid unit!')

    self.set_average_pace()

  def get_split(self, units, distance, hours, minutes, seconds):
    hours, minutes, seconds = roll_over_times(hours, minutes, round(seconds))
    output = f'{distance} {units}: '
    time_units = 'sec'
    if hours > 0:
      output += f'{hours}:'
      time_units = 'hr'
    if hours > 0 or minutes > 0:
      output += get_int_to_str(minutes) if hours > 0 else f'{minutes}'
      output += ':'
      time_units = 'min'
    output += get_int_to_str(seconds) if (minutes > 0 or hours > 0) else f'{seconds}'
    output += f' {time_units}'
    return output

  def get_splits(self):
    curr_distance = 1
    total_hours, total_minutes, total_seconds = 0, 0, 0
    output = ''
    while curr_distance <= self.distance:
      total_hours, total_minutes, total_seconds = add_total_time(self.averge_pace_minutes, self.average_pace_seconds,
                                                                 total_hours, total_minutes, total_seconds)
      output += f'{self.get_split(self.units, curr_distance, total_hours, total_minutes, total_seconds)}\n'
      curr_distance += 1

    remaining_distance = self.distance % 1
    if remaining_distance > 0:
      avg_pace_in_seconds = self.average_pace_seconds + get_minutes_to_seconds(self.averge_pace_minutes)
      remaining_seconds = avg_pace_in_seconds * remaining_distance

      total_hours, total_minutes, total_seconds = add_total_time(0, remaining_seconds, total_hours, total_minutes, total_seconds)
      output += f'{self.get_split(self.units, self.distance, total_hours, total_minutes, total_seconds)}\n'

    return f'Splits:\n{output}'

  def get_average_pace(self):
    hours, minutes, seconds = roll_over_times(0, self.averge_pace_minutes, round(self.average_pace_seconds))
    return f'Average Pace: {minutes}:{get_int_to_str(seconds)} min/{self.units}'

  def print_splits(self):
    print(self.get_splits())

  def print_average_pace(self):
    print(self.get_average_pace())
