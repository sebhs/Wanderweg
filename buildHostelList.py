"""
Creates list of all hostels on hostelworld.com for a given country and writes them to file
Example use of Scraper class

To-do:
	- Add multiprocessing (threadpool?) to speed up
"""

# Imports
from screenScrape import Scraper
import sys


"""
Used to find the list of other locations on the country and provences pages
Inputs:
	urls - list of web addresses to scrape
	cityPage - bool saying if the links we are searching for are cities or not
Outputs
	If cityPage, list of tuples of (url, bool), else, list of urls
"""
def fetchOtherLocations(urls, cityPage):
	links = []
	for url in urls:
		s = Scraper(url)
		container = s.search('div', klass='otherlocations')
		otherLocations = s.search('a', portion='href', html=container[0])
		for link in otherLocations:
			if cityPage:
				links.append((link, True))
			else:
				links.append(link)
	return links


"""
Finds the link to every hostel on the page in the list of URLs, finds pagination links as well
Inputs:
	urls - list of tuples of (url, bool) where bool says weather to look for pagination or not
Ouptus:
	unique list of hostels
"""
def fetchHostels(urls):
	repeats = set()
	hostels = []

	while urls:
		url = urls.pop()
		s = Scraper(url[0])
		links = s.search('a', klass='hwta-property-link', portion='href')
		for link in links:
			if link not in repeats:
				repeats.add(link)
				hostels.append(link)

		if url[1]:
			pages = s.search('a', klass='pagination-page-number', portion='href')
			seen = set()
			for page in pages:
				if page != url and page not in seen:
					seen.add(page)
					urls.append((page, False))

	return hostels


# Helper function to write list of hostels to file
def writeToFile(urls):
	f = open('hostels.txt', 'w+')
	for url in urls:
		f.write(url + '\r\n')


# Builds list of hostels by searching down through Hostel worlds structure (country -> provence -> city -> hostel)
def createList(url):
	provences = fetchOtherLocations([url], False)
	print("Number of provences: ", len(provences))
	cities = fetchOtherLocations(provences, True)
	print("Number of cities: ", len(cities))
	hostels = fetchHostels(cities)
	print("Number of hostels: ", len(hostels))
	writeToFile(hostels)


# Main function that is called to parse command line and execute function
def main():
	if len(sys.argv) == 1:
		sys.stderr.write("Please give the country of interest\nProper format is python3 buildHostelList.py ~country~\n")
		return
	url = 'https://www.hostelworld.com/hostels/' + sys.argv[1]
	createList(url)


if __name__ == '__main__':
	main()