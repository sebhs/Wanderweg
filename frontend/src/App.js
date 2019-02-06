import React, { Component } from 'react';
import TripPlannerParent from './TripPlanning/TripPlannerParent'

import {
  ComposableMap,
  ZoomableGroup,
  Geographies,
  Geography,
} from "react-simple-maps"



class App extends Component {
  render() {
    return (
      <TripPlannerParent />
    );
  }
}

export default App;
