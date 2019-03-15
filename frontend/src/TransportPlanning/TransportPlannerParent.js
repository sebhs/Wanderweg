import React, { Component } from 'react';
import 'react-dates/lib/css/_datepicker.css';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import ReactJson from 'react-json-view'
import tripDataFake from './../fakeData/tripPlan.json';
import transportDataFake from './../fakeData/transport.json';
import Card from '@material-ui/core/Card';
import CityElem from './CityElem'
import TransportElem from './TransportElem'
import Paper from '@material-ui/core/Paper';


const wrapperStyles = {
    width: "100%",
    maxWidth: "100%",
    margin: "0 auto",
}

const host = 'http://localhost:5000'

class TransportPlannerParent extends Component {

    constructor() {
        super();
        this.state = {
            transportData: {},
            dataLoaded: false
        }
    }

    componentDidMount() {
        this.setState({ dataLoaded: false })
        const apiPoint = 'route_info';
        const URL = `${host}/${apiPoint}`
        let arrivalDate = new Date();
        const tripArr = tripDataFake.trip_info.map(elem => {
            let date = arrivalDate;
            arrivalDate.setTime(date.getTime() + elem.duration_in_days * 86400000);
            return {
                city_id: elem.city_id,
                ISO_date: date.toISOString()
            }
            //someDate.setDate(someDate.getDate() + numberOfDaysToAdd); 
        })
        const postBody = {
            "trip_info": tripArr
        }
        console.log(JSON.stringify(postBody));
        console.log('POST', URL);
        fetch(URL, {
            method: 'POST',
            // mode: 'no-cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postBody)
        })
            .then(function (response) {
                console.log("response: ")
                console.log(response)

                return response.json();
            }).then(function (data) {
                console.log("data: ")
                console.log(data)

                this.setState({
                    transportData: data,
                    dataLoaded: true,
                });
            }).catch((err) => {
                alert(err)
                console.error(err)
            });
        

        //     // this.setState({
        //     //     dataLoaded: true,
        //     // });
        //     alert(err)
        //     console.error(err)
        // });
        // .then(res => res.json())
        // .then(data => {

        //     this.setState({
        //         transportData: data,
        //         dataLoaded: true,
        //     });
        // }).catch((err) => {
        //     // this.setState({
        //     //     dataLoaded: true,
        //     // });
        //     alert(err)
        //     console.error(err)
        // });


    }










    render() {
        /* Waiting for data to load*/
        if (!this.state.dataLoaded) {
            return (<div style={{ display: 'flex', height: '200px', justifyContent: 'center' }}>
                <CircularProgress
                    style={{ padding: '100px' }} size={80} />
            </div>)
        }


        return (
            // <div style={wrapperStyles}>
            <div>
                {/* <Card style={{ padding: '60px' }}>
                    {tripDataFake.trip_info.map((city, index) => (
                        <div>
                            <CityElem
                                city={city}
                            />
                            {index < transportDataFake.length &&
                            <div>
                                <TransportElem
                                transport={transportDataFake[index]}
                                />
                            </div>
                            }
                        </div>
                    ))}


                    <ReactJson collapsed={true} name={'transportDataFake'} src={transportDataFake} />
                    <ReactJson collapsed={true} name={'tripDataFake'} src={tripDataFake} />


                </Card> */}

                <ReactJson collapsed={true} name={'tripDataFake'} src={this.state.transportData} />

            </div>
        );
    }
}

export default TransportPlannerParent;
