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
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';


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
            transportData: [],
            // transportData: transportDataFake,

            dataLoaded: true,
            transportTrip: []
        }
    }
    componentDidMount() {
        this.fetch()
        let emptyTransportTrip = [];
        // for(let i = 0; i < this.state.transportData.length; i++){
        //     emptyTransportTrip.push({})
        // }
        // this.setState({transportTrip:emptyTransportTrip});
    }
    fetch() {
        this.setState({ dataLoaded: false })
        const apiPoint = 'route_info';
        const URL = `${host}/${apiPoint}`
        console.log(this.props.startDate)
        let arrivalDate = this.props.startDate.toDate();;
        arrivalDate.setTime(arrivalDate.getTime() + 2 * 86400000);
        const tripArr = this.props.tripPlan.map(elem => {
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
            .then(res => res.json())
            .then(data => {

                this.setState({
                    transportData: data,
                    dataLoaded: true,
                });
                console.log(JSON.stringify(data))
            }).catch((err) => {
                this.setState({
                    dataLoaded: true,
                });
                alert("Couldn't load transportation data")
                console.error(err)
            });
    }

    addTransport = function (value, index) {
        if (value.length <= 0) return;
        let a = this.state.transportTrip.slice(); //creates the clone of the state
        a[index] = value[0];
        this.setState({ transportTrip: a });
    }




    render() {
        console.log(this.state)
        /* Waiting for data to load*/
        if (!this.state.dataLoaded) {
            return (<div style={{ display: 'flex', height: '200px', justifyContent: 'center' }}>
                <CircularProgress
                    style={{ padding: '100px' }} size={80} />
            </div>)
        }
        console.log(this.props)
        return (
            // <div style={wrapperStyles}>
            <div>
                <Card style={{ padding: '60px' }}>
                    {this.props.tripPlan.map((city, index) => (
                        <div>
                            <CityElem
                                city={city}
                            />
                            {index < this.state.transportData.length &&
                                <div style={{ "text-align": "center", "vertical-align": "middle" }}>
                                    <Typography gutterBottom variant="h5">
                                        Choose a transport option:
                                </Typography>
                                {typeof this.state.transportData[index]}
                                    <TransportElem
                                        transport={this.state.transportData[index]}
                                        pos={index}
                                        addTransport={this.addTransport.bind(this)}
                                        transportTrip={this.state.transportTrip}
                                    />
                                </div>
                            }
                        </div>
                    ))}
                    <div style={{ "text-align": "center", "vertical-align": "middle" }}>
                        <Button variant="contained"
                            color="secondary"
                            onClick={() => this.props.finishedPlanning(this.state.transportTrip,this.props.tripPlan)}>
                            Done
                        </Button>
                    </div>


                </Card>


            </div>
        );
    }
}

export default TransportPlannerParent;
