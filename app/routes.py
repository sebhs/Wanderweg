from app import app
from flask import request
from app.climate import GatherClimate
from app.activities import GatherActivities
from app.trains import GatherTrains
from app.population import GatherPop

@app.route('/')
def home():
    return "Server is running"

#Returns climate data for a city. Note that it also requires the country
@app.route('/weather/<country>/<city>')
def getWeather(country, city):
    climateScraper = GatherClimate()
    return climateScraper.scrapeData(country, city)

#Returns activities in a city
@app.route('/activities/<city>')
def getActivities(city):
    activityScraper = GatherActivities()
    return activityScraper.scrapeCity(city)

#Returns train info for a trip between two cities 
#Note that requests need to replace spaces with underscores
@app.route('/trains', methods=['GET'])
def getTrains():
    #Fetch and clean up params
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    date = request.args.get('date')
    num_results = int(request.args.get('n'))
    origin = origin.replace("_", " ")
    destination = destination.replace("_", " ")
    #Get route data
    trainScraper = GatherTrains()
    return trainScraper.scrapeAllInfo(origin, destination, date, num_results)

@app.route('/population/<country>/<city>')
def getPopulation(country, city):
    print(country, city)
    popScraper = GatherPop()
    return popScraper.scrapeInfo(country, city)