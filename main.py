from flask import Flask, render_template, request
from pace_converter import *

app = Flask(__name__)

pace_converter = PaceConverter()
track_split_converter = TrackSplitConverter()

@app.route("/", methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    distance = request.form['distance']
    units = request.form['units']
    hours = request.form['hours']
    minutes = request.form['minutes']
    seconds = request.form['seconds']
    pace_converter.set_input(distance, hours, minutes, seconds, units)
    average_pace = pace_converter.get_average_pace()
    splits = pace_converter.get_splits()
    splits = splits.split('\n')
    return render_template('index.html', distance=distance, units=units, hours=hours, minutes=minutes,
                           seconds=seconds, average_pace=average_pace, splits=splits)

  return render_template('index.html')

@app.route("/convert", methods=['GET', 'POST'])
def convert():
  if request.method == 'POST':
    pace_converter.convert_units()
    distance, hours, minutes, seconds, units = pace_converter.get_input()
    average_pace = pace_converter.get_average_pace()
    splits = pace_converter.get_splits()
    splits = splits.split('\n')
    return render_template('index.html', distance=distance, units=units, hours=hours, minutes=minutes,
                           seconds=seconds, average_pace=average_pace, splits=splits)

  return render_template('index.html')

@app.route("/track", methods=['GET', 'POST'])
def track():
  if request.method == 'POST':
    distance = request.form['distance']
    laps = request.form['laps']
    minutes = request.form['minutes']
    seconds = request.form['seconds']
    units = request.form['units']
    lane = request.form['lane']

    track_split_converter.set_input(distance, laps, minutes, seconds, units, lane)
    track_pace = track_split_converter.get_track_pace()
    splits = track_split_converter.get_track_splits()
    splits = splits.split('\n')
    return render_template('track.html', distance=distance, laps=laps, minutes=minutes, seconds=seconds,
                           units=units, lane=lane, track_pace=track_pace, splits=splits)

  return render_template('track.html')

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
