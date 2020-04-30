from subprocess import Popen
import random
import time
from object_detection.object_detection import objectdetector
from sensor_msgs.msg import Joy
#from image_view.srv import save as saveSrv
import os
import rospy

joystickPublisher = None

os.environ["TFHUB_CACHE_DIR"] = '/home/local/ASUAD/sbadyal/Spring2020/autonomous_drone_tracking_tank/python/object_detection/model'

class gazebo_interface():

    def __init__(self):
        rospy.init_node("gazebo_iterface")
        joyTopicName = 'joy' 
        self.pub = rospy.Publisher(joyTopicName, Joy, queue_size=10)
        self.od = objectdetector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")

    
    def stop(self):
        joyMsg = Joy()
        numAxes = 6
        joyMsg.axes = [0.0 for _ in range(numAxes)]
        joyMsg.buttons = [0 for _ in range(numAxes * 2)]
        self.pub.publish(joyMsg)


    def move(self,x, y, secs=0.5):
        joyMsg = Joy()
        numAxes = 6
        joyMsg.axes = [0.0 for _ in range(numAxes)]
        joyMsg.buttons = [0 for _ in range(numAxes * 2)]
        joyMsg.axes[0] = x
        joyMsg.axes[1] = y
        self.pub.publish(joyMsg)
        time.sleep(secs)
        # uncomment this if you want to call stop from within move automagically
        self.stop()


    def save_image(self):
        p = Popen(["rosservice", "call", "/image_saver/save"], shell=False)

    def getObservation(self, x, y):
        self.move(x, y)
        self.save_image()
        return self.od.run('./data/foo.jpg')



if __name__=='__main__':
    print("Initialized Object Detector")
    gz = gazebo_interface()
    
    def run(gz):
        results = []
        numberList1 = [x * 0.1 for x in range(-7, 8)]
        #print(numberList1)
        x = random.choice(numberList1)
        y = random.choice(numberList1)
        secs = 0.1
        results.append([str(i) for i in gz.getObservation(x,y)])
        results.append([str(i) for i in gz.getObservation(-x,-y)])
        
        return x, y, secs, results

    with open('dataSetlarge.csv','w') as f:
        prevState = ['0.5','0.5']
        for x in range(1000):
            x,y,s,r = run(gz)
            f.write(','.join(prevState))
            f.write(',')
            f.write(','.join((str(x), str(y), str(s))))
            f.write(',')
            f.write(','.join(r[0]))
            f.write('\n')
            f.write(','.join(r[0]))
            f.write(',')
            f.write(','.join((str(-x), str(-y), str(s))))
            f.write(',')
            f.write(','.join(r[1]))
            f.write('\n')
            prevState = r[1].copy()
