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

    render() {
        const { classes } = this.props;
        const { spacing } = this.state;

        return (
            <Grid container className={classes.root} spacing={32}>
                <Grid item xs={12}>
                    <Grid container className={classes.demo} justify="center" spacing={Number(spacing)}>
                        {[0, 1, 2].map(value => (
                            <Grid key={value} item>
                                <Paper className={classes.paper} style={{ padding: "20px" }}>

                                    {value === 0 &&
                                        <div>
                                            <Typography>
                                                <b>Bus Option:</b>
                                            </Typography>
                                            <br />

                                            <Typography>
                                                <b>Duration:</b> {this.props.transport.bus[0].duration}
                                            </Typography>
                                            <Typography>
                                                <b>Price:</b> ${this.props.transport.bus[0].price}
                                            </Typography>
                                        </div>
                                    }
                                    {value === 1 &&
                                        <div>
                                            <Typography>
                                                <b>Cheapest Train Option:</b>

                                            </Typography>
                                            <br />
                                            <Typography>

                                                <b>Duration:</b> {this.props.transport.cheapest[0].duration}
                                            </Typography>
                                            <Typography>

                                                <b>Price:</b> ${this.props.transport.cheapest[0].price}
                                            </Typography>
                                        </div>
                                    }
                                    {value === 2 &&
                                        <div>
                                            <Typography>
                                                <b>Fastest Train Option:</b>
                                            </Typography>
                                            <br />

                                            <Typography>
                                                <b>Duration:</b> {this.props.transport.fastest[0].duration}
                                       c     </Typography>
                                            <Typography>
                                                <b>Price:</b> $c{this.props.transport.fastest[0].price}
                                            </Typography>
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
