import React, { Component } from 'react';
import ReactJson from 'react-json-view'
import Card from '@material-ui/core/Card';
import Button from '@material-ui/core/Button';
import city from './../fakeData/rome.json';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import { withStyles } from '@material-ui/core/styles';
import ActivitesList from './InfoViewChildren/ActivitesList'
const wrapperStyles = {
    width: "40%",
    float: 'right',
}
class InfoView extends Component {
    constructor() {
        super();
        this.state = {
            index: 0,
            cityInfo: city
        }
    }

    componentDidMount() {
        this.setState({
            cityInfo: city
        })
    }


    // weatherBar() {
    //     let weatherBar = this.state.cityInfo.weather.map(weather =>
    //         <span>
    //             {weather.climate}  {weather.temp.inC + "ºC | "}
    //         </span>)

    //     return (
    //         <div>
    //         </div>
    //     )
    // }
    // activitesList() {
    //     const gridStyles = theme => ({
    //         style: {
    //             display: 'flex',
    //             flexWrap: 'wrap',
    //             justifyContent: 'space-around',
    //             overflow: 'hidden',
    //             backgroundColor: theme.palette.background.paper,
    //         },
    //         gridList: {
    //             flexWrap: 'nowrap',
    //             // Promote the list into his own layer on Chrome. This cost memory but helps keeping high FPS.
    //             transform: 'translateZ(0)',
    //         },
    //         title: {
    //             color: theme.palette.primary.light,
    //         },
    //         titleBar: {
    //             background:
    //                 'linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)',
    //         },
    //     });

    //     let tmp = 
    //         <div style = {{
    //             display: 'flex',
    //             flexWrap: 'wrap',
    //             justifyContent: 'space-around',
    //             overflow: 'hidden',
    //         }

    //         }>
    //             <GridList cols={2.5}>
    //                 {this.state.cityInfo.activities.data.map(elem => (
    //                     <GridListTile key={elem.cover_image_url}>
    //                         <img src={elem.cover_image_url} alt={elem.title} />
    //                         <GridListTileBar
    //                             title={elem.title}
    //                             actionIcon={
    //                                 <IconButton>
    //                                     <StarBorderIcon />
    //                                 </IconButton>
    //                             }
    //                         />
    //                     </GridListTile>
    //                 ))}
    //             </GridList>
    //         </div>


    //     return (
    //         tmp);
    // }


    render() {
        // if (!this.state.cityInfo.name) {
        //     return (<div style={wrapperStyles}>
        //         No city selected
        //     </div>)
        // }
        return (
            // <div style={wrapperStyles}>
            <div >
                <Card style={{ padding: '20px', height: '100vh' }}>
                    City: {this.state.cityInfo.city}
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => this.props.addToTrip()}
                    >
                        Add city to trip
                </Button>
                    <ActivitesList
                        cityInfo={this.state.cityInfo}
                    />
                    <ReactJson collapsed={true} name={'weather'} src={this.state.cityInfo.weather} />
                    <ReactJson collapsed={true} name={'activities'} src={this.state.cityInfo.activities} />
                    <ReactJson collapsed={true} name={'hostels'} src={this.state.cityInfo.hostels} />
                </Card>



            </div>
        );
    }
}

export default InfoView;
