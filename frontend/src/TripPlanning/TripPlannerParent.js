import React, { Component } from 'react';
import ContinentSelect from './ContinentSelect'
import CountrySelect from './CountrySelect'


// const pages =  [<ContinentSelect setContinent={this.setContinent}/>, <CountrySelect /> ]
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
            <div>
                {this.getPage(this.state.index)}
            </div>
        );
    }
}

export default TripPlannerParent;
