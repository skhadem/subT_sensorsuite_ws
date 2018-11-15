#! /usr/bin/env python
from __future__ import division
import math

import rospy
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import TwistStamped, TwistWithCovarianceStamped
from std_msgs.msg import Float64

import sensor_msgs.point_cloud2 as pc2


twist_pub = rospy.Publisher("/twist_estimate", TwistWithCovarianceStamped, queue_size=10)

twist_covariance = [0.01, 0,    0, 0, 0, 0,
                    0,    0.01, 0, 0, 0, 0,
                    0,    0,    0, 0, 0, 0,
                    0,    0,    0, 0, 0, 0,
                    0,    0,    0, 0, 0, 0,
                    0,    0,    0, 0, 0, 0]
def pt_cloud_cb(msg):
    # pts = pc2.read_points(msg, field_names=["x", "y", "doppler"])
    x_vel = 0
    y_vel = 0
    pt_len = 0

    pts = list(pc2.read_points(msg, field_names=["x", "y", "doppler"]))

    for pt in pts:
        if (pt[2] != 0):
            x_vel += -1 * pt[2] * (pt[0] / (math.sqrt(math.pow(pt[0], 2) + math.pow(pt[1], 2))))
            y_vel += -1 * pt[2] * (pt[1] / (math.sqrt(math.pow(pt[0], 2) + math.pow(pt[1], 2))))
            pt_len += 1


    vel_estimate = TwistWithCovarianceStamped()
    vel_estimate.header = msg.header
    vel_estimate.header.frame_id = "base_link"

    vel_estimate.twist.covariance = twist_covariance
    vel_estimate.twist.twist.linear.x = x_vel / pt_len
    vel_estimate.twist.twist.linear.y = y_vel / pt_len

    twist_pub.publish(vel_estimate)


# truth_vel_pub = rospy.Publisher("/truth_vel", Float64, queue_size=10)
# def vel_truth(msg):
#     vx = msg.twist.linear.x
#     vy = msg.twist.linear.y
#
#     v = math.sqrt(math.pow(vx,2) + math.pow(vy,2))
#
#     vel = Float64()
#     vel.data = v
#
#     truth_vel_pub.publish(vel)
#
# estimate_vel_pub = rospy.Publisher("/estimate_vel", Float64, queue_size=10)
# def vel_estimate(msg):
#     vx = msg.twist.linear.x
#     vy = msg.twist.linear.y
#
#     v = math.sqrt(math.pow(vx,2) + math.pow(vy,2))
#
#     vel = Float64()
#     vel.data = v
#
#     estimate_vel_pub.publish(vel)




def main():
    rospy.init_node("doppler_reader")

    mmwave_topic = "/mmWaveDataHdl/RScan"
    sub0 = rospy.Subscriber(mmwave_topic, PointCloud2, pt_cloud_cb)

    # sub1 = rospy.Subscriber("/vrpn_client_node/SubT/twist", TwistStamped, vel_truth)
    # sub2 = rospy.Subscriber("/twist_estimate", TwistStamped, vel_estimate)


    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("shutting down")

if __name__ == '__main__':
    main()
