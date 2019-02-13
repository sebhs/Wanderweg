import React, { Component } from 'react';
import MapView from './MapView'
import InfoView from './InfoView'
import Grid from '@material-ui/core/Grid';
import selectedCountry from './../fakeData/italy.json';
import selectedCity from './../fakeData/rome.json';


const wrapperStyles = {
    width: "100%",
    maxWidth: "100%",
    margin: "0 auto",
}

class TripPlannerParent extends Component {

    constructor() {
        super();
        this.state = {
            tripPlan: {},
            selectedCity: selectedCity,
            cityMarkers: [],
        }
    }

    componentDidMount() {
        let cityMarkers = selectedCountry.cities.map((city, index) => {
            return {
                index: index,
                position: city.location,
                onClick: () => this.setToCurrentCity(index)

            }
        });
        console.log(cityMarkers);
        this.setState({ cityMarkers })
    }


    setToCurrentCity = function (index) {
        this.setState({
            selectedCity: selectedCountry.cities[index],
        })
    }




    render() {
        return (
            <div style={wrapperStyles}>
                <MapView cityMarker={this.state.cityMarkers} />
                <InfoView
                    selectedCity={this.state.selectedCity}
                />
            </div>
        );
    }
}

export default TripPlannerParent;
