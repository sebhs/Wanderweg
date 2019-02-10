import React, { Component } from 'react';
import ContinentSelect from './ContinentSelect'
import CountrySelect from './CountrySelect'



const wrapperStyles = {
    width: "100%",
    maxWidth: "100%",
    margin: "0 auto",
}

class TripPlannerParent extends Component {
    
    constructor() {
        super();
        this.state = {
            index: 0,
        }
    }
    setContinent = (selectedContinent) => {
        this.setState({ selectedContinent, index: ++this.state.index })
    }

    getPage = (index) => {
        if(index === 0) {
            return(<ContinentSelect setContinent={this.setContinent}/>);
        } else {
           return(<CountrySelect selectedContinent={this.state.selectedContinent} />);
        }
       
        
    }

    render() {
        return (
            <div style={wrapperStyles}>
                {this.getPage(this.state.index)}
            </div>
        );
    }
}

export default TripPlannerParent;
