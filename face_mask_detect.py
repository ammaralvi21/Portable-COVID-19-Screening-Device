# MIT License
#
# Copyright (c) 2019 Iván de Paz Centeno
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import cv2
import os
import tensorflow as tf
import numpy as np
from tensorflow import keras




#scale_percent = 60 # percent of original size

#def change_res(width, height):
  #  cap.set(3, width)
 #   cap.set(4, height)


#change_res(224, 224)

#minimum_brightness = 1.6


class  face_mask_detect:
    def __init__(path):
        self.model = keras.models.load_model(path)
        self.font = cv2.FONT_HERSHEY_SIMPLEX    # font
        self.org = (00, 00)                     # org 
        self.fontScale = 0.7                    # fontScale 
        self.color = (0, 0, 255)                # Red color in BGR 
        self.thickness = 2


    
    def detect_mask(self,(x1,y1), (x2,y2), image):
        self.x1 = x1 - 20
        self.y1 = y1 - 20
        self.x2 = x2 + 20
        self.y2 = y2 + 50
        self.crop_img = image[self.y1:self.y2, self.x1:self.x2]
        if self.crop_img.size > 0:
            self.out_of_range = 0
            dim = (224, 224)
            img_resized = cv2.resize(self.crop_img, dim, interpolation=cv2.INTER_LINEAR)
            img_resized = np.expand_dims(img_resized, axis=0)
           
            prob = self.model.predict(img_resized)
            self.is_detected = np.argmax(prob, axis=1)
            self.prob_mask = prob[0][1]
            self.prob_no_mask = prob[0][0]
        else
            self.out_of_range = 1

        return
   
            

    
    
'''    

while(True):
    # Capture frame-by-frame

    # Our operations on the frame come here 
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # loop over various values of gamma

    #image = cv2.resize(image, (0,0), fx = 0.3, fy = 0.3)
    
    

   # model.predict(crop_img)
    if result:
    # Result is an array with all the bounding boxes detected. We know that for 'ivan.jpg' there is only one.
        bounding_box = result[0]['box']
        #keypoints = result[0]['keypoints']
        x1 = bounding_box[0] - 20
        y1 = bounding_box[1] - 10
        x2 = bounding_box[0] + bounding_box[2] + 20
        y2 = bounding_box[1] + bounding_box[3] + 50
        cv2.rectangle(image,
                    (x1,y1),
                    (x2,y2),
                    (0,155,255),
                    2)
        crop_img = image[y1:y2, x1:x2]

        cols, rows, x = crop_img.shape
        brightness = np.sum(crop_img) / (255 * cols * rows)
        ratio = brightness / minimum_brightness
        if ratio < 1:
            image = cv2.convertScaleAbs(image, alpha = (1 / ratio), beta = 0)
            crop_img = image[y1:y2, x1:x2]

        cv2.putText(image, "={}".format(ratio), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        #
        # Display the resulting frame
        if crop_img.size > 0:
            dim = (224, 224)
            img_resized = cv2.resize(crop_img, dim, interpolation=cv2.INTER_LINEAR)
            img_resized = np.expand_dims(img_resized, axis=0)
           
            predIdxs = model.predict(img_resized)
            predIdxs = np.argmax(predIdxs, axis=1)
            org = (x1 - 10, y1 - 10)
            image = cv2.putText(image, str(predIdxs) + "  " + str(image.size), org, font, fontScale, color, thickness, cv2.LINE_AA, False)  

            #print(predIdxs)
            cv2.imshow('frame',cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        else:
            cv2.imshow('frame',cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

'''