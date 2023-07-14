#!python3
import location
import http.client
import io
import json
import datetime
from PIL import Image

'''This program checks the Space Weather Prediction Center for the current
Status of the Aurora.

Please adjust certain parameters'''

my_email = '' # Place your email here to allow them to contact you in the event of an issue.

def getLocation():
	if location.is_authorized():
		location.start_updates()
		myLocation = location.get_location()
		location.stop_updates()
	else:
		print("Location is not authorized.  Please open settings to authorize location")
		exit() # Exit codes > 0 don't work properly in Pythonista
		
	return myLocation
		
def getMap(latitude):
	if latitude > 0:
		conn = ("services.swpc.noaa.gov", "/images/aurora-forecast-northern-hemisphere.jpg")
	else:
		conn = ("services.swpc.noaa.gov", "/images/aurora-forecast-southern-hemisphere.jpg")
	h1 = http.client.HTTPSConnection(conn[0])
	h1.request(
			"GET", 
			conn[1], 
			None, 
			headers={"User-Agent": f"AuroraPredict/1.1a {my_email}"}
		)
	
	resp = h1.getresponse() # Get the HTTP Response
	if resp.status in range(200, 300): # Check to make sure the response is good.
		image = resp.read()
	else:
		print("Something isn't right.", resp.status, resp.reason)
		exit() # Exit if something is wrong.
		
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
		"User-Agent": f"AuroraPredict/1.1a {my_email}", # Add email in the event of needing to contact
		"Accept": "application/json"})
	resp = h2.getresponse()
	if resp.status in range(200, 300):
		data = json.load(resp)
	else:
		print("Something is wrong!", resp.status, resp.reason)
		exit(2) # Exit > 0 is an error, I am using exit 2 as HTTP Error
		
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
	image_map = getMap(my_location["latitude"]) # Pass the latitude to get the Norther or Southern Hemisphere
	print(f"Lat:  {my_location['latitude']}\n" \
       	f"Long: {my_location['longitude']}\n" \
		f"Indx: {my_index[0][2]}\n\n" \
		f"UTC\ntime:\t\t{datetime.datetime.utcnow()}\n" \
		f"Observation:\t{my_index[1]}\n" \
		f"Forcast:\t{my_index[2]}")
	image_map.show() # Benefit of Pythonista and PIL is that it will show the image in the console.
			
if __name__ == "__main__":
	main()
