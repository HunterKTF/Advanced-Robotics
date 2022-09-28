"""
Python library to compute the position of a GPS sensor using a transformation matrix

Author: Jorge Ricardo Hernández Sabino
Contact: jorge.hernandezs@udem.edu
Last Updated: 28/09/2022
"""

# Import dependencies for matrix handling
import numpy as np


# Create a class for the transformation matrix generation
class Transform:
    def __init__(self):
        self.alpha = 0              # yaw angle
        self.beta = 0               # pitch angle
        self.gamma = 0              # roll angle
        
        self.tx = 0                 # translation in x
        self.ty = 0                 # translation in y
        self.tz = 0                 # translation in z
        
        self.yaw = np.array([])     # empty rotational matrix for yaw movement
        self.pitch = np.array([])   # empty rotational matrix for pitch movement
        self.roll = np.array([])    # empty rotational matrix for roll movement
        
        self.R = np.array([])       # empty 3D rotational matrix
        self.t = np.array([])       # empty translation vector
        
        self.T_LG = np.array([])    # empty transformation matrix
        self.p_L = []               # empty position list
        self.p_G_h = np.array([])   # empty GPS homogeneous position array
        self.p_g = np.array([])     # empty GPS position array
    
    # Computing the transformation matrix to obtain the result
    def compute_transformation(self):
        # Compute the position of object regarding the LiDAR sensor
        p_L = np.array([[self.p_L[0]],
                        [self.p_L[1]],
                        [self.p_L[2]]])
        p_L = np.append(p_L, [[1]], axis=0)
        
        # Compute the global position of GPS using the transformation matrix
        self.p_G_h = self.T_LG.dot(p_L)
        self.p_g = self.p_G_h[0:3]
        print(self.p_g)
    
    # This function returns the 3D rotation matrix R
    def compute_3d_rotation(self):
        
        # Create the 3D rotational matrix for yaw movement using alpha angle
        alpha = np.radians(self.alpha)
        self.yaw = np.array([[np.cos(alpha), -np.sin(alpha), 0],
                             [np.sin(alpha), np.cos(alpha), 0],
                             [0, 0, 1]])

        # Create the 3D rotational matrix for pitch movement using beta angle
        beta = np.radians(self.beta)
        self.pitch = np.array([[np.cos(beta), 0, np.sin(beta)],
                               [0, 1, 0],
                               [-np.sin(beta), 0, np.cos(beta)]])

        # Create the 3D rotational matrix for roll movement using gamma angle
        gamma = np.radians(self.gamma)
        self.roll = np.array([[1, 0, 0],
                              [0, np.cos(gamma), -np.sin(gamma)],
                              [0, np.sin(gamma), np.cos(gamma)]])

        # Compute the 3D rotational matrix of the system
        temp = np.matmul(self.yaw, self.pitch)
        self.R = np.matmul(temp, self.roll)
        print(self.R)
    
    # This function returns the 3D translation vector t.
    def compute_3d_translation(self):
        # Create the translation array using the coordinates of t
        self.t = np.array([[self.tx], [self.ty], [self.tz]])
        print(self.t)
    
    # This function returns the 3D transformation matrix T_LG that will be applied to p_L
    def compute_3d_transformation_matrix(self):
        # Create the transformation matrix using the rotational matrix and translation vector
        temp_matrix = np.append(self.R, self.t, axis=1)
        self.T_LG = np.append(temp_matrix, [[0, 0, 0, 1]], axis=0)  # Append the scaling vector
        print(self.T_LG)
