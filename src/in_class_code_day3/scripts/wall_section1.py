#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

mean_distance = -1.0

def scan_received(msg, pub):
	""" Processes data from the laser scanner, msg is of type sensor_msgs/LaserScan """
	global mean_distance
	valid_ranges = []
	for i in range(5):
		if msg.ranges[i] > 0 and msg.ranges[i] < 8:
		valid_ranges.append(msg.ranges[i])
	if len(valid_ranges) > 0:
		mean_distance = sum(valid_ranges)/float(len(valid_ranges))
	else:
		mean_distance = -1.0
	print mean_distance

def approach_wall():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber('scan', LaserScan, scan_received, pub)
    rospy.init_node('teleop', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if mean_distance != -1.0:
            velocity_msg = Twist(Vector3(0.2*(mean_distance - 1.0), 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
        pub.publish(velocity_msg)
        r.sleep()
        
if __name__ == '__main__':
    try:
        approach_wall()
    except rospy.ROSInterruptException: pass
