#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

mean_distance_front = -1.0
mean_distance_stbd = -1.0



def scan_received(msg, pub):
	""" Processes data from the laser scanner, msg is of type sensor_msgs/LaserScan """
	global mean_distance_front
	global mean_distance_stbd

	print msg.ranges[270]

def approach_wall():
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	sub = rospy.Subscriber('scan', LaserScan, scan_received, pub)
	rospy.init_node('teleop', anonymous=True)
	r = rospy.Rate(10) # 10hz

	while not rospy.is_shutdown():

		#if mean_distance_front != -1.0 and mean_distance_stbd != -1.0:
		print "mean_distance_front: ", mean_distance_front 
		#print "mean_distance_stbd: ", mean_distance_stbd

			
			#gonna hit something, stop forward velocity and twist away until clear
			#if mean_distance_front < 1.0:
				#print "frozen and turning"
        		#velocity_msg = Twist(Vector3(0.0, 0.0, 0.0), Vector3(0.0, 0.0, 0.0))
			#pub.publish(velocity_msg)
        		#r.sleep()
			#otherwise, have forward velocity and keep in line with the wall
			#else:
				#print "maintaining wall distance", (0.05*(mean_distance_stbd - 1.0))
				#velocity_msg = Twist(Vector3(0.5, 0.0, 0.0), Vector3(0.0,0.0,0.5*(mean_distance_stbd - 1.0)))
				#pub.publish(velocity_msg)
        			#r.sleep()
		
if __name__ == '__main__':
    try:
        approach_wall()
    except rospy.ROSInterruptException: pass
