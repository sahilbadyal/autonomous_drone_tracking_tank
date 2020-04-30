from subprocess import Popen
import random
import time
from object_detection.object_detection import objectdetector
from sensor_msgs.msg import Joy
from image_view.srv import save as saveSrv
import os
import rospy

joystickPublisher = None

os.environ["TFHUB_CACHE_DIR"] = '/home/local/ASUAD/sbadyal/Spring2020/autonomous_drone_tracking_tank/python/object_detection/model'

def stop(pub):
    """
    time.sleep(0.5)
    p = Popen(["rostopic","pub", "/joy", "sensor_msgs/Joy", "header:\n  seq: 0\n  stamp:\n    secs: 185\n    nsecs: 469000000\n  frame_id: ''\naxes: [-0.0, -0.0, -0.0, -0.0, 0.0, 0.0]\nbuttons: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"], shell=False)
    time.sleep(1)
    p.kill()
    """
    joyMsg = Joy()
    numAxes = 6
    joyMsg.axes = [0.0 for _ in range(numAxes)]
    pub.publish(joyMsg)


def move(pub, x, y, secs):
    """
    time.sleep(0.5)
    p = Popen(["rostopic","pub", "/joy", "sensor_msgs/Joy", "header:\n  seq: 0\n  stamp:\n    secs: 185\n    nsecs: 469000000\n  frame_id: ''\naxes: ["+str(x)+","+str(y)+", -0.0, -0.0, 0.0, 0.0]\nbuttons: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"], shell=False)
    time.sleep(secs)
    p.kill()
    """
    joyMsg = Joy()
    numAxes = 6
    joyMsg.axes = [0.0 for _ in range(numAxes)]
    joyMsg.axes[0] = x
    joyMsg.axes[1] = y
    pub.publish(joyMsg)
    time.sleep(secs)
    # uncomment this if you want to call stop from within move automagically
    #stop(pub)


def save_image():
    """
    p = Popen(["rosservice", "call", "/image_saver/save"], shell=False)
    """
    serviceName = '/image_saver/save'
    rospy.wait_for_service(serviceName)
    try:
        saveImage = rospy.ServiceProxy(serviceName, saveSrv)
        saveImage()
    except rospy.ServiceException as e:
        print('Service call failed: {}'.format(e))

#stop() 
#move(-0.0, 0.1, abs(max([-0.1,0], key=abs)))
#stop()

od = objectdetector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")

print("Initialized Object Detector")

def run():
    joyTopicName = 'joy' 
    pub = rospy.Publisher(joyTopicName, Joy, queue_size=10)
    results = []
    numberList1 = [x * 0.1 for x in range(-7, 8)]
    #print(numberList1)
    x = random.choice(numberList1)
    y = random.choice(numberList1)
    order = abs(max([x,y], key=abs))
    secs = 0.7
    print(order, secs)
    print("Aage")
    move(pub, x, y, secs)
    stop(pub)
    save_image()
    results.append([str(x) for x in od.run('./data/foo.jpg')])
    print("Peeche")
    move(pub, -x, -y, secs)
    stop(pub)
    save_image()
    results.append([str(x) for x in od.run('./data/foo.jpg')])
    return x, y, secs, results

with open('dataSetlarge.csv','w') as f:
    prevState = ['0.5','0.5']
    for x in range(1000):
        x,y,s,r = run()
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
