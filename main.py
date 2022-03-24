import sqlite3
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import abort
from long_distance_pace_converter import *
from track_split_converter import *

def get_db_connection():
  connection = sqlite3.connect('database.db')
  connection.row_factory = sqlite3.Row
  return connection

def get_workout(day):
  connection = get_db_connection()
  workout = connection.execute('SELECT * FROM schedule WHERE day = ?',
                               (day,)).fetchone()
  connection.close()
  if workout is None:
    abort(404)
  return workout

app = Flask(__name__)

long_distance_pace_converter = LongDistancePaceConverter()
track_split_converter = TrackSplitConverter()

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    distance = request.form['distance']
    units = request.form['units']
    hours = request.form['hours']
    minutes = request.form['minutes']
    seconds = request.form['seconds']
    long_distance_pace_converter.set_input(distance, hours, minutes, seconds, units)
    average_pace = long_distance_pace_converter.get_average_pace()
    splits = long_distance_pace_converter.get_splits()
    splits = splits.split('\n')
    return render_template('index.html', distance=distance, units=units, hours=hours, minutes=minutes,
                           seconds=seconds, average_pace=average_pace, splits=splits)

  return render_template('index.html')

@app.route("/splits", methods=['GET', 'POST'])
def splits():
  if request.method == 'POST':
    data = request.get_json()
    distance = data['distance']
    units = data['units']
    hours = data['hours']
    minutes = data['minutes']
    seconds = data['seconds']
    long_distance_pace_converter.set_input(distance, hours, minutes, seconds, units)

    average_pace = long_distance_pace_converter.get_average_pace()
    splits = long_distance_pace_converter.get_splits()
    splits = splits.split('\n')

    data['average_pace'] = average_pace
    data['splits'] = splits
    return data

  distance, hours, minutes, seconds, units = long_distance_pace_converter.get_input()
  average_pace = long_distance_pace_converter.get_average_pace()
  splits = long_distance_pace_converter.get_splits()
  splits = splits.split('\n')

  data = {'distance':distance, 'hours':hours, 'minutes':minutes, 'seconds':seconds,
          'units':units, 'average_pace':average_pace, 'splits':splits}
  return data

@app.route("/convert", methods=['GET', 'POST'])
def convert():
  long_distance_pace_converter.convert_units()
  distance, hours, minutes, seconds, units = long_distance_pace_converter.get_input()

  average_pace = long_distance_pace_converter.get_average_pace()
  splits = long_distance_pace_converter.get_splits()
  splits = splits.split('\n')

  data = {'distance':distance, 'hours':hours, 'minutes':minutes, 'seconds':seconds,
          'units':units, 'average_pace':average_pace, 'splits':splits}
  return data

@app.route("/track", methods=['GET', 'POST'])
def track():
  if request.method == 'POST':
    request_data = request.get_json()
    distance = request_data['distance']
    laps = request_data['laps']
    minutes = request_data['minutes']
    seconds = request_data['seconds']
    units = request_data['units']
    lane = request_data['lane']
    track_split_converter.set_input(minutes, seconds, units, lane, distance, laps)
    track_pace = track_split_converter.get_average_pace()
    data = request_data
    data['track_pace'] = track_pace
    return data

  else:
    distance, laps, minutes, seconds, units, lane = track_split_converter.get_input()

  track_pace = track_split_converter.get_average_pace()
  splits = track_split_converter.get_splits()
  splits = splits.split('\n')
  return render_template('track.html', distance=distance, laps=laps, minutes=minutes, seconds=seconds,
                         units=units, lane=lane, track_pace=track_pace, splits=splits)

@app.route("/track/splits", methods=['GET', 'POST'])
def track_splits():
  if request.method == 'POST':
    data = request.get_json()
    distance = data['distance']
    laps = data['laps']
    minutes = data['minutes']
    seconds = data['seconds']
    units = data['units']
    lane = data['lane']
    track_split_converter.set_input(minutes, seconds, units, lane, distance, laps)

    track_pace = track_split_converter.get_average_pace()
    splits = track_split_converter.get_splits()
    splits = splits.split('\n')

    data['track_pace'] = track_pace
    data['splits'] = splits
    return data

  distance, laps, minutes, seconds, units, lane = track_split_converter.get_input()
  track_pace = track_split_converter.get_average_pace()
  splits = track_split_converter.get_splits()
  splits = splits.split('\n')

  data = {'distance':distance, 'laps':laps, 'minutes':minutes, 'seconds':seconds,
          'units':units, 'lane':lane, 'track_pace':track_pace, 'splits':splits}
  return data

@app.route("/schedule", methods=['GET', 'POST'])
def schedule():
  connection = get_db_connection()
  schedule = connection.execute('SELECT * FROM schedule').fetchall()
  connection.close()
  return render_template('schedule.html', schedule=schedule)

@app.route('/schedule/<string:day>')
def workout(day):
  workout = get_workout(day)
  return render_template('workout.html', workout=workout)

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
