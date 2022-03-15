from helper import *

class LongDistancePaceConverter:
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
