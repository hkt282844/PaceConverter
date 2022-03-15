from helper import *

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
