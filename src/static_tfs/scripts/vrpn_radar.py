#! /usr/bin/env python

import rospy
import tf

from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TransformStamped
from sensor_msgs.msg import PointCloud2

transform = tf.TransformBroadcaster()
rdr_fwd_ptcloud_pub = rospy.Publisher("radar_fwd/mmWave_repub", PointCloud2, queue_size=10)
rdr_lat_ptcloud_pub = rospy.Publisher("radar_lat/mmWave_repub", PointCloud2, queue_size=10)

def pose_repub(msg):
    t = TransformStamped()
    t.child_frame_id = "base_link"
    t.header.stamp = rospy.Time(0)
    t.header.frame_id = msg.header.frame_id

    t.transform.translation.x = msg.pose.position.x
    t.transform.translation.y = msg.pose.position.y
    t.transform.translation.z = msg.pose.position.z

    t.transform.rotation.x = msg.pose.orientation.x
    t.transform.rotation.y = msg.pose.orientation.y
    t.transform.rotation.z = msg.pose.orientation.z
    t.transform.rotation.w = msg.pose.orientation.w

    transform.sendTransformMessage(t)

def fwd_ptcloud_repub(msg):
    msg.header.frame_id = "base_link"
    # msg.header.stamp = rospy.Time(0)
    rdr_fwd_ptcloud_pub.publish(msg)

def lat_ptcloud_repub(msg):
    msg.header.frame_id = "base_link"
    # msg.header.stamp = rospy.Time(0)
    rdr_lat_ptcloud_pub.publish(msg)

def main():
    rospy.init_node('pose_tf')
    pose_topic = "/vrpn_client_node/SubT/pose"
    pose_sub = rospy.Subscriber(pose_topic, PoseStamped, pose_repub)

    mmwave_topic = "/mmWaveDataHdl/RScan"
    radar_fwd_sub = rospy.Subscriber("/radar_fwd"+mmwave_topic, PointCloud2, fwd_ptcloud_repub)
    radar_lat_sub = rospy.Subscriber("/radar_lat"+mmwave_topic, PointCloud2, lat_ptcloud_repub)

    rospy.loginfo("Subscribing to %s", pose_topic)
    rospy.loginfo("Subscribing to %s", "/radar_fwd"+mmwave_topic)
    rospy.loginfo("Subscribing to %s", "/radar_lat"+mmwave_topic)

    r = rospy.Rate(10)      # 10 Hz
    while not rospy.is_shutdown():
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: # ctrl-c
        pass

    rospy.spin()
