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
import TextField from '@material-ui/core/TextField';
import Snackbar from '@material-ui/core/Snackbar';
import CloseIcon from '@material-ui/icons/Close';


const wrapperStyles = {
    width: "40%",
    float: 'right',
}
class InfoView extends Component {
    constructor() {
        super();
        this.state = {
            index: 0,
            activities: [],
            snackBarMsg: ""
        }
    }

    componentWillReceiveProps(nextProps) {
        // You don't have to do this check first, but it can help prevent an unneeded render
        if (!this.props.cityLoaded) {
            this.handleCloseSnackBar()
        }
    }
    selectHostel = function (hostel) {
        this.setState({ selectedHostel: hostel })
    }
    addActivity = function (activity) {
        this.setState({ activities: [...this.state.activities, activity], })
    }
    removeActivity = function (activity) {
        let arr = [...this.state.activities]; // make a separate copy of the array
        var index = arr.indexOf(activity)
        if (index !== -1) {
            arr.splice(index, 1);
            this.setState({ activities: arr });
        }
    }
    handleChangeDays = days => event => {
        this.setState({
            numDays: event.target.value,

        });
    };


    handleAddTrip = function () {
        if (this.state.selectedHostel === undefined || this.state.selectedHostel === "") {
            this.handleClickSnackBar("Please select a hostel");
            this.setState({ numDays: "" });
            return;
        }
        if (this.state.numDays === undefined || this.state.numDays === "") {
            this.handleClickSnackBar("Please select add valid number of days");
            this.setState({ numDays: "" });
            return;
        }
        if (this.props.addToTrip(this.state.selectedHostel, this.state.numDays, this.state.activities)) {
            this.handleClickSnackBar("Trip Added");
        } else {
            this.handleClickSnackBar("Trip already added");
        }
        this.setState({ numDays: "" });
        this.setState({ selectedHostel: "" });


    }
    handleClickSnackBar = (msg) => {
        this.setState({ snackBarMsg: msg, snackBar: true });
    };

    handleCloseSnackBar = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        this.setState({ snackBar: false });
    };
    snackBar() {
        return (<Snackbar
            anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
            }}
            open={this.state.snackBar}
            autoHideDuration={3000}
            onClose={this.handleCloseSnackBar}
            ContentProps={{
                'aria-describedby': 'message-id',
            }}
            message={<span id='message-id'>{this.state.snackBarMsg}</span>}
            action={[
                <IconButton
                    key='close'
                    aria-label='Close'
                    color='inherit'
                    onClick={this.handleCloseSnackBar}
                >
                    <CloseIcon />
                </IconButton>,
            ]}
        />);
    }


    render() {
        if (!this.props.firstCitySelected) {
            return (
                <div>
                    <Card style={{ padding: '20px', height: '100vh' }}>

                        <Typography variant="h3" gutterBottom>
                            Start Planning your Trip
                    </Typography>
                        <Typography variant="h6sƒ" >
                            Click on one of the markers on the map to explore a city!
                    </Typography>
                    </Card>
                </div>

            );
        }
        if (!this.props.cityLoaded) {
            return (<div style={{ display: 'flex', height: '200px', justifyContent: 'center' }}>
                <CircularProgress
                    style={{ padding: '100px' }} size={80} />
            </div>)
        }



        return (
            // <div style={wrapperStyles}>
            <div >
                {this.snackBar()}
                <Card style={{ padding: '20px', height: '100vh', overflow: 'auto' }}>
                    <Typography variant="h2" gutterBottom>
                        {this.props.cityInfo.name}, {this.props.cityInfo.country}
                    </Typography>
                    <Card>
                        {(this.props.cityInfo.activities.data.length > 0) ? (
                            <CardMedia style={{ height: 170 }}
                                image={(this.props.cityInfo.activities.data[0].city.cover_image_url)}
                            />
                        ) : (
                                <CardMedia style={{ height: 170 }}
                                    image={(this.props.cityInfo.alt_cover)}
                                />
                            )}
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
                                addActivity={this.addActivity.bind(this)}
                                removeActivity={this.removeActivity.bind(this)}

                                activities={this.state.activities}

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
                                selectHostel={this.selectHostel.bind(this)}
                                selectedHostel={this.state.selectedHostel}
                            />
                        </div>
                    }
                    <br /><br />
                    <div style={{ align: "justify" }}>
                        <TextField
                            id="outlined-number"
                            label="Number of Days"
                            value={this.state.numDays}
                            onChange={this.handleChangeDays('days')}
                            type="number"
                            // className={classes.textField}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            margin="normal"
                            variant="outlined"
                        />
                        <span>&nbsp;&nbsp;</span>

                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => this.handleAddTrip()}
                        >
                            Add city to trip
                </Button>
                <span>&nbsp;&nbsp;</span>
                        <Button variant="contained" 
                        color="secondary" 
                        onClick={() => this.props.donePlanning()}
                        >
                            Finished
                        </Button>

                    </div>

                    {/* <ReactJson collapsed={true} name={'cityInfo'} src={this.props.cityInfo} /> */}
                </Card>



            </div>
        );
    }
}

export default InfoView;
