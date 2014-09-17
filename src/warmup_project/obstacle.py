#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

y_total = 0
x_total = 0

def scan_received(msg, pub):
	y_total = 0
	x_total = 0
	for i in range(360):
		if msg.ranges[i] > 0 and msg.ranges[i] < 8: #valid range
			y_total = y_total + math.cos(i)*msg.ranges[i] # negative values go backward
			x_total = x_total + math.sin(i)*msg.ranges[i] # negative values turns right				

	

def approach_wall():
	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	sub = rospy.Subscriber('scan', LaserScan, scan_received, pub)
	rospy.init_node('teleop', anonymous=True)
	r = rospy.Rate(10) # 10hz
	
	while not rospy.is_shutdown():
		linear = 1 + -(.5*y_total)
		ang = .5*x_total # negative turns right
		velocity_msg = Twist(Vector3(linear, 0.0, 0.0), Vector3(0.0, 0.0, ang))
		pub.publish(velocity_msg)
		r.sleep()
		print "linear: ", linear, " ang: ", ang
 
if __name__ == '__main__':
	try:
		approach_wall()
	except rospy.ROSInterruptException: pass


