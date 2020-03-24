from geocode import getGeocodeLocation
import httplib2
import json

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# constants
client_id = "yourclientid"
client_secret = "yourclientsecret"

def findARestaurant(mealType,location):
	coordinates = getGeocodeLocation(location);
	latitude = coordinates[0]
	longitude = coordinates[1]

	# Search for restaurants
	url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&ll=%s,%s&query=%s&v=20171231&locale=en'% (client_id, client_secret, latitude, longitude, mealType))
	h = httplib2.Http()
	response, content = h.request(url, 'GET')
	result = json.loads(content)

	# grab first venue's result
	venue_name = result['response']['venues'][0]['name']
	addr = result['response']['venues'][0]['location']['formattedAddress']
	venue_addr = ""
	for item in addr:
		venue_addr += item + " "
	venue_id = result['response']['venues'][0]['id']
	
	# url to make image request
	image_request = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20171231'% (venue_id, client_id, client_secret))
	response, content = h.request(image_request, 'GET')
	result = json.loads(content)

	# if no photos exist use stock photo otherwise use photo, display as 300x300 px
	# default image
	image_url = "http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct"
	
	# if a photo exists, set the correct prefix and suffix
	if (result['response']['photos']['count'] != 0):
		prefix = result['response']['photos']['items'][0]['prefix']
		suffix = result['response']['photos']['items'][0]['suffix']
		image_url = ('%s300x300%s'% (prefix, suffix))


	print ('Restaurant Name: %s\nRestaurant Address: %s\nImage: %s\n'% (venue_name, venue_addr, image_url))

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
