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
import Button from '@material-ui/core/Button';


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


    //taken from here: https://www.w3resource.com/javascript-exercises/javascript-date-exercise-13.php    
    timeConvert = function (n) {
        var num = n;
        var hours = (num / 60);
        var rhours = Math.floor(hours);
        var minutes = (hours - rhours) * 60;
        var rminutes = Math.round(minutes);
        return rhours + "h and " + rminutes + "min";
    }

    render() {
        const { classes } = this.props;
        const { spacing } = this.state;

        return (
            <Grid container className={classes.root} spacing={32}>
                <Grid item xs={12}>
                    <Grid container className={classes.demo} justify="center" spacing={Number(spacing)}>

                        <Grid  item>
                            <Paper className={classes.paper}
                                style={{ padding: "20px" }}
                            >
                                {(this.props.transport === undefined || this.props.transport === null) ? (
                                    <div>No Transport available</div>
                                ) : (
                                    <div>
                                    <Typography variant="h8">
                                        <b>Transportation with {this.props.transport.type}:</b>
                                    </Typography>
                                    <br />

                                    <Typography>
                                        <b>Duration:</b> {this.timeConvert(this.props.transport.duration)}
                                    </Typography>
                                    <Typography>
                                        <b>Price:</b> ${this.props.transport.price}
                                    </Typography>
                                    <Typography>

                                    <Button variant="contained"
                                        target="_blank"
                                        href={this.props.transport.url}
                                        >
                                        Book
                                    </Button>
                                    </Typography>

                                </div>
                                )}

                            </Paper>

                        </Grid>
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
