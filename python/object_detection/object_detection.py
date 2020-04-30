# -*- coding: utf-8 -*-
#@title Imports and function definitions

# For running inference on the TF-Hub module.
import tensorflow as tf

import tensorflow_hub as hub

import numpy as np

# For downloading the image.

from object_detection.od_utils import *

# For measuring the inference time.
import time

import os

# Print Tensorflow version
print(tf.__version__)

# Check available GPU devices.
print("The following GPU devices are available: %s" % tf.test.gpu_device_name())


os.environ["TFHUB_CACHE_DIR"] = '/home/local/ASUAD/sbadyal/Spring2020/autonomous_drone_tracking_tank/python/object_detection/model'


class objectdetector(object):

  def __init__(self, handle):
    self.detector = hub.load(handle).signatures['default']

  def __load_img(self, path):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    return img

  def run(self, path):
    img = self.__load_img(path)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    start_time = time.time()
    result = self.detector(converted_img)
    end_time = time.time()

    result = {key:value.numpy() for key,value in result.items()}

    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)

    #ind = np.unravel_index(np.argmax(result['detection_scores'], axis=None), result['detection_scores'].shape)
    arr = np.array([str(x) for x in result["detection_class_entities"]])
    print(arr, type(arr))
    index = np.where(arr=="b'Ball'")
    if(len(index[0])==0):
        return []
    ind = index[0][0]
    db = np.array([result["detection_boxes"][ind]])
    dce = np.array([result["detection_class_entities"][ind]])
    ds = np.array([result["detection_scores"][ind]])
    image_with_boxes = draw_boxes(
        img.numpy(), db,
        dce, ds)
    #image_with_boxes = draw_boxes(
    #    img.numpy(), result["detection_boxes"],
    #    result["detection_class_entities"], result["detection_scores"])

    #display_image(image_with_boxes)
    centerY = db[0][0] +  (db[0][2] - db[0][0])/2 
    centerX = db[0][1] +  (db[0][3] - db[0][1])/2 
    return (centerX, centerY)



if __name__=='__main__':

  """### More images
  Perform inference on some additional images with time tracking.
  """
  """Pick an object detection module and apply on the downloaded image. Modules:
  * **FasterRCNN+InceptionResNet V2**: high accuracy,
  * **ssd+mobilenet V2**: small and fast.

  """
  module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]
  
  image_urls = ["https://images.unsplash.com/photo-1489087433598-048557455f41?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80"]
  detector = objectdetector(module_handle)
  for image_url in image_urls:
    start_time = time.time()
    #image_path = download_and_resize_image(image_url, 640, 480)
    image_path = '../simulation/data/foo.jpg'
    print(image_path)
    bounded_box_image = detector.run(image_path)
    end_time = time.time()
    print("Inference time:",start_time-end_time)
    print(bounded_box_image)
