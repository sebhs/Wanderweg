import React, { Component } from 'react';
import MapView from './MapView'
import InfoView from './InfoView'
import StartView from './StartView'
import 'react-dates/lib/css/_datepicker.css';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import ReactJson from 'react-json-view'
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
            startpage: false, //TODO: set to true
            firstCitySelected: false,
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
                console.log(data)
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
                data.activities = JSON.parse(data.activities);
                this.setState({
                    cityInfo: data,
                    cityLoaded: true,
                });
            }).catch((err) => {
                console.error(err)
            });
    }


    setToCurrentCity = function (index) {
        this.setState({
            selectedCity: this.state.cities[index],
            currentCityIndex: index,
            firstCitySelected:true

        })
        this.fetchCity();
    }
    goToPlanTrip = function() {
        this.setState({startpage : false})
    }

    addToTrip = function (hostel, duration, activities) {
        if (this.state.currentCityIndex > -1) {
            // let tmpPolyline = this.state.polylinePath;
            // let tmpPlan = this.state.tripPlan;
            // tmpPolyline.push(this.state.cities[this.state.currentCityIndex].location);
            //const city_id = this.state.cities[this.state.currentCityIndex].city_id;
            const city = {
                city_id : this.state.cities[this.state.currentCityIndex].city_id,
                hostel : hostel,
                duration_in_days: duration, //duration in days
                activities : activities
            }
            const crd = this.state.cities[this.state.currentCityIndex].location;
            // this.setState({
            //     tripPlan: tmpPlan,
            //     polylinePath: tmpPolyline,
            // })
            if(this.state.tripPlan.length > 0 && this.state.tripPlan[this.state.tripPlan.length-1].city_id === city.city_id){
                return false;
            }
            this.setState({
                polylinePath: [...this.state.polylinePath, crd],
                tripPlan: [...this.state.tripPlan, city],
            })
            console.log(JSON.stringify(this.state.tripPlan))
            // console.log(this.state.tripPlan) 
            return true;
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


                {this.state.startpage ? (
                    <StartView 
                    goToPlanTrip={this.goToPlanTrip.bind(this)}
                    />
                ) : (
                        <InfoView
                            cityInfo={this.state.cityInfo}
                            cityLoaded={this.state.cityLoaded}
                            addToTrip={this.addToTrip.bind(this)}
                            firstCitySelected={this.state.firstCitySelected}
                        />
                    )}
                    {/* <ReactJson collapsed={false} name={'tripPlan'} src={this.state.tripPlan} /> */}

            </div>
        );
    }
}

export default TripPlannerParent;
