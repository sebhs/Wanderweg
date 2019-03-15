import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import ButtonBase from '@material-ui/core/ButtonBase';
import Button from '@material-ui/core/Button';
const styles = theme => ({
    //   root: {
    //     flexGrow: 1,
    //   },
    paper: {
        padding: theme.spacing.unit * 2,
        margin: 'auto',
        width: '80%',
        height: '80%',
    },
    image: {
        width: 128 * 2,
        height: 128,
    },
    img: {
        maxWidth: '100%',
        maxHeight: '100%',
    }
});
function CityElem(props) {
    const { classes } = props;
    let total_cost = function () {
        let totalPrice = props.city.hostel.price.match(/\d+/g).map(Number)[0];
        totalPrice *= parseInt(props.city.duration_in_days);

        for (let i = 0; i < props.city.activities.length; i++) {
            totalPrice += props.city.activities[i].retail_price.value;
        }
        return totalPrice;
    }

    return (
        <div className={classes.root}>
            {/* <Paper className={classes.paper}> */}
            <Grid container spacing={16}>
                <Grid item>
                    <ButtonBase className={classes.image}>
                        <img className={classes.img} alt="complex" src={props.city.city_obj.alt_cover} />
                    </ButtonBase>
                </Grid>
                <Grid item xs={12} sm container>
                    <Grid item xs container direction="column" spacing={16}>
                        <Grid item xs>
                            <Typography gutterBottom variant="h5">
                                {props.city.city_obj.name}, {props.city.city_obj.country}
                            </Typography>
                            <Typography gutterBottom>
                                <b>Days:</b> {props.city.duration_in_days}
                            </Typography>

                            <Typography gutterBottom>
                                <b>Your Hostel:</b> {props.city.hostel.name}
                                <span>&nbsp;&nbsp;</span>
                                |
                                <span>&nbsp;&nbsp;</span>
                                Price: <i>{props.city.hostel.price.substring(2)}</i>
                                <span>&nbsp;&nbsp;</span>

                                <Button variant="contained"
                                    target="_blank"
                                    href={props.city.hostel.url}
                                >
                                    Book
                        </Button>
                            </Typography>
                            <Typography gutterBottom>
                                <b>Your Activites:</b>
                            </Typography>
                            {props.city.activities.map(activity => (
                                <Typography gutterBottom>
                                    {activity.title}
                                    <span>&nbsp;&nbsp;</span>
                                    |
                                <span>&nbsp;&nbsp;</span>
                                    Price: <i>{activity.retail_price.formatted_value}</i>
                                    <span>&nbsp;&nbsp;</span>

                                    <Button variant="contained"
                                        target="_blank"
                                        href={activity.url}>
                                        Book
                                    </Button>
                                </Typography>
                            ))}
                            {/* <Typography color="textSecondary">ID: 1030114</Typography> */}
                        </Grid>

                    </Grid>
                    <Grid item>
                        <Typography variant="subtitle1">Total Cost: <b>${total_cost()}</b></Typography>
                    </Grid>
                </Grid>
            </Grid>
            {/* </Paper> */}
        </div>
    );
}



export default withStyles(styles)(CityElem);
