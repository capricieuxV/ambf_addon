import bpy
import pybullet as p
from mathutils import Matrix

# Example Blender object
blender_object = bpy.context.active_object

# Create a Bullet physics world
physicsClient = p.connect(p.DIRECT)
p.setGravity(0, 0, -9.81)

# Get Blender object properties
location = blender_object.location
rotation = blender_object.rotation_euler.to_quaternion()
scale = blender_object.scale
mass = blender_object.rigid_body.mass
collision_shape = blender_object.rigid_body.collision_shape
friction = blender_object.rigid_body.friction
restitution = blender_object.rigid_body.restitution
linear_damping = blender_object.rigid_body.linear_damping
angular_damping = blender_object.rigid_body.angular_damping

# Set Bullet collision shape
if collision_shape == 'BOX':
    half_extents = [s / 2 for s in scale]
    bullet_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)
elif collision_shape == 'SPHERE':
    bullet_collision_shape = p.createCollisionShape(p.GEOM_SPHERE, radius=scale.x)
# Add other collision shapes as needed

# Create Bullet rigid body
bullet_body = p.createMultiBody(
    baseMass=mass,
    baseCollisionShapeIndex=bullet_collision_shape,
    basePosition=location,
    baseOrientation=rotation
)

# Set Bullet properties
p.changeDynamics(bullet_body, -1, friction=friction, restitution=restitution)
p.changeDynamics(bullet_body, -1, linearDamping=linear_damping, angularDamping=angular_damping)

# Continue with the simulation
p.stepSimulation()
