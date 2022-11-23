'''
This is the library to access to an iPhone via pyicloud to get the geolocation
'''

# Standard imports
import sys
import folium
import numpy as np
import requests
import pandas as pd
from pyicloud import PyiCloudService

# Local imports
from scr import icloud_email, pswd


# Create a class for getting and visualizing geolocation
class Location:
    def __init__(self):
        self.count = 0

        self.user = icloud_email
        self.password = pswd

        self.api = None
        self.iphone = None

        self.status = None
        self.location = None
        self.sound = None

        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.url = r'https://nationalmap.gov/epqs/pqs.php?'

        self.prev_lat = 0
        self.prev_lon = 0
        self.prev_alt = 0

        self.latitude = np.array([])
        self.longitude = np.array([])
        self.altitude = np.array([])

        self.my_map = None

        self.p_g_start = None
        self.p_g = None
        self.ned_north = np.array([])
        self.ned_east = np.array([])
        self.ned_elevation = np.array([])

        self.r_ea = np.float64(6378137.0)  # Radius of the Earth (in meters)
        self.f = np.float64(1 / 298.257223563)  # Flattening factor WGS84 Model
        self.r_eb = self.r_ea * (1 - self.f)

        self.sampling_time = 3  # Sample every second
        self.dist = 0
        self.idle = 0
        self.speed = 0
        self.accel = 0
        self.dist_starting_pos = 0
        self.elevation = 0
        self.not_allowed = 0

        self.dist_accum = np.array([0, 0])
        self.speed_accum = np.array([0, 0])

        self.samples = 10
        self.time_arr = np.zeros(self.samples)
        self.dist_arr = np.zeros(self.samples)
        self.idle_arr = np.zeros(self.samples)
        self.dist_start_arr = np.zeros(self.samples)
        self.alt_arr = np.zeros(self.samples)
        self.elev_arr = np.zeros(self.samples)
        self.na_arr = np.zeros(self.samples)

    def get_api(self):
        self.api = PyiCloudService(self.user, self.password)

        if self.api.requires_2fa:
            print("Two-factor authentication required.")
            code = input("Enter the code you received of one of your approved devices: ")
            result = self.api.validate_2fa_code(code)
            print("Code validation result: %s" % result)

            if not result:
                print("Failed to verify security code")
                sys.exit(1)

            if not self.api.is_trusted_session:
                print("Session is not trusted. Requesting trust...")
                result = self.api.trust_session()
                print("Session trust result %s" % result)

                if not result:
                    print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")
        elif self.api.requires_2sa:
            import click
            print("Two-step authentication required. Your trusted devices are:")

            devices = self.api.trusted_devices
            for i, device in enumerate(devices):
                print(
                    "  %s: %s" % (i, device.get('deviceName',
                                                "SMS to %s" % device.get('phoneNumber')))
                )

            device = click.prompt('Which device would you like to use?', default=0)
            device = devices[device]
            if not self.api.send_verification_code(device):
                print("Failed to send verification code")
                sys.exit(1)

            code = click.prompt('Please enter validation code')
            if not self.api.validate_verification_code(device, code):
                print("Failed to verify verification code")
                sys.exit(1)

    def get_iphone(self):
        self.iphone = self.api.devices[3]

        self.status = self.iphone.status()
        self.location = self.iphone.location()

    def get_altitude(self):
        query = ('https://api.open-elevation.com/api/v1/lookup'
                 f'?locations={self.lat},{self.lon}')
        r = requests.get(query).json()  # json object, various ways you can extract value
        elevation = pd.json_normalize(r, 'results')['elevation'].values[0]
        self.alt = float(elevation)

    def init_location(self):
        self.prev_lat, self.prev_lon, self.prev_alt = self.location["latitude"], \
                                                      self.location["longitude"], \
                                                      self.location["altitude"]
        self.lat, self.lon, self.alt = self.location["latitude"], self.location["longitude"], self.location["altitude"]
        self.get_altitude()

    def get_location(self):
        self.prev_lat, self.prev_lon, self.prev_alt = self.lat, self.lon, self.alt
        self.lat, self.lon, self.alt = self.location["latitude"], self.location["longitude"], self.location["altitude"]
        self.get_altitude()

    def print_map(self):
        self.my_map = folium.Map(location=[self.lat, self.lon], zoom_start=20)
        folium.Marker([self.lat, self.lon], popup="Hi").add_to(self.my_map)

    def update_map(self):
        folium.Marker([self.lat, self.lon], popup="Hi").add_to(self.my_map)

    def save_map(self):
        self.my_map.save("location.html")

    def play_sound(self):
        self.sound = self.iphone.play_sound()

    def get_dist_origin(self):
        latitude = np.array([self.p_g_start[0], self.p_g[0]])
        longitude = np.array([self.p_g_start[1], self.p_g[1]])
        altitude = np.array([self.p_g_start[2], self.p_g[2]])

        sin_lat = np.sin(np.radians(latitude))
        cos_lat = np.cos(np.radians(latitude))
        sin_lon = np.sin(np.radians(longitude))
        cos_lon = np.cos(np.radians(longitude))

        e = np.sqrt(np.power(self.r_ea, 2) - np.power(self.r_eb, 2)) / self.r_ea

        n_e = self.r_ea / np.sqrt(1 - np.power(e, 2) * np.power(sin_lat, 2))
        ff = n_e + altitude
        fn = 1 - np.power(e, 2)
        f_mult = n_e * fn + altitude

        # E.C.E.F. coordinates
        p_e = np.array([ff * cos_lat * cos_lon,
                        ff * cos_lat * sin_lon,
                        f_mult * sin_lat], dtype=float)
        p_e = p_e.transpose()

        # Point of reference
        shape = latitude.shape
        idx = np.arange(1, shape[0], 1, dtype=int)
        idx_ref = np.arange(shape[0] - 1)

        pe_subs = p_e[idx, :] - p_e[idx_ref, :]

        ned_list = []
        ned_north = []
        ned_east = []
        ned_elevation = []
        temp_dist = 0
        for x in idx_ref:
            rn_e = np.array([
                [-sin_lat[x] * cos_lon[x], -sin_lat[x] * sin_lon[x], cos_lat[x]],
                [-sin_lon[x], cos_lon[x], 0.0],
                [-cos_lat[x] * cos_lon[x], -cos_lat[x] * sin_lon[x], -sin_lat[x]]
            ])

            NED = rn_e.dot(pe_subs[x])
            ned_list.append(NED)
            ned_north = np.append(ned_north, abs(NED[0]))
            ned_east = np.append(ned_east, abs(NED[1]))
            ned_elevation = np.append(ned_elevation, NED[2])

            self.dist_starting_pos = np.sqrt(np.power(abs(NED[1]), 2) + np.power(abs(NED[0]), 2))

    def ned_coordinates(self):
        self.latitude = np.array([self.prev_lat, self.lat])
        self.longitude = np.array([self.prev_lon, self.lon])
        self.altitude = np.array([self.prev_alt, self.alt])
        # Geodetic coordinates
        self.p_g = np.array([self.lat,
                             self.lon,
                             self.alt])
        self.p_g = self.p_g.transpose()

        if self.count < 1:
            self.p_g_start = self.p_g

        sin_lat = np.sin(np.radians(self.latitude))
        cos_lat = np.cos(np.radians(self.latitude))
        sin_lon = np.sin(np.radians(self.longitude))
        cos_lon = np.cos(np.radians(self.longitude))

        e = np.sqrt(np.power(self.r_ea, 2) - np.power(self.r_eb, 2)) / self.r_ea

        n_e = self.r_ea / np.sqrt(1 - np.power(e, 2) * np.power(sin_lat, 2))
        ff = n_e + self.altitude
        fn = 1 - np.power(e, 2)
        f_mult = n_e * fn + self.altitude

        # E.C.E.F. coordinates
        p_e = np.array([ff * cos_lat * cos_lon,
                        ff * cos_lat * sin_lon,
                        f_mult * sin_lat], dtype=float)
        p_e = p_e.transpose()

        # Point of reference
        shape = self.latitude.shape
        idx = np.arange(1, shape[0], 1, dtype=int)
        idx_ref = np.arange(shape[0] - 1)

        pe_subs = p_e[idx, :] - p_e[idx_ref, :]

        ned_list = []
        temp_dist = 0
        for x in idx_ref:
            rn_e = np.array([
                [-sin_lat[x] * cos_lon[x], -sin_lat[x] * sin_lon[x], cos_lat[x]],
                [-sin_lon[x], cos_lon[x], 0.0],
                [-cos_lat[x] * cos_lon[x], -cos_lat[x] * sin_lon[x], -sin_lat[x]]
            ])

            NED = rn_e.dot(pe_subs[x])
            ned_list.append(NED)
            self.ned_north = np.append(self.ned_north, abs(NED[0]))
            self.ned_east = np.append(self.ned_east, abs(NED[1]))
            self.ned_elevation = np.append(self.ned_elevation, NED[2])
            self.dist_accum[0] = self.dist_accum[1]

            self.dist += np.sqrt(np.power(abs(NED[1]), 2) + np.power(abs(NED[0]), 2))
            self.dist_accum[1] = self.dist

            self.speed_accum[0] = self.speed_accum[1]
            self.speed = (self.dist_accum[1] - self.dist_accum[0]) / self.sampling_time
            self.speed_accum[1] = self.speed

            self.accel = (self.speed_accum[1] - self.speed_accum[0]) / self.sampling_time

            if self.speed == 0:
                self.idle += self.sampling_time

            self.elevation = self.ned_elevation[-1]

            self.get_dist_origin()
            # print("NED Coordinates: ", NED)
            # print()

    def update_arrays(self):
        self.count += 1
        self.time_arr = np.append(self.time_arr[1:], np.array([self.sampling_time*self.count]))
        self.dist_arr = np.append(self.dist_arr[1:], np.array([self.dist]))
        self.idle_arr = np.append(self.idle_arr[1:], np.array([self.idle]))
        self.dist_start_arr = np.append(self.dist_start_arr[1:], np.array([self.dist_starting_pos]))
        self.alt_arr = np.append(self.alt_arr[1:], np.array([self.alt]))
        self.elev_arr = np.append(self.elev_arr[1:], np.array([self.elevation]))
        self.na_arr = np.append(self.na_arr[1:], np.array([self.not_allowed]))
