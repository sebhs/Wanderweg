import React, { Component } from 'react';
import TripPlannerParent from './TripPlanning/TripPlannerParent'
import TransportPlannerParent from './TransportPlanning/TransportPlannerParent'
import TripItineraryParent from './TripItinerary/TripItineraryParent'


class App extends Component {

  constructor() {
    super();
    this.state = {
      tripPlan: [],
      displayTripPlanner: true,
      displayItinerary: false,
    }
  }
  setTrip = function (tripPlan, startDate) {

    this.setState({ tripPlan, startDate, displayTripPlanner: false })
  }
  finishedPlanning = function(transport, tripPlan) {
    this.setState({ tripPlan, transport, displayItinerary: true })
  }

  render() {
    return (
      <div>
        {this.state.displayTripPlanner ? (
          <TripPlannerParent
            setTrip={this.setTrip.bind(this)}
          />
        ) : (
          <div>
          {this.state.displayItinerary ? (
            <TripItineraryParent
            tripPlan={this.state.tripPlan}
            transport={this.state.transport}
            />
          ) : (
            <TransportPlannerParent
            tripPlan={this.state.tripPlan}
            startDate={this.state.startDate}
            finishedPlanning={this.finishedPlanning.bind(this)}
          />
            )}
        </div>

          )}
          
      </div>
    );
  }
}

export default App;
