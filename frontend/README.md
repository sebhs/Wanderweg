
## WanderWeg React App

In order to run the Wanderweg App, first run 

### `npm install`

to install all the dependencies.

Then run:

### `npm start`

to start the React app.<br>

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

Make sure that the backend is running on `localhost:5000` before starting the app. 


In order to understand more about how the react app works check out the [wiki](https://github.com/StanfordCS194/Wanderweg/wiki)!


## More detailed description:


The Frontend application is built entirely with React JS and is using the Material UI framework for visually appealing display. 


If you don’t have node.js on your computer, please install it. 

This can be done with homebrew on a mac with the following command: 

`brew install node`

Otherwise visit this website to figure out how to install node https://nodejs.org/en/

In oder to get it started go to the frontend directory and  type in `npm install` to install all necessary dependencies. 

Once all the dependencies have been installed run `npm start`, wait a bit and the webs app will start on [http://localhost:3000](http://localhost:3000) Make sure that you have the backend sever running on `localhost:5000` before starting the web-app. 

The app consists of 3 parts: TripPlanning, TransportPlanning, and TripItinerary - which can all be found in the folders with the same names. 

The TripPlanning part lets the user explore different cities, add them to the trip, and select activities and hostels for each city. In the TransportPlanning part the user can select from different transportation options between the cities. And finally the TripItinerary displays the entire trip with prices and lets you book the different parts.

The parent of all these parts is App.js which handles the communication between them. In the following I will describe each part in more detail with its React components and how they work. 

## TripPlanning

### TripPlannerParent.js 

This handles the communication between all other components in this folder. It also fetches all the cities at the `/cities` endpoint. When started it displays the MapView on the left and the StartView on the right. After the StartView finished (see below) it switches the right component from StartView to InfoView but leaves the MapView on the left. 

#### StartView.js
The component is used for the user to select a Start-date of the trip. It utilizes Airbnb’s SingleDatePicker React component to ask for a date. After a date is selected it communicates to the TripPlannerParent that a date is selected at passes that date to it. 

#### MapView.js

The map is displayed by using the Google Maps Api. It displays markers for all the cities that were fetched by the TripPlannerParent. These markers are clickable, and when one is clicked it becomes green and sends the information on which city is selected to the parent which will fetch the api point `city_info/id` with that info and pass it along to the InfoView component. 

The map also displays polylines between the cities that were added to the trip. 

#### InfoView.js 

This component displays all the information about the currently selected city that it receives by the TripPlannerParent. It shows name, picture, possible activities to do, hostels, and allows you to add a city to your trip. In handles most of the logic for communicating between all its children. 

InfoView itself also has children components that can be found in `TripPlanning/InfoViewChildren`



##### ActivityElem.js

The component displays a single activity with its picture, name, details, price etc. The component has a button to get more information which will redirect you to a link of the activity and another button to add (or remove when already added) an activity to your trip/ 

##### HostelElem.js

The component displays a single hostel with its picture, name, rating, price etc.  The component has a button to get more information which will redirect you to a link of the hostel on hostelworld.com and another button to select the hostel. The user can only select one hostel per trip and cannot select none or more than one. 

##### ItemsList.js
Depending on the parameters passed into this component, it either displays a horizontally scrollable list of activity elements or hostel elements. 



## TransportPlanning

### TransportPlannerParent.js
The TransportPlannerParent gets a trip object that has been created by the TripPlannerParent and passed in through App.js. With the data of this objects it makes a POST request to the endpoint `/route_info` which returns the transportation information between all the cities. All the information is displayed like this: 

City A 
Possible Transport between A and B
City B
Possible Transport between B and C
City C 

Where he user can always choose between three options of transportation. Bus, cheapest train, fastest train. Sometimes only one  or two of the three will be avaliable, depending on the live data that is returned by the endpoint. 

#### CityElem.js
This component displays a city object that is given in a visually appealing way. 

#### TransportElem.js 
This components displays the three different options of transportation the user can choose from. The boxes are clickable and turn green when selected. This information is passed back to the parent. 


## TripItinerary
### TripItineraryParent.js
The TripItineraryParent displays your final trip itinerary with all the prices, durations, and transportations. Further it includes links for each activity, hostel, and transportation in order for the user to book the entire trip. 

#### ItineraryCityElem.js
Similar to the CityElem.js above,  a city object that is given in a visually appealing way and adds the links to book all the activities and hostels chosen. 

#### ItineraryTransportationElem.js 
This components displays the transportation that was previously chosen with the price, duration, and a link to book the transportation 


## App.js
The app.js component is the root parent of all and handles the logic for the communication between TripPlanning, TransportPlanning, and TropItinerary and finally gets rendered by index.js. 











































































































