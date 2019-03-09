import React, { Component } from 'react';
import MapView from './MapView'
import InfoView from './InfoView'
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';

// import { cities } from './../fakeData/cities.json';

import milan from './../fakeData/milan.json';
import rome from './../fakeData/rome.json';
import florence from './../fakeData/florence.json';

const wrapperStyles = {
    width: "100%",
    maxWidth: "100%",
    margin: "0 auto",
}

const host = 'http://localhost:5000'

class TripPlannerParent extends Component {

    constructor() {
        super();
        this.state = {
            tripPlan: [],
            polylinePath: [],
            selectedCity: {},
            cities: [],
            currentCityIndex: -1,
            cityMarkers: [],
            cityLoaded: false,
            cityInfo: rome,
            dataLoaded: false,
        }
    }

    componentDidMount() {
        this.setState({ dataLoaded: false })
        const apiPoint = 'cities';
        const URL = `${host}/${apiPoint}`
        console.log('GET', URL);
        fetch(URL, {
            method: 'GET',
        })
            .then(res => res.json())
            .then(data => {
                this.setState({
                    cities: data,
                    dataLoaded: true,
                });
            this.fetchCity(); //TODO: delete
             console.log('City list fetched');
            }).catch((err) => {
                console.error(err)
            });
    }



    fetchCity() {
        this.setState({ cityLoaded: false })
        const { selectedCity } = this.state
        // let city = selectedCity.city_id === rome.city_id ? rome : milan;
        // city = selectedCity.city_id === florence.city_id ? florence : city;
        const apiPoint = 'city_info';
        const city_id = selectedCity.city_id;// TODO: add back
        // const city_id = 3;

        const URL = `${host}/${apiPoint}/${city_id}`
        console.log('GET', URL);
        fetch(URL, {
            method: 'GET',
        })
            .then(res => res.json())
            .then(data => {
                data.activities =  JSON.parse(data.activities);
                this.setState({
                    cityInfo: data,
                    cityLoaded: true,
            });
             console.log('City fetched', data);
            }).catch((err) => {
                console.error(err)
            });
    }


    setToCurrentCity = function (index) {
        this.setState({
            selectedCity: this.state.cities[index],
            currentCityIndex: index
        })
        this.fetchCity();

    }

    addToTrip = function () {
        if (this.state.currentCityIndex > -1) {
            // let tmpPolyline = this.state.polylinePath;
            // let tmpPlan = this.state.tripPlan;
            // tmpPolyline.push(this.state.cities[this.state.currentCityIndex].location);
            const city_id = this.state.cities[this.state.currentCityIndex].city_id;
            const crd = this.state.cities[this.state.currentCityIndex].location;
            // this.setState({
            //     tripPlan: tmpPlan,
            //     polylinePath: tmpPolyline,
            // })
            this.setState({
                polylinePath: [...this.state.polylinePath, crd],
                tripPlan: [...this.state.tripPlan, city_id],
            })
        }
    }




    render() {
        /* Waiting for data to load*/
        if (!this.state.dataLoaded) {
            return (<div style={{ display: 'flex', height: '200px', justifyContent: 'center' }}>
                <CircularProgress
                    style={{ padding: '100px' }} size={80} />
            </div>)
        }

        let cityMarkers = this.state.cities.map((city, index) => {
            return {
                index: index,
                city_id: city.city_id,
                position: city.location,
                onClick: () => this.setToCurrentCity(index)
            }
        });

        return (
            // <div style={wrapperStyles}>
            <div>
                <MapView cityMarker={cityMarkers}
                    currentCityIndex={this.state.currentCityIndex}
                    polylinePath={this.state.polylinePath}
                    tripPlan={this.state.tripPlan}
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
