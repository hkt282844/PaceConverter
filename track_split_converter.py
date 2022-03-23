from pace_converter_base_class import *
from helper import *

class TrackSplitConverter(PaceConverterBaseClass):
  """
  Responsible for printing and converting running splits for track running
  """
  def __init__(self):
    super().__init__()
    self.laps = ''
    self.avg_pace_mins = ''
    self.avg_pace_secs = ''
    self.lane_number = 1

  def get_input(self):
    return (self.distance, self.laps, self.avg_pace_mins, self.avg_pace_secs, self.average_pace_units, self.lane_number)

  def set_input(self, minutes, seconds, units, lane, distance='', laps=''):
    assert (distance != '') or (laps != ''), 'ERROR: distance and laps cannot both be empty!'

    if distance != '':
      distance = get_str_to_int(distance)
      assert_number(distance, 'Distance')
      self.distance = distance

    if laps != '' and self.distance == '':
      laps = get_str_to_int(laps)
      assert_number(laps, 'Laps')
      self.laps = laps

    minutes = get_str_to_int(minutes)
    assert_number(minutes, 'Minutes')
    self.avg_pace_mins = minutes

    seconds = get_str_to_int(seconds)
    assert_number(seconds, 'Seconds')
    self.avg_pace_secs = seconds

    units = get_units(units)
    self.assert_units(units)
    self.average_pace_units = units

    lane = 1 if lane == '' else get_str_to_int(lane)
    assert_number(lane, 'Lane')
    self.lane_number = lane

  def convert_units(self):
    if self.average_pace_units == 'm':
      return 1
    return get_miles_to_m(1) if self.average_pace_units == 'mi' else get_km_to_m(1)

  def convert_pace(self, split_distance):
    total_seconds = get_minutes_to_seconds(self.avg_pace_mins) + self.avg_pace_secs
    units_in_meters = self.convert_units()
    total_seconds /= units_in_meters
    total_seconds *= split_distance
    return total_seconds

  def get_track_splits_per_lap(self):
    split_units = 'laps'
    lap_distance = get_lap_distance(self.lane_number)

    lap_fraction = 1 / 2
    split_distance = lap_distance * lap_fraction
    total_split_pace_in_secs = self.convert_pace(split_distance)
    output = self.get_splits_per_distance(lap_fraction, lap_fraction, total_split_pace_in_secs, split_units)

    total_split_pace_in_secs = self.convert_pace(lap_distance)
    output += self.get_splits_per_distance(1, self.laps, total_split_pace_in_secs, split_units)

    return f'Splits:\n{output}'

  def get_track_splits_per_meters(self):
    avg_split_units = 'm'
    split_distance = 100
    total_split_pace_in_secs = self.convert_pace(split_distance)
    output = self.get_splits_per_distance(split_distance, 200, total_split_pace_in_secs, avg_split_units)

    split_distance = 400
    total_split_pace_in_secs = self.convert_pace(split_distance)
    output += self.get_splits_per_distance(split_distance, self.distance, total_split_pace_in_secs, avg_split_units)
    return f'Splits:\n{output}'

  def get_splits(self):
    if self.avg_pace_mins != '' and self.avg_pace_secs != '' and self.lane_number != '':
      return self.get_track_splits_per_lap() if self.lane_number > 1 else self.get_track_splits_per_meters()
    return ''

  def get_average_pace(self):
    if self.avg_pace_mins == '' or self.avg_pace_secs == '' or self.lane_number == '':
      return ''

    distance = self.distance if self.lane_number == 1 else get_lap_distance(self.lane_number) * self.laps
    total_converted_secs = self.convert_pace(distance)
    converted_hours, converted_minutes, converted_seconds = roll_over_times(0, 0, round(total_converted_secs))

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

    output += f'{distance}m' if self.lane_number == 1 else f'{self.laps} laps'
    return output
