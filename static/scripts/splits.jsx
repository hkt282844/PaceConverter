import React, { useEffect, componentDidMount } from 'react';
import { form, select, label, Form, FormGroup, FormLabel, FormControl, Button as BButton } from 'react-bootstrap';
import axios from 'axios';
import '../css/index.css';

class Splits extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      distance: '',
      units: 'miles',
      hours: '',
      minutes: '',
      seconds: '',
      average_pace: '',
      splits: []
    }
    this.updateDistance = this.updateDistance.bind(this);
    this.updateUnits = this.updateUnits.bind(this);
    this.updateHours = this.updateHours.bind(this);
    this.updateMinutes = this.updateMinutes.bind(this);
    this.updateSeconds = this.updateSeconds.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  updateDistance(event) {
    this.setState({
      distance: event.target.value
    });
  }

  updateUnits(event) {
    this.setState({
      units: event.target.value
    })
  }

  updateHours(event) {
    this.setState({
      hours: event.target.value
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

  componentDidMount() {
    fetch('/splits')
    .then(response => response.json())
    .then(data => this.setState({
      distance: data.distance,
      units: data.units,
      minutes: data.minutes,
      seconds: data.seconds,
      average_pace: data.average_pace,
      splits: data.splits
    }))
  };

  handleSubmit() {
    axios({
      method: 'post',
      url: '/splits',
      data: this.state})
  }

  render() {

    return (
      <div className="Track">

        <div className="Form">
          <form onSubmit={this.handleSubmit} action="/" method="get">

            <FormGroup>
              <FormLabel className="InputLabel">Total Distance:</FormLabel>
              <FormControl type="text" name="distance" value={this.state.distance} placeholder="3" onChange={this.updateDistance} className="InputField" />
            </FormGroup>

            <FormGroup>
              <FormLabel className="InputLabel">Units:</FormLabel>
              <FormControl type="text" name="units" value={this.state.units} onChange={this.updateUnits} className="InputField" />
            </FormGroup>

            <FormGroup>
              <FormLabel className="InputLabel">Total Hours:</FormLabel>
              <FormControl type="text" name="hours" value={this.state.hours} placeholder="0" onChange={this.updateHours} className="InputField" />
            </FormGroup>

            <FormGroup>
              <FormLabel className="InputLabel">Total Minutes:</FormLabel>
              <FormControl type="text" name="minutes" value={this.state.minutes} placeholder="30" onChange={this.updateMinutes} className="InputField" />
            </FormGroup>

            <FormGroup>
              <FormLabel className="InputLabel">Total Seconds:</FormLabel>
              <FormControl type="text" name="seconds" value={this.state.seconds} placeholder="0" onChange={this.updateSeconds} className="InputField" />
            </FormGroup>

            <input type="submit" value="Submit" className="SubmitButton" />
          </form>
        </div>

        <div>
          <label>{this.state.average_pace}</label>
          {this.state.splits.map( (item) => <li key={item}>{item}</li> )}
        </div>

      </div>
    );
  }
}

export default Splits;
