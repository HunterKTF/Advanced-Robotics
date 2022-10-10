# Import standard libraries
import serial
import time

# Begin serial communication with GPS
gps = serial.Serial(port='COM3', baudrate=4800, timeout=0.1)    # Using Windows
# gps = serial.Serial(port='/dev/ttyUSB0', baudrate=4800, timeout=0.1)    # Using Linux


# Function to convert coordinates to degrees decimal
def convert_to_degrees_decimal(lat, lat_orientation, lon, lon_orientation, alt):
    # Get latitude in degrees decimal
    lat_temp = float(lat) / 100.0
    lat_degrees = int(lat_temp)
    lat_decimal = (lat_temp - lat_degrees) * 100 / 60
    lat = lat_degrees + lat_decimal
    
    # Get longitude in degrees decimal
    lon_temp = float(lon) / 100.0
    lon_degrees = int(lon_temp)
    lon_decimal = (lon_temp - lon_degrees) * 100 / 60
    lon = lon_degrees + lon_decimal
    
    alt = float(alt)        # Altitude in decimals
    if lat_orientation.lower() in "s":
        lat = -lat          # Latitude in correct sign
    if lon_orientation.lower() in "w":
        lon = -lon          # Longitude in correct sign
    
    return lat, lon, alt


# Infinite loop
while True:
    time.sleep(1)                   # Waits 1 second
    line = gps.readline()           # Reads serial port input data
    splits = str(line).strip("b'").split(',')
    
    if splits[0] == "$GPGGA":       # Gets GPGGA info from GPS device
        latitude = splits[2]        # Retrieves latitude data
        latDirec = splits[3]        # Retrieves latitude direction data
        longitude = splits[4]       # Retrieves longitude data
        longDirec = splits[5]       # Retrieves longitude direction data
        altitude = splits[9]        # Retrieves altitude data
        
        lat, lon, alt = convert_to_degrees_decimal(latitude, latDirec, longitude, longDirec, altitude)
        
        print(lat, lon, alt)
