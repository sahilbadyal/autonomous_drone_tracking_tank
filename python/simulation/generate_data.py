from subprocess import Popen
import random
import time
from object_detection.object_detection import objectdetector
import os

os.environ["TFHUB_CACHE_DIR"] = '/home/local/ASUAD/sbadyal/Spring2020/autonomous_drone_tracking_tank/python/object_detection/model'

def stop():
    p = Popen(["rostopic","pub", "/joy", "sensor_msgs/Joy", "header:\n  seq: 0\n  stamp:\n    secs: 185\n    nsecs: 469000000\n  frame_id: ''\naxes: [-0.0, -0.0, -0.0, -0.0, 0.0, 0.0]\nbuttons: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"], shell=False)
    time.sleep(1)
    p.kill()

def move(x ,y, secs):
    p = Popen(["rostopic","pub", "/joy", "sensor_msgs/Joy", "header:\n  seq: 0\n  stamp:\n    secs: 185\n    nsecs: 469000000\n  frame_id: ''\naxes: ["+str(x)+","+str(y)+", -0.0, -0.0, 0.0, 0.0]\nbuttons: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]"], shell=False)
    time.sleep(secs)
    p.kill()

def save_image():
    p = Popen(["rosservice", "call", "/image_saver/save"], shell=False)

#stop() 
#move(-0.0, 0.1, abs(max([-0.1,0], key=abs)))
#stop()

od = objectdetector("https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")

print("Initialized Object Detector")

def run():
    results = []
    numberList1 = [x * 0.1 for x in range(-10, 10)]
    print(numberList1)
    x = random.choice(numberList1)
    y = random.choice(numberList1)
    order = abs(max([x,y], key=abs))
    secs = 1 
    print(order, secs)
    move(x, y, secs)
    stop()
    save_image()
    results.append([str(x) for x in od.run('./data/foo.jpg')])
    move(-x, -y, secs)
    stop()
    save_image()
    results.append([str(x) for x in od.run('./data/foo.jpg')])
    return x, y, secs, results

with open('dataSet.csv','w') as f:
    for x in range(50):
        x,y,s,r = run()
        f.write(','.join((str(x), str(y), str(s))))
        f.write(',')
        f.write(','.join(r[0]))
        f.write('\n')
        f.write(','.join((str(-x), str(-y), str(s))))
        f.write(',')
        f.write(','.join(r[1]))
        f.write('\n')