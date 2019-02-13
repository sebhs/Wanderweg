import React, { Component } from 'react';
import Europe from './../maps/topojson/continents/europe.json';
import NorthAmerica from './../maps/topojson/continents/north-america.json';
import Africa from './../maps/topojson/continents/africa.json';
import Asia from './../maps/topojson/continents/asia.json';
import Oceania from './../maps/topojson/continents/oceania.json';
import SouthAmerica from './../maps/topojson/continents/south-america.json';

import {
    ComposableMap,
    ZoomableGroup,
    Geographies,
    Geography,
} from "react-simple-maps"



const strToContinent = new Map([
    ['Europe', Europe],
    ['North America',NorthAmerica],
    ['Africa', Africa],
    ['Oceania', Oceania],
    ['Asia', Asia],
    ['South America', SouthAmerica],

  ]);
  

class CountrySelect extends Component {
    constructor() {
        super();
        this.state = {
            width: 0,
            height: 0,
        }


    }

    handleClickOnContinent = (geography) => {
        console.log(geography)
        alert(geography.properties.geounit)
    };

    ContinentMap() {
        return (
            <ComposableMap
                projectionConfig={{
                    scale: 205,
                    rotation: [-11, 0, 0],
                }}
                width={980}
                height={551}
                style={{
                    width: "100%",
                    height: "auto",
                }}
            >
                <ZoomableGroup center={[0, 20]} disablePanning>
                    <Geographies geography={strToContinent.get(this.props.selectedContinent)}>
                        {(geographies, projection) => geographies.map((geography, i) => geography.id !== "ATA" && (
                            <Geography
                                key={i}
                                geography={geography}
                                projection={projection}
                                onClick={() => this.handleClickOnContinent(geography)}
                                style={{
                                    default: {
                                        fill: "#ECEFF1",
                                        stroke: "#607D8B",
                                        strokeWidth: 0.75,
                                        outline: "none",
                                    },
                                    hover: {
                                        fill: "#607D8B",
                                        stroke: "#607D8B",
                                        strokeWidth: 0.75,
                                        outline: "none",
                                    },
                                    pressed: {
                                        fill: "#FF5722",
                                        stroke: "#607D8B",
                                        strokeWidth: 0.75,
                                        outline: "none",
                                    },
                                }}
                            />
                        ))}
                    </Geographies>
                </ZoomableGroup>
            </ComposableMap>
        )
    }

    render() {
        return (
            <div>
                <div>Select the continent you want to travel to?</div>
                {this.ContinentMap()}
            </div>
        );
    }
}

export default CountrySelect;
