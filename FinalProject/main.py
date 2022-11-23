# Import standard libraries
from time import sleep

# Import local libraries
from geolocation import Location

# Initialize object Location
location = Location()

# Get object API
location.get_api()

c = 0
while True:
    # Get cellular information
    location.get_iphone()

    if c < 1:
        # Initialize local view map
        location.print_map()

        location.init_location()

    else:
        # Get location information from cellular
        location.get_location()

        location.update_map()

    location.ned_coordinates()

    print(location.location)

    print("Geodetic coords:", location.lat, location.lon, location.alt, end=" | ")
    print("Travelled distance:", location.dist, end=" | ")
    print("Idle time:", location.idle)
    print("Speed:", location.speed, end=" | ")
    print("Acceleration:", location.accel, end=" | ")
    print("Distance from current position:", location.dist_starting_pos, end=" | ")
    print("Altitude:", location.alt, end=" | ")
    print("Elevation:", location.elevation)
    print()

    # Save map to location.html
    location.save_map()

    # Wait 1 second per query
    sleep(location.sampling_time)

    c += 1
