#!/usr/bin/env python

import rospy
#from turtlesim.msg import Pose
from beginner_tutorials.msg import cipheredPose
from random import randint #Para generar numeros pseudoaleatorios
from Crypto.Cipher import AES



def coordGenerator():
    
    
    rospy.init_node('coordinates_generator', anonymous=True)

    pub = rospy.Publisher('turtleAutoMove', cipheredPose, queue_size=10)

    pose = cipheredPose()

    rate = rospy.Rate(0.2) #Cada 5 segundos un mensaje

    rospy.sleep(1) #Con este sleep se evita perder el primer mensaje

    

    while not rospy.is_shutdown():
    	x = str(randint(0,11))
    	y = str(randint(0,11))
        hello_str = "Generada nueva posicion con x= %s && y= %s" %(x,y)
        rospy.loginfo(hello_str)
        pose.x = x
        pose.y = y
        pose.theta = '0'
        pose.angular_velocity = '0'
        pose.linear_velocity = '0'
        pose = addPadding(pose)    
        rospy.loginfo(pose)
        pose = encryptMessage(pose)    
        rospy.loginfo(pose)
        pub.publish(pose)
        rate.sleep()

def addPadding(pose):
    pose.x = pose.x.rjust(16, '0')
    pose.y = pose.y.rjust(16, '0')
    pose.theta = pose.theta.rjust(16, '0')
    pose.angular_velocity = pose.angular_velocity.rjust(16, '0')
    pose.linear_velocity = pose.linear_velocity.rjust(16, '0')
    return pose

def encryptMessage(pose):
    e = AES.new('Esto es la clave. Razvan', AES.MODE_CBC, 'Vector inicializ')
    pose.x = e.encrypt(pose.x)
    pose.y = e.encrypt(pose.y)
    pose.theta = e.encrypt(pose.theta)
    pose.angular_velocity = e.encrypt(pose.angular_velocity)
    pose.linear_velocity = e.encrypt(pose.linear_velocity)
    return pose

if __name__ == '__main__':
    try:
        coordGenerator()
    except rospy.ROSInterruptException:
        pass

