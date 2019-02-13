import React, { Component } from 'react';
import worldMapCont from './../maps/topojson/world-continents.json';

// import worldMapCont from './../map/topojson/world-continents.json';

import {
    ComposableMap,
    ZoomableGroup,
    Geographies,
    Geography,
} from "react-simple-maps"



class ContinentSelect extends Component {
    constructor() {
        super();
        this.state = {
            width: 0,
            height: 0,
        }
    }

    handleClickOnContinent = (geography) => {
        this.props.setContinent(geography.properties.continent);
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
                    <Geographies geography={worldMapCont}>
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
            <div >
                <div>Select the continent you want to travel to?</div>
                {this.ContinentMap()}
            </div>
        );
    }
}

export default ContinentSelect;
