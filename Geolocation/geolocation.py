'''
This is the library to access to an iPhone via pyicloud to get the geolocation
'''

# Standard imports
import sys
import folium
import numpy as np
from pyicloud import PyiCloudService

# Local imports
from secrets import icloud_email, pswd


# Create a class for getting and visualizing geolocation
class Location:
    def __init__(self):
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

        self.prev_lat = 0
        self.prev_lon = 0
        self.prev_alt = 0

        self.latitude = np.array([])
        self.longitude = np.array([])
        self.altitude = np.array([])

        self.my_map = None

        self.p_g = None
        self.ned_north = np.array([])
        self.ned_east = np.array([])
        self.ned_elevation = np.array([])
        self.dist = np.array([0])

        self.r_ea = np.float64(6378137.0)  # Radius of the Earth (in meters)
        self.f = np.float64(1 / 298.257223563)  # Flattening factor WGS84 Model
        self.r_eb = self.r_ea * (1 - self.f)

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
        self.iphone = self.api.devices[1]

        self.status = self.iphone.status()
        self.location = self.iphone.location()

    def get_location(self):
        self.prev_lat, self.prev_lon, self.prev_alt = self.lat, self.lon, self.alt

        self.lat, self.lon, self.alt = self.location["latitude"], self.location["longitude"], self.location["altitude"]

    def print_map(self):
        self.my_map = folium.Map(location=[self.lat, self.lon], zoom_start=18)
        folium.Marker([self.lat, self.lon], popup="Hi").add_to(self.my_map)

    def update_map(self):
        folium.Marker([self.lat, self.lon], popup="Hi").add_to(self.my_map)

    def save_map(self):
        self.my_map.save("location.html")

    def play_sound(self):
        self.sound = self.iphone.play_sound()

    def ned_coordinates(self):
        self.latitude = np.array([self.prev_lat, self.lat])
        self.longitude = np.array([self.prev_lon, self.lon])
        self.altitude = np.array([self.prev_alt, self.alt])
        # Geodetic coordinates
        p_g = np.array([self.latitude,
                        self.longitude,
                        self.altitude])
        p_g = p_g.transpose()

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

            temp_dist += np.sqrt(np.power(abs(NED[1]), 2) + np.power(abs(NED[0]), 2))
            self.dist = np.append(self.dist, temp_dist)
            # print("NED Coordinates: ", NED)
            # print()
