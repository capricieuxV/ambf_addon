import bpy
import rospy
from geometry_msgs.msg import PoseStamped

# Specify the name of the Blender object to track
object_name = "Cube"

# ROS node and publisher setup
rospy.init_node('blender_object_publisher')
pub = rospy.Publisher('/blender_object_pose', PoseStamped, queue_size=10)

def publish_object_pose():
    # Get the specified object from the Blender scene
    obj = bpy.data.objects[object_name]

    # Retrieve the object's position
    position = obj.location

    # Create a PoseStamped message
    pose_msg = PoseStamped()
    pose_msg.header.stamp = rospy.Time.now()
    pose_msg.header.frame_id = "blender"
    pose_msg.pose.position.x = position.x
    pose_msg.pose.position.y = position.y
    pose_msg.pose.position.z = position.z

    # Publish the object's pose
    pub.publish(pose_msg)

if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            publish_object_pose()
            rospy.Rate(10).sleep()  # Publish at 10 Hz
    except rospy.ROSInterruptException:
        pass