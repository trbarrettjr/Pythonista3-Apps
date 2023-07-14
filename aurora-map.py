#!python3
import location
import http.client
import io
import json
import datetime
from PIL import Image

def getLocation():
	if location.is_authorized():
		location.start_updates()
		myLocation = location.get_location()
		location.stop_updates()
	else:
		print("Location is not authorized.  Please open settings to authorize location")
		exit(1)
		
	return myLocation
		
def getMap():
	conn = ("services.swpc.noaa.gov", 
	"/images/aurora-forecast-northern-hemisphere.jpg")
	h1 = http.client.HTTPSConnection(conn[0])
	h1.request("GET", conn[1], None, headers={"User-Agent": "AuroraPredict/1.1a email@domain.tld"}) # Provide an email address in the event they need to contact you.
	resp = h1.getresponse()
	if resp.status in range(200, 300):
		image = resp.read()
	else:
		print("Something isn't right.", resp.status, resp.reason)
		exit(2)
		
	image = Image.open(io.BytesIO(image))
	h1.close()
	return image
	
def getIndex(lat, long):
	conn = ("services.swpc.noaa.gov",
	"/json/ovation_aurora_latest.json")
	h2 = http.client.HTTPSConnection(conn[0])
	h2.request("GET", 
	conn[1], 
	None, 
	headers={
		"User-Agent": "AuroraPredict/1.1a email@domain.tld", # provide an email address in the event they need to contact you.
		"Accept": "application/json"})
	resp = h2.getresponse()
	if resp.status in range(200, 300):
		data = json.load(resp)
	else:
		print("Something is wrong!", resp.status, resp.reason)
		
	lat = int(lat)
	if long < 0:
		long = int(long + 360)
	else:
		long = int(long)
	
	for i in data["coordinates"]:
		if i[0] == long and i[1] == lat:
			result = i
	
	return result, data["Observation Time"], data["Forecast Time"]
	
def main():
	my_location = getLocation()
	my_index = getIndex(my_location["latitude"], my_location["longitude"])
	image_map = getMap()
	print("Lat:  {}\n" \
       "Long: {}\n" \
		"Indx: {}\n\n" \
		"UTC\ntime:\t\t{}\n" \
		"Observation:\t{}\n" \
		"Forcast:\t{}".format(
			my_location["latitude"], 
			my_location["longitude"], 
			my_index[0][2], 
			datetime.datetime.utcnow(),
			my_index[1],
			my_index[2]
		)
	)
	image_map.show()
			
if __name__ == "__main__":
	main()
