import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import cos, sin



def dh_frame_i(d, a, alpha, theta) :
    # Return DH frame with given parameters
    return np.array([[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
                      [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
                      [0, sin(alpha), cos(alpha), d],
                      [0, 0, 0, 1]])

def dh_frame_tot(d, a, alpha, theta) :

    # Initialize base frame and positions and orientations matrices
    T = np.eye(4)
    positions = []
    orientations = []

    # Successive transformations
    for i in range(len(d)) :
        A = dh_frame_i(d[i], a[i], alpha[i], theta[i])
        T = T @ A

        # Add t
        positions.append(T[:3, 3]) # First 3 entries of the right column of the matrix
        orientations.append(T[:3, :3]) # Top left 3 x 3 in the matrix

    return positions, orientations;


# DH Parameters for  6 DOF Robot (not accurate for TES, yet)
d = [0.2, 0, 0, 0.6, 0, 0.4]      
a = [0, 0.5, 0.4, 0, -0.3, 0.0]          
alpha = [np.pi/2, 0, 0, np.pi/2, -np.pi/2, np.pi/2]  
theta = [np.pi/3, np.pi/4, np.pi/6, np.pi/2, -np.pi/4, np.pi/2]  

# Get positions and orientations 
positions, orientations = dh_frame_tot(d, a, alpha, theta)

# Plot robot and frames
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each joint and its frame
for i, pos in enumerate(positions):
    # Plotting the joint as point
    ax.scatter(pos[0], pos[1], pos[2], color='purple', marker='o', s=30)

    # Rotations matrix
    R = orientations[i]
    
    scale = 0.3
    
    # Plot axes of the frame at this joint 
    ax.quiver(pos[0], pos[1], pos[2], R[0, 0], R[1, 0], R[2, 0], color='r', length=scale, label="Frame X-Axis" if i==0 else "") 
    ax.quiver(pos[0], pos[1], pos[2], R[0, 1], R[1, 1], R[2, 1], color='g', length=scale, label="Frame Y-Axis" if i==0 else "")  
    ax.quiver(pos[0], pos[1], pos[2], R[0, 2], R[1, 2], R[2, 2], color='b', length=scale, label="Frame Z-axis" if i==0 else "") 

# Plot lines for links between joints
x_vals = [pos[0] for pos in positions]
y_vals = [pos[1] for pos in positions]
z_vals = [pos[2] for pos in positions]
ax.plot(x_vals, y_vals, z_vals, color='black', linewidth=2)

# Arbitrary graph limits (for now)
ax.set_xlim([-1.3, 1.3])
ax.set_ylim([-1.3, 1.3])
ax.set_zlim([0, 1.3])

ax.set_xlabel('Global X axis')
ax.set_ylabel('Global Y axis')
ax.set_zlabel('Global Z axis')

ax.legend()

plt.show()