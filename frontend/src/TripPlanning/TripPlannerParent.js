import React, { Component } from 'react';
import MapView from './MapView'
import InfoView from './InfoView'
import Grid from '@material-ui/core/Grid';
import { cities } from './../fakeData/cities.json';

import milan from './../fakeData/milan.json';
import rome from './../fakeData/rome.json';
import florence from './../fakeData/florence.json';

const wrapperStyles = {
    width: "100%",
    maxWidth: "100%",
    margin: "0 auto",
}

class TripPlannerParent extends Component {

    constructor() {
        super();
        this.state = {
            tripPlan: [],
            polylinePath: [],
            selectedCity: cities[0],
            currentCityIndex: -1,
            cityMarkers: [],
            cityLoaded: false,
            cityInfo:rome
        }
    }

    componentDidMount() {
        let cityMarkers = cities.map((city, index) => {
            return {
                index: index,
                city_id:city.id,
                position: city.location,
                onClick: () => this.setToCurrentCity(index)
            }
        });
        this.setState({ cityMarkers })
        this.fetchCity()
    }

    fetchCity() {
        this.setState({cityLoaded: false})
        const {selectedCity} = this.state
        let city = selectedCity.id === rome.id ? rome : milan;
        city = selectedCity.id === florence.id ? florence : city;
        this.setState({
            cityInfo: city,
            cityLoaded: true
        })  
    }


    setToCurrentCity = function (index) {
        this.setState({
            selectedCity: cities[index],
            currentCityIndex: index
        })
        this.fetchCity();

    }

    addToTrip = function () {
        if (this.state.currentCityIndex > -1) {
            // let tmpPolyline = this.state.polylinePath;
            // let tmpPlan = this.state.tripPlan;
            // tmpPolyline.push(cities[this.state.currentCityIndex].location);
            const city_id = cities[this.state.currentCityIndex].id;
            const crd = cities[this.state.currentCityIndex].location;
            // this.setState({
            //     tripPlan: tmpPlan,
            //     polylinePath: tmpPolyline,
            // })
            this.setState({
                polylinePath:[...this.state.polylinePath, crd],
                tripPlan: [...this.state.tripPlan,city_id ],
            })
        }
    }




    render() {
        return (
            // <div style={wrapperStyles}>
            <div>
                <MapView cityMarker={this.state.cityMarkers}
                    currentCityIndex={this.state.currentCityIndex}
                    polylinePath = {this.state.polylinePath}
                    tripPlan = {this.state.tripPlan}
                     />

                <InfoView
                    cityInfo={this.state.cityInfo}
                    cityLoaded={this.state.cityLoaded}

                    addToTrip={this.addToTrip.bind(this)}
                />
            </div>
        );
    }
}

export default TripPlannerParent;
