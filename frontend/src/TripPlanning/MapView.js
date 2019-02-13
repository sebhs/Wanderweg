/* eslint-disable */
import React from 'react';
import { compose, withProps } from 'recompose'
import { withScriptjs, withGoogleMap, GoogleMap } from 'react-google-maps'
import { Marker, Polyline } from 'react-google-maps'
import { Circle } from 'react-google-maps';


/*
 */



const GoogleMapsAPIKey = 'AIzaSyBw0StR76cWn1lE3laP23Tr9zig47bC-K8';
// const GoogleMapsAPIKey = 'AIzaSyCPnvf_D3QLKB2IrTT48DYH2rymnu9FCAM';




export default class Map extends React.Component {
    componentDidMount() {
        //GoogleMapsAPIKey = this.props.googleMapsAPIKey
    }

    render() {
        const cityMarkers = this.props.cityMarker.map(markerObj =>
            <Marker
                index={markerObj.index}
                position={markerObj.position}
                onClick={markerObj.onClick} />)
        return (
            <div>
                <MyMapComponent
                cityMarkers={cityMarkers}
                // polyline={
                //     <Polyline
                //         options={{ strokeColor: '#808080', strokeWeight: 2 }}
                //         path={this.props.pathCoordinates}
                //         geodesic={true}
                //     />}

                // centerPosition={this.props.centerPosition}
                // allVehiclesPolylines={allVehiclesPolylines}
                // currentSelectedVehicleMarker={currentSelectedVehicleMarker}
                // selectedVehicle={this.props.selectedVehicle}
                // currentVehicleCircle={currentVehicleCircle}
                // currentVehiclePolyline={currentVehiclePolyline}
                />
            </div>
        );
    }
}


const MyMapComponent = compose(
    withProps({
        googleMapURL: `https://maps.googleapis.com/maps/api/js?key=${GoogleMapsAPIKey}&v=3.exp&libraries=geometry,drawing,places`,
        loadingElement: <div style={{ height: `100%` }} />,
        containerElement: <div style={{ height: `100vh`, width: '60%', float: 'left' }} />,
        mapElement: <div style={{ height: `100%` }} />,
    }),
    withScriptjs,
    withGoogleMap,
)((props) =>
    <GoogleMap
        defaultZoom={6}
        defaultCenter={{ lat: 41.8719, lng: 12.5674 }}>
        {props.cityMarkers}

    </GoogleMap>);

