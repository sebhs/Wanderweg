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
        width: 128 * 4,
        height: '80%',
    },
    image: {
        width: 128,
        height: 128,
    },
    img: {
        maxWidth: '100%',
        maxHeight: '100%',
    }
});
function HostelElem(props) {
    const { classes } = props;
 

    return (
        <div className={classes.root}>
            <Paper className={classes.paper} style={{backgroundColor: (props.selectedHostel === props.hostel) ? "LightGreen" : null}}>
                <Grid container spacing={16}>
                    <Grid item>
                        <ButtonBase className={classes.image}>
                            <img className={classes.img} alt="complex" src={props.hostel.cover_image_url} />
                        </ButtonBase>
                    </Grid>
                    <Grid item xs={12} sm container>
                        <Grid item xs container direction="column" spacing={16}>
                            <Grid item xs>
                                <Typography gutterBottom variant="subtitle1">
                                    {props.hostel.name}
                                </Typography>
                                <Typography gutterBottom> {props.hostel.location}</Typography>
                                {/* <Typography color="textSecondary">ID: 1030114</Typography> */}
                            </Grid>
                            <Grid item>
                                <Button variant="contained" className={classes.button} target="_blank" href={props.hostel.url}>
                                    More
                             </Button>
                             
                                {(props.selectedHostel !== props.hostel) &&
                                <span>
                                     <span>&nbsp;&nbsp;</span>
                                    <Button variant="contained" className={classes.button} onClick={() => props.selectHostel(props.hostel)}>
                                        Select
                                     </Button>
                                </span>}
                            </Grid>

                        </Grid>
                        <Grid item>
                            <Typography variant="subtitle1">Price: <b> {props.hostel.price.substring(2)}</b>&nbsp;&nbsp;&nbsp;&nbsp;Rating: <b>{props.hostel.rating}</b></Typography>
                        </Grid>
                    </Grid>
                </Grid>
            </Paper>
        </div>
    );
}



export default withStyles(styles)(HostelElem);
