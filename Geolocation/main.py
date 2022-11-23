# Import standard libraries
from time import sleep

# Import local libraries
from geolocation import Location

# Initialize object Location
location = Location()

# Get object API
location.get_api()

# Get cellular information
location.get_iphone()
print(location.location)

# Get location information from cellular
location.get_location()

# Initialize local view map
location.print_map()

while True:
    # Fetch last location data and update map
    location.get_location()
    location.update_map()

    print(location.latitude, location.longitude)
    location.ned_coordinates()

    # Save map to location.html
    location.save_map()

    # Wait 1 second per query
    sleep(1)
