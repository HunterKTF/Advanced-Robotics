import serial
import time

gps = serial.Serial(port='COM3', baudrate=4800, timeout=0.1)

# print('Latitiude \t LatDirec \t Longitude \t LongDirec')

def convert_to_degrees_decimal(lat, lat_orientation, lon, lon_orientation, alt):

    lat_temp = float(lat) / 100.0
    lat_degrees = int(lat_temp)
    lat_decimal = (lat_temp - lat_degrees) * 100 / 60
    lat = lat_degrees + lat_decimal

    lon_temp = float(lon) / 100.0
    lon_degrees = int(lon_temp)
    lon_decimal = (lon_temp - lon_degrees) * 100 / 60
    lon = lon_degrees + lon_decimal

    alt = float(alt)
    if lat_orientation.lower() in "s":
        lat = -lat
    if lon_orientation.lower() in "w":
        lon = -lon
    
    return lat, lon, alt

while True:
    time.sleep(1)
    line = gps.readline()
    splits = str(line).strip("b'").split(',')

    if splits[0] == "$GPGGA":
        print(splits)
        latitiude = splits[2]
        latDirec  = splits[3]
        longitude = splits[4]
        longDirec = splits[5]
        altitude  = splits[9]

        lat, lon, alt = convert_to_degrees_decimal(latitiude, latDirec, longitude, longDirec, altitude)

        print(lat, lon, alt)
        # print(latitiude, 9*' ', latDirec, 10*' ', longitude, 8*' ', longDirec)
