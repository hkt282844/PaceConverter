import React, { useEffect, componentDidMount } from 'react';
import { form, select, label, Form, FormGroup, FormLabel, FormControl, Button as BButton } from 'react-bootstrap';
import axios from 'axios';
import '../css/index.css';

class Track extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      distance: '',
      laps: '',
      minutes: '',
      seconds: '',
      units: 'miles',
      lane: 1,
      track_pace: '',
      splits: []
    }
    this.updateDistance = this.updateDistance.bind(this);
    this.updateLaps = this.updateLaps.bind(this);
    this.updateMinutes = this.updateMinutes.bind(this);
    this.updateSeconds = this.updateSeconds.bind(this);
    this.updateUnits = this.updateUnits.bind(this);
    this.updateLane = this.updateLane.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.showDistance = this.showDistance.bind(this);
    this.showLaps = this.showLaps.bind(this);
  }

  updateDistance(event) {
    this.setState({
      distance: event.target.value
    });
  }

  updateLaps(event) {
    this.setState({
      laps: event.target.value
    })
  }

  updateMinutes(event) {
    this.setState({
      minutes: event.target.value
    })
  }

  updateSeconds(event) {
    this.setState({
      seconds: event.target.value
    })
  }

  updateUnits(event) {
    this.setState({
      units: event.target.value
    })
  }

  updateLane(event) {
    this.setState({
      lane: event.target.value
    })
  }

  componentDidMount() {
    fetch('/track/splits')
    .then(response => response.json())
    .then(data => this.setState({
      distance: data.distance,
      laps: data.laps,
      minutes: data.minutes,
      seconds: data.seconds,
      units: data.units,
      lane: data.lane,
      track_pace: data.track_pace,
      splits: data.splits
    }))
  };

  handleSubmit() {
    axios({
      method: 'post',
      url: '/track/splits',
      data: this.state})
  }

  showDistance() {
    if (this.state.lane == 1) {
      this.state.laps='';

      return (
        <FormGroup>
          <FormLabel className="InputLabel">Split Distance:</FormLabel>
          <FormControl type="text" name="distance" value={this.state.distance} placeholder="400" onChange={this.updateDistance} className="InputField" />
        </FormGroup>
      );
    }
    return null;
  }

  showLaps() {
    if (this.state.lane > 1) {
      this.state.distance='';

      return (
        <FormGroup>
          <FormLabel className="InputLabel">Laps:</FormLabel>
          <FormControl type="text" name="laps" value={this.state.laps} placeholder="0" onChange={this.updateLaps} className="InputField" />
        </FormGroup>
      );
    }
    return null;
  }

  render() {

    return (
      <div className="Track">

        <div className="Form">
          <form onSubmit={this.handleSubmit} action="/track" method="get">

            <FormGroup>
              <FormLabel className="LaneNumberLabel">Lane Number:</FormLabel>
              <select value={this.state.lane} onChange={this.updateLane} className="LaneNumberDropDown">
                <option disabled='true' value=''>Select</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
              </select>
            </FormGroup>

            <this.showDistance />

            <this.showLaps />

            <FormGroup>
              <FormLabel className="InputLabel">Pace Minutes:</FormLabel>
              <FormControl type="text" name="minutes" value={this.state.minutes} placeholder="10" onChange={this.updateMinutes} className="InputField" />
            </FormGroup>

            <FormGroup>
              <FormLabel className="InputLabel">Pace Seconds:</FormLabel>
              <FormControl type="text" name="seconds" value={this.state.seconds} placeholder="0" onChange={this.updateSeconds} className="InputField" />
            </FormGroup>

            <FormGroup>
              <FormLabel className="InputLabel">Pace Units:</FormLabel>
              <FormControl type="text" name="units" value={this.state.units} onChange={this.updateUnits} className="InputField" />
            </FormGroup>

            <input type="submit" value="Submit" className="SubmitButton" />
          </form>
        </div>

        <div>
          <label>{this.state.track_pace}</label>
          {this.state.splits.map( (item) => <div key={item}>{item}</div> )}
        </div>

      </div>
    );
  }
}

export default Track;
