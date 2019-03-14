import React, { Component } from 'react';
import TripPlannerParent from './TripPlanning/TripPlannerParent'
import TransportPlannerParent from './TransportPlanning/TransportPlannerParent'


class App extends Component {
  render() {
    return (
      // <TripPlannerParent />
      <TransportPlannerParent/>
    );
  }
}

export default App;
