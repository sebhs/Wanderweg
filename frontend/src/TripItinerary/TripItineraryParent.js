import React, { Component } from 'react';
import 'react-dates/lib/css/_datepicker.css';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import ReactJson from 'react-json-view'
import Card from '@material-ui/core/Card';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import CityElem from './ItineraryCityElem.js'
import TransportElem from './ItineraryTransportElem.js'
import propsFake from './../fakeData/propsFake.json';

const wrapperStyles = {
    width: "100%",
    maxWidth: "100%",
    margin: "0 auto",
}

class TripItineraryParent extends Component {

    constructor() {
        super();
        this.state = {

        }
    }
    componentDidMount() {

    }

    render() {
        console.log(JSON.stringify(this.props))
        return (
            // <div style={wrapperStyles}>
            <div>
                <Card style={{ padding: '60px' }}>
                <Typography gutterBottom variant="h3">
                    Your Itinerary:
                </Typography>
                <br/><br/>
                    {this.props.tripPlan.map((city, index) => (
                        <div>
                            <CityElem
                                city={city}
                            />
                            <br/>
                            {index < this.props.transport.length &&
                                <div style={{ "text-align": "center", "vertical-align": "middle" }}>
                           
                                    <TransportElem
                                        transport={this.props.transport[index] ? this.props.transport[index] : null }
                                       
                                    />
                                </div>
                            }
                        </div>
                    ))}
                </Card>
            </div>
        );
    }
}

export default TripItineraryParent;
