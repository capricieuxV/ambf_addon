import bpy
import mathutils

# Assume camera_object is the camera object in Blender
camera_object = bpy.context.active_object

# Get the rotation matrix from the camera's current rotation
rot_mat = camera_object.matrix_world.to_3x3()

# Extract the camera's forward, right, and up vectors
forward = -rot_mat.col[2].normalized()  # Negative Z-axis
right = rot_mat.col[0].normalized()     # X-axis
up = rot_mat.col[1].normalized()        # Y-axis

# The camera's world location
cam_location = camera_object.matrix_world.translation

# Calculate the look_at point
up = right.cross(forward)
look_at = cam_location + forward

print("Camera Location:", cam_location)
print("Look At:", look_at)
print("Up Direction:", up)
