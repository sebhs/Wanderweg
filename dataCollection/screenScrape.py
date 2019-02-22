"""
Creates an exportable class to make screen-scraping easier

To-do:
	- error checking on html fetch
	- more efficient element.class search
	- consider abstracting more by taking list of urls and desired props and including multiprocessing
"""

# Imports
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

class Scraper:

	"""
	Inialize Scraper, fetches HTML at given URL and stores internally as a BeautifulSoup object
	Inputs:
		url - valid HTTP(S) web address
	"""
	def __init__(self, url):
		
		# Get around for servers with protections against Python crawlers
		headers = {'User-Agent': 'Mozilla/5.0'} 

		req = Request(url, headers=headers)
		with urlopen(req) as response:
			htmlStr = response.read().decode('utf-8')
			self.soup = BeautifulSoup(htmlStr, 'html.parser')


	"""
	Finds a desired piece of HTML
	Inputs:
		element - DOM object we want to find (i.e. 'div' or 'a')
		klass - the class of the DOM object that we are looking for, defaults to None
		portion - the DOM element inside the match that we want to return, defaults to None
		html - the html that we want to search inside of, defaults to internally stored HTML from initialization
	Outputs:
		List of all matches to search query
	"""
	def search(self, element, klass=None, portion=None, html=None):
		if html == None: html = self.soup
		matches = []
		for e in html.find_all(element):
			
			if klass == None:
				if portion != None:
					matches.append(e.get(portion))
				else:
					matches.append(e)
				continue

			k = e.get('class')
			if k != None and k[0] == klass:
				if portion != None:
					matches.append(e.get(portion))
				else:
					matches.append(e)

		return matches
