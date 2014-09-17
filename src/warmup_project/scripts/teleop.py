#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3

def getch():

	""" Return the next character typed on the keyboard """
	import sys, tty, termios
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)

	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)

	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def teleop():

	pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
	rospy.init_node('my_keyboard_teleop', anonymous=True)
	turn_vel = .4
	linear_vel = 1
	while not rospy.is_shutdown():
		c = getch()
		if c == 'i':
			pub.publish(Twist(linear=Vector3(x=linear_vel)))
		elif c == 'u':
			pub.publish(Twist(linear=Vector3(x=linear_vel),angular=Vector3(z=turn_vel)))
		elif c == 'o':
			pub.publish(Twist(linear=Vector3(x=linear_vel), angular=Vector3(z=-turn_vel)))
		elif c == 'j':
			pub.publish(Twist(angular=Vector3(z=turn_vel)))
		elif c == 'l':
			pub.publish(Twist(angular=Vector3(z=-turn_vel)))
		elif c == 'm':
			pub.publish(Twist(linear=Vector3(x=-linear_vel), angular=Vector3(z=-turn_vel)))
		elif c == ',': 
			pub.publish(Twist(linear=Vector3(x=-linear_vel)))
		elif c == '.':
			pub.publish(Twist(linear=Vector3(x=-linear_vel), angular=Vector3(z=turn_vel)))
		elif c == 'q':
			break
		else:
			pub.publish(Twist())

if __name__ == '__main__':
	try:
		teleop()
	except rospy.ROSInterruptException: pass



