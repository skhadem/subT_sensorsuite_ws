#! /usr/bin/env python

import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped

transform = tf.TransformBroadcaster()

def run(msg):
    t = TransformStamped()
    t.child_frame_id = msg.child_frame_id
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = msg.header.frame_id

    t.transform.translation.x = msg.pose.pose.position.x
    t.transform.translation.y = msg.pose.pose.position.y
    t.transform.translation.z = msg.pose.pose.position.z

    t.transform.rotation.x = msg.pose.pose.orientation.x
    t.transform.rotation.y = msg.pose.pose.orientation.y
    t.transform.rotation.z = msg.pose.pose.orientation.z
    t.transform.rotation.w = msg.pose.pose.orientation.w

    transform.sendTransformMessage(t)




if __name__ == '__main__':
    rospy.init_node('pose_to_tf')
    pose_topic = "/vrpn_client/_________/pose"
    d = rospy.Subscriber(pose_topic, Odometry, run) # check this topic
    rospy.loginfo("Subscribing to %s"%pose_topic)
    rospy.spin()
