import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import FormLabel from '@material-ui/core/FormLabel';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import RadioGroup from '@material-ui/core/RadioGroup';
import Radio from '@material-ui/core/Radio';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';


const styles = theme => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        height: 140,
        width: 200,
    },
    control: {
        padding: theme.spacing.unit * 2,
    },
});

class TransportElem extends React.Component {
    state = {
        spacing: '40',
    };

    handleChange = key => (event, value) => {
        this.setState({
            [key]: value,
        });
    };
    //taken from here: https://www.w3resource.com/javascript-exercises/javascript-date-exercise-13.php    
    timeConvert = function (n) {
        var num = n;
        var hours = (num / 60);
        var rhours = Math.floor(hours);
        var minutes = (hours - rhours) * 60;
        var rminutes = Math.round(minutes);
        return rhours + "h and " + rminutes + "min";
    }
    noOption = function () {
        return (<div>
            <Typography variant="h8">
                <b>This option is currently not available</b>
            </Typography>
        </div>)
    }


    render() {
        const { classes } = this.props;
        const { spacing } = this.state;

        return (
            <Grid container className={classes.root} spacing={32}>
                <Grid item xs={12}>
                    <Grid container className={classes.demo} justify="center" spacing={Number(spacing)}>

                        {this.props.transport.trip_info.map((value, index) => (
                            <Grid key={value} item>
                                <Paper className={classes.paper} 
                                onClick={() => { this.props.addTransport(value,this.props.pos)}}
                                style={{ padding: "20px" ,backgroundColor: ((value.length > 0) && this.props.transportTrip.includes(value[0])) ? "LightGreen" : null}}
                                >

                                    {(index === 0) &&
                                        <div>
                                            {(value.length > 0) ? (
                                                <div>
                                                    <Typography variant="h8">
                                                        <b>Bus Option:</b>
                                                    </Typography>
                                                    <br />

                                                    <Typography>
                                                        <b>Duration:</b> {this.timeConvert(value[0].duration)}
                                                    </Typography>
                                                    <Typography>
                                                        <b>Price:</b> ${value[0].price}
                                                    </Typography>
                                                </div>
                                            ) : (
                                                    this.noOption()
                                                )
                                            }
                                        </div>
                                    }
                                    {(index === 1) &&
                                        <div>
                                            {(value.length > 0) ? (
                                                <div>
                                                    <Typography variant="h8">
                                                        <b>Cheapest Train Option:</b>
                                                    </Typography>
                                                    <br />
                                                    <Typography>
                                                        <b>Duration:</b> {this.timeConvert(value[0].duration)}
                                                    </Typography>
                                                    <Typography>
                                                        <b>Price:</b> ${value[0].price}
                                                    </Typography>
                                                </div>
                                            ) : (
                                                    this.noOption()
                                                )
                                            }
                                        </div>
                                    }
                                    {(index === 2) &&
                                        <div>
                                            {(value.length > 0) ? (
                                                <div>
                                                    <Typography variant="h8">
                                                        <b>Fastest Train Option:</b>
                                                    </Typography>
                                                    <br />

                                                    <Typography>
                                                        <b>Duration:</b> {this.timeConvert(value[0].duration)}
                                                    </Typography>
                                                    <Typography>
                                                        <b>Price:</b> ${value[0].price}
                                                    </Typography>
                                                </div>
                                            ) : (
                                                    this.noOption()
                                                )}
                                        </div>
                                    }
                                </Paper>

                            </Grid>

                        ))}
                    </Grid>
                </Grid>

            </Grid>
        );
    }
}

TransportElem.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(TransportElem);
