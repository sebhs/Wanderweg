import sys
sys.path.append('./dataCollection')
from screenScrape import Scraper

def gatherHostelData(url):
	scrpr = Scraper(url)
	hostelsData = []
	hostels = scrpr.search('div', klass='fabresult')
	for h in hostels:
		hData = {}

		# Find images
		images = scrpr.search('div', klass='fabresult-image', portion='data-images', html=h)
		images = images[0].split(',')
		hData['cover_image_url'] = images[0]
		hData['image_urls'] = images[1:]

		# Find hostel name and site url
		link = scrpr.search('a', klass='hwta-property-link', html=h)
		hData['url'] = link[0].get('href')
		hData['name'] = link[0].text

		# Find location
		loc = scrpr.search('div', klass='addressline', html=h)
		hData['location'] = loc[0].text.replace('\n', '').replace(' - Show on Map', '')

		# Find rating
		rat = scrpr.search('a', klass='hwta-rating-score', html=h)
		hData['rating'] = 0.0 if not rat else rat[0].text.replace('\n', '').replace(' ', '')

		# Find price
		price = scrpr.search('span', klass='price', html=h)
		hData['price'] = 0.0 if not price else price[0].text

		hostelsData.append(hData)

	return hostelsData