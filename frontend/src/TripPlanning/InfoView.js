import React, { Component } from 'react';
import ReactJson from 'react-json-view'
import Card from '@material-ui/core/Card';
import Button from '@material-ui/core/Button';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import { withStyles } from '@material-ui/core/styles';
import ItemsList from './InfoViewChildren/ItemsList'
import Typography from '@material-ui/core/Typography';
import CardMedia from '@material-ui/core/CardMedia';
import CircularProgress from '@material-ui/core/CircularProgress';



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

    componentDidMount() {
    }


    render() {
        if (!this.props.cityLoaded) {
            return (<div style={{ display: 'flex', height: '200px', justifyContent: 'center' }}>
                <CircularProgress
                    style={{ padding: '100px' }} size={80} />
            </div>)
        }

        console.log(this.props.cityInfo);
        return (
            // <div style={wrapperStyles}>
            <div >
                <Card style={{ padding: '20px', height: '100vh' }}>
                    <Typography variant="h2" gutterBottom>
                        {this.props.cityInfo.name}, {this.props.cityInfo.country}
                    </Typography>
                    <Card>
                        {(this.props.cityInfo.activities.data.length > 0) &&
                            <CardMedia style={{ height: 170 }}
                                image={this.props.cityInfo.activities.data[0].city.cover_image_url}
                            />}
                    </Card>
                    <br />

                    {(this.props.cityInfo.activities.data.length > 0) &&
                        <div>
                            <Typography variant="h4" gutterBottom>
                                Activities in  {this.props.cityInfo.name}
                            </Typography>
                            <ItemsList
                                elems={this.props.cityInfo.activities.data}
                                isActivity={true}

                            />
                        </div>
                    }
                    <br />

                    {(this.props.cityInfo.hostels.length > 0) &&
                        <div>
                            <Typography variant="h4" gutterBottom>
                                Hostels in  {this.props.cityInfo.name}
                            </Typography>
                            <ItemsList
                                elems={this.props.cityInfo.hostels}
                                isActivity={false}
                            />
                        </div>
                    }
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => this.props.addToTrip()}
                    >
                        Add city to trip
                </Button>
                    <ReactJson collapsed={true} name={'weather'} src={this.props.cityInfo.weather} />
                    <ReactJson collapsed={true} name={'activities'} src={this.props.cityInfo.activities} />
                    <ReactJson collapsed={true} name={'hostels'} src={this.props.cityInfo.hostels} />
                </Card>



            </div>
        );
    }
}

export default InfoView;
