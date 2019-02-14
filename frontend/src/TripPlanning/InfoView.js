import React, { Component } from 'react';
import ReactJson from 'react-json-view'
import Card from '@material-ui/core/Card';


const wrapperStyles = {
    width: "40%",
    float: 'right',
}
class InfoView extends Component {

    constructor() {
        super();
        this.state = {
            index: 0,
        }
    }

    // weatherBar() {
    //     let weatherBar = this.props.selectedCity.weather.map(weather =>
    //         <span>
    //             {weather.climate}  {weather.temp.inC + "ºC | "}
    //         </span>)

    //     return (
    //         <div>
    //         </div>
    //     )
    // }



    render() {
        if (!this.props.selectedCity.name) {
            return (<div style={wrapperStyles}>
                No city selected
            </div>)
        }
        return (
            <div style={wrapperStyles}>
                <Card style={{ padding: '20px', height:'100vh' }}>
                    City: {this.props.selectedCity.name}
                    <ReactJson collapsed={true} name={'weather'} src={this.props.selectedCity.weather} />
                    <ReactJson collapsed={true} name={'activities'} src={this.props.selectedCity.activities} />
                    <ReactJson collapsed={true} name={'hostels'} src={this.props.selectedCity.hostels} />

                </Card>
            </div>
        );
    }
}

export default InfoView;
