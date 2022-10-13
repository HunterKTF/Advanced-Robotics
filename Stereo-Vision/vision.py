# Import standard libraries
import numpy as np
from matplotlib import pyplot as plt


class Stereo:
    def __init__(self):
        self.B = 0
        self.f = 0
        self.f_pixels = 0
        self.s_h = 0
        self.s_v = 0
        self.p_s = 0
        self.h_max = 0
        self.v_max = 0
        self.sp = 0
        self.m = 0
        self.p = 0

    def z_min(self):
        z_min = self.f * self.B / ((self.h_max * self.p_s) - 1)
        return z_min

    def disparity(self, z):
        m = (self.f * self.B) / (self.p_s * z)
        return m

    def disparity_func(self, x):
        return (self.f * self.B) / (self.p_s * x)

    def disparity_vs_range(self, z_min, z_max):
        x = np.linspace(z_min, z_max, 100)

        plt.plot(x, self.disparity_func(x), color='red')
        plt.xlabel('Z range [m]')
        plt.ylabel('Disparity [px]')
        plt.title('Disparity vs Range')
        plt.show()

    def range_resolution(self, z):
        r = np.power(z, 2)/(self.B * self.f) * self.sp * self.p_s
        r = r / 1000
        return r

    def range_resolution_func(self, z):
        return (np.power(z, 2)/(self.B * self.f) * self.sp * self.p_s)/1000

    def range_res_vs_range(self, z_min, z_max):
        z = np.linspace(z_min, z_max, 100)

        plt.plot(z, self.range_resolution_func(z), color='red')
        plt.xlabel('Z range [m]')
        plt.ylabel('Resolution [mm]')
        plt.title('Range resolution vs Range')
        plt.show()

    def compute_deltas(self, z):
        delta_x = (self.p / self.f_pixels) * z
        delta_y = (self.p / self.f_pixels) * z
        delta_z = np.power(z, 2)/(self.f_pixels * (self.B/1000)) * self.m

        return delta_x, delta_y, delta_z

    def delta_x_func(self, z):
        return (self.p / self.f_pixels) * z

    def delta_y_func(self, z):
        return (self.p / self.f_pixels) * z

    def delta_z_func(self, z):
        return np.power(z, 2)/(self.f_pixels * (self.B/1000)) * self.m

    def plot_deltas(self, z_min, z_max):
        z = np.linspace(z_min, z_max, 100)

        # Plot delta x
        plt.plot(z, self.delta_x_func(z), color='red')
        plt.xlabel('Z range [m]')
        plt.ylabel('∆X [m]')
        plt.title('∆X vs Range')
        plt.show()

        # Plot delta y
        plt.plot(z, self.delta_y_func(z), color='red')
        plt.xlabel('Z range [m]')
        plt.ylabel('∆Y [m]')
        plt.title('∆Y vs Range')
        plt.show()

        # Plot delta z
        plt.plot(z, self.delta_z_func(z), color='red')
        plt.xlabel('Z range [m]')
        plt.ylabel('∆Z [m]')
        plt.title('∆Z vs Range')
        plt.show()

    def max_range_measurable(self, m_min):
        z_max = (m_min * self.p_s) / (self.f * self.B)
        return z_max
