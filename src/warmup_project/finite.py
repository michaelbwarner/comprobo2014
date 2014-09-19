#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

state = 0 #0=wall following, 1=obstacle avoidance

stbd_dist = -1.0
front_dist = -1.0
stbd_target = 0.3
front_target = 2.0	

y_total = 0
x_total = 0

def get_avg_range(msg, target):

	valid_ranges = []
	for i in range(5):
		cur = msg.ranges[i+target-3]
		if cur  > 0 and cur < 8:
			valid_ranges.append(cur)
	if len(valid_ranges) > 0:
		return sum(valid_ranges)/float(len(valid_ranges))
	else:
		return -1.0


def scan_received(msg, pub):

	back_dist = get_avg_range(msg, 180)
	if back_dist != -1.0 and back_dist < 2: #if something is chasing it, go to obstacle avoidance
		state = 1
	else: 
		state = 0
	
	if state == 0:
		
		front_dist = get_avg_range(msg, 0)
		stbd_dist = get_avg_range(msg, 270)
		back_dist = get_avg_range(msg, 180)
		
	else:
		global y_total
		global x_total
		y_total = 0
        	x_total = 0
        	for i in range(360):
                	if msg.ranges[i] > 0 and msg.ranges[i] < 2: #valid range
                        	y_total = y_total + math.cos(i)*(2-msg.ranges[i]) # negative values go backward
                       	 	x_total = x_total + math.sin(i)*(2-msg.ranges[i]) # negative values turns right

def publish(msg, pub, linear, ang):

	velocity_msg = Twist(Vector3(linear, 0.0, 0.0), Vector3(0.0, 0.0, ang))
	pub.publish(velocity_msg)
	r.sleep()				

		
def approach_wall():

	pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	sub = rospy.Subscriber('scan', LaserScan, scan_received, pub)
	rospy.init_node('teleop', anonymous=True)
	r = rospy.Rate(10) # 10hz
	
	while not rospy.is_shutdown():
		if state == 0: #wall following
			if stbd_dist != -1.0:
				if front_dist != -1.0 and front_dist < front_target:
					ang = -1.0*(front_dist - front_target)
					publish(msg, pub, 0.0, ang)
					print "front control: ", front_dist, " control: ", ang)
       				else:
					#turning to the right is negative twist
					ang = -0.5*(stbd_dist - stbd_target)
					publish(msg, pub, .05, ang)
					print "stbd control: ", stbd_dist, " control: ", control)
        		else:
				publish(msg, pub, 0.0, 0.0)
				print "invalid stbd"

		else: #obstacle avoidance
	                linear = 1 + -(.5*y_total)
  			ang = .5*x_total # negative turns right
			publish(msg, pub, linear, ang)
               		print "linear: ", linear, " ang: ", ang


if __name__ == '__main__':
	try:
		approach_wall()
	except rospy.ROSInterruptException: pass


