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
import { SingleDatePicker } from 'react-dates';
import 'react-dates/initialize'
import Snackbar from '@material-ui/core/Snackbar';
import CloseIcon from '@material-ui/icons/Close';

class StartView extends Component {
    constructor() {
        super();
        this.state = {
        }
    }

    componentDidMount() {
    }


    handleChange = (date) => {
        this.setState({
            startDate: date
        });
    };

    onClick = () => {
        if (this.state.date === undefined) {
            this.handleClickSnackBar();
        } else {
            this.props.goToPlanTrip(this.state.date);
        }
    }
    handleClickSnackBar = () => {
        this.setState({ snackBar: true });
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
            message={<span id='message-id'>Please Choose a Start Date</span>}
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
        return (
            <div >
                <Card style={{ padding: '20px', height: '100vh' }}>
                    {this.snackBar()}
                    <Typography variant="h3" gutterBottom>
                        Welcome to Wanderweg
                    </Typography>
                    <Typography>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                    </Typography>
                    <br />
                    <br />
                    <br />

                    <Typography variant="h5" gutterBottom>
                        Choose a date to get started with your trip
                    </Typography>
                    <SingleDatePicker
                        date={this.state.date} // momentPropTypes.momentObj or null
                        onDateChange={date => this.setState({ date })} // PropTypes.func.isRequired
                        focused={this.state.focused} // PropTypes.bool
                        onFocusChange={({ focused }) => this.setState({ focused })} // PropTypes.func.isRequired
                        id="your_unique_id" // PropTypes.string.isRequired,
                    />
                    <br />
                    <br />
                    <Button variant="contained" color="secondary" onClick={this.onClick}>
                        Plan Trip
                </Button>
                </Card>


            </div>
        );
    }
}

export default StartView;
