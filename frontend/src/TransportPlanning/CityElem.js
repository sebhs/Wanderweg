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


    return (
        <div className={classes.root}>
            {/* <Paper className={classes.paper}> */}
                <Grid container spacing={16}>
                    <Grid item>
                        <ButtonBase className={classes.image}>
                            <img className={classes.img} alt="complex" src={props.city.hostel.cover_image_url} />
                        </ButtonBase>
                    </Grid>
                    <Grid item xs={12} sm container>
                        <Grid item xs container direction="column" spacing={16}>
                            <Grid item xs>
                                <Typography gutterBottom variant="h5">
                                    {props.city.city}, {props.city.country}
                                </Typography>
                                <Typography gutterBottom>
                                    <b>Hostel you are staying:</b> {props.city.hostel.name}
                                </Typography>
                                <Typography gutterBottom>
                                    <b>Activites you are going to do:</b>
                                </Typography>
                                {props.city.activities.map(activity => (
                                    <Typography gutterBottom>
                                        {activity.title}
                                    </Typography>
                                ))}
                                {/* <Typography color="textSecondary">ID: 1030114</Typography> */}
                            </Grid>
                            {/* <Grid item>
                                <Button variant="contained" className={classes.button} target="_blank" href={props.city.hostel.url}>
                                    More
                             </Button> */}
                            {/*                              
                                {(props.city.selectedHostel !== props.city.hostel) &&
                                <span>
                                     <span>&nbsp;&nbsp;</span>
                                    <Button variant="contained" className={classes.button} onClick={() => props.city.selectHostel(props.city.hostel)}>
                                        Select
                                     </Button>
                                </span>}
                            </Grid> */}

                        </Grid>
                        <Grid item>
                            <Typography variant="subtitle1">Total Cost: <b>$88</b></Typography>
                        </Grid>
                    </Grid>
                </Grid>
            {/* </Paper> */}
        </div>
    );
}



export default withStyles(styles)(CityElem);
