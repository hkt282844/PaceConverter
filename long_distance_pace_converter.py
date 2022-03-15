from pace_converter_base_class import *
from helper import *

class LongDistancePaceConverter(PaceConverterBaseClass):
  """
  Responsible for printing and converting running splits for non-track running
  """
  def __init__(self, distance=0, hours=0, minutes=0, seconds=0, units='mi'):
    super().__init__(distance, units)
    self.hours = get_str_to_int(hours)
    self.minutes = get_str_to_int(minutes)
    self.seconds = get_str_to_int(seconds)
    self.assert_input()

    self.total_avg_pace_in_secs = 0
    self.set_average_pace()

  def assert_input(self):
    number_inputs_map = {'Distance':self.distance, 'Hours':self.hours, 'Minutes':self.minutes, 'Seconds':self.seconds}
    for key, value in number_inputs_map.items():
      assert_number(value, key)
    self.assert_units(self.average_pace_units)

  def get_input(self):
    return (self.distance, self.hours, self.minutes, self.seconds, self.average_pace_units)

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
      self.average_pace_units = units

    self.set_average_pace()

  def set_average_pace(self):
    self.total_avg_pace_in_secs = 0 if self.distance == 0 else get_average_pace_in_seconds(self.hours, self.minutes, self.seconds, self.distance)

  def convert_units(self):
    if self.average_pace_units == 'mi':
      self.distance = get_miles_to_km(self.distance)
      self.average_pace_units = 'km'
    elif self.average_pace_units == 'km':
      self.distance = get_km_to_miles(self.distance)
      self.average_pace_units = 'mi'
    else:
      raise Exception(self.average_pace_units + ' is not a valid unit!')

    self.set_average_pace()

  def get_splits(self):
    output = self.get_splits_per_distance(1, self.distance, self.total_avg_pace_in_secs, self.average_pace_units)
    return f'Splits:\n{output}'

  def get_average_pace(self):
    hours, minutes, seconds = roll_over_times(0, 0, round(self.total_avg_pace_in_secs))
    return f'Average Pace: {minutes}:{get_int_to_str(seconds)} min/{self.average_pace_units}'
