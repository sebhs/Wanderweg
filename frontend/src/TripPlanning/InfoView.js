import React, { Component } from 'react';


const wrapperStyles = {
    width: "100%",
    maxWidth: "100%",
    margin: "0 auto",
    padding: "1%",
}
class InfoView extends Component {

    constructor() {
        super();
        this.state = {
            index: 0,
        }
    }

    weatherBar() {
        let weatherBar = this.props.selectedCity.weather.map(weather =>
            <span>
                {weather.climate}  {weather.temp.inC + "ºC | "}
            </span>)

        return (
            <div>
            {"Weather Noah is Dick"}
            </div>
        )
    }
    


    render() {
        if(!this.props.selectedCity.name) {
            return(    <div style={wrapperStyles}>
                    No city selected
            </div>)
        }
        return (
            <div style={wrapperStyles}>
                City: {this.props.selectedCity.name}
                {this.weatherBar()}
            </div>
        );
    }
}

export default InfoView;
