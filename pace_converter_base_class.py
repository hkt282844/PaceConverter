from helper import *

class PaceConverterBaseClass:
  """
  Base class for other pace converter classes
  """
  def __init__(self):
    self.distance = ''
    self.average_pace_units = 'miles'

  def assert_units(self, units):
    assert units == 'mi' or units == 'km' or units == 'm', 'Units must either be miles, kilometers, or meters!'

  def set_average_pace(self):
    self.averge_pace_minutes, self.average_pace_seconds = get_average_pace(self.hours, self.minutes, self.seconds, self.distance)

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

  def get_splits_per_distance(self, split_distance, total_distance, total_split_pace_in_secs, split_units):
    curr_distance = split_distance
    total_hours, total_minutes, total_seconds = 0, 0, 0
    output = ''
    while curr_distance <= total_distance:
      total_hours, total_minutes, total_seconds = add_total_time(0, total_split_pace_in_secs, total_hours, total_minutes, total_seconds)
      output += f'{self.get_split(split_units, curr_distance, total_hours, total_minutes, total_seconds)}\n'
      curr_distance += split_distance

    remaining_distance = total_distance % split_distance
    if remaining_distance > 0:
      total_seconds = (total_split_pace_in_secs / split_distance) * total_distance

      total_hours, total_minutes, total_seconds = add_total_time(0, total_seconds, 0, 0, 0)
      output += f'{self.get_split(split_units, total_distance, total_hours, total_minutes, total_seconds)}\n'

    return output

  def get_splits(self):
    raise NotImplementedError

  def get_average_pace(self):
    raise NotImplementedError

  def print_splits(self):
    print(self.get_splits())

  def print_average_pace(self):
    print(self.get_average_pace())
