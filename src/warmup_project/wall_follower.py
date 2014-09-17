#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

stbd_dist = -1.0
front_dist = -1.0
stbd_target = 0.3
front_target = 2.0	

def scan_received(msg, pub):
	""" Processes data from the laser scanner, msg is of type sensor_msgs/LaserScan """
	global front_dist
	valid_ranges = []
	for i in range(5):
		if msg.ranges[i] > 0 and msg.ranges[i] < 8:
			valid_ranges.append(msg.ranges[i])
	if len(valid_ranges) > 0:
		front_dist = sum(valid_ranges)/float(len(valid_ranges))
	else:
		front_dist = -1.0

	#print "front_dist: ", front_dist	

	target = 270
	global stbd_dist
	valid_ranges = []
	for i in range(5):
		cur = msg.ranges[i+target-3]
		if cur  > 0 and cur < 8:
			valid_ranges.append(cur)
	if len(valid_ranges) > 0:
		stbd_dist = sum(valid_ranges)/float(len(valid_ranges))
	else:
		stbd_dist = -1.0

	#print "stbd_dist: ", stbd_dist

def approach_wall():
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	sub = rospy.Subscriber('scan', LaserScan, scan_received, pub)
	rospy.init_node('teleop', anonymous=True)
	r = rospy.Rate(10) # 10hz
	
	while not rospy.is_shutdown():
		if stbd_dist != -1.0:
			if front_dist != -1.0 and front_dist < front_target:
				control = -1.0*(front_dist - front_target)
				velocity_msg = Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, control))
				pub.publish(velocity_msg)
				r.sleep()
				print "front control: ", front_dist, " control: ", control)
       			else:
				#turning to the right is negative twist
				control = -0.5*(stbd_dist - stbd_target)
				velocity_msg = Twist(Vector3(0.05, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
				pub.publish(velocity_msg)
				r.sleep()
				print "stbd control: ", stbd_dist, " control: ", control)
        	else:
			velocity_msg = Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
			pub.publish(velocity_msg)
			r.sleep()
			print "invalid stbd"
 
if __name__ == '__main__':
	try:
		approach_wall()
	except rospy.ROSInterruptException: pass


