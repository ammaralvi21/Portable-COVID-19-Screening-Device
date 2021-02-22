"""trt_mtcnn.py

This script demonstrates how to do real-time face detection with
Cython wrapped TensorRT optimized MTCNN engine.
"""

import time
import argparse
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf, GObject
import cv2
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.mtcnn import TrtMtcnn
from facemask_model_api import FaceMask
import numpy as np
import threading
import time
import ctypes
import smbus
STM32_ADDRESS = 0x40
# Open i2c device @/dev/i2c-1, addr 0x40.
bus = smbus.SMBus(1)



WINDOW_NAME = 'TrtMtcnnDemo'
BBOX_COLOR = (0, 255, 0)  # green
minimum_brightness = 1.5

def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time face detection with TrtMtcnn on Jetson '
            'Nano')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_camera_args(parser)
    parser.add_argument('--minsize', type=int, default=200,
                        help='minsize (in pixels) for detection [40]')
    args = parser.parse_args()
    return args           

args = parse_args()
cam = Camera(args)

if not cam.isOpened():
    raise SystemExit('ERROR: failed to open camera!')



def app_main():
    win = Gtk.Window(default_height=720, default_width=1024)
    win.connect("destroy", Gtk.main_quit)
    win.fullscreen()
    label = Gtk.Label(label="This is a normal label")
    image = Gtk.Image()
    #win.add(label)
    win.add(image)
    #win.add(label)

    def update_progess():
        data = bus.read_byte(STM32_ADDRESS)
        label.set_text(str(data))
        return False

    def redraw_screen():
        win.remove(image)
        win.add(label)
        win.show_all()
        return False

    def Mask_Detect_Phase():
        """Continuously capture images from camera and do face detection."""

        run = True
        fps = 0.0
        tic = time.time()
        mtcnn = TrtMtcnn()
        FaceMaskObj = FaceMask('face_mask_detection_model_TFTRT_FP16')
        myROICnt = 0
        old_dets = np.array([[30, 10, 100, 80, 9.980469e-01]])
        confidence_buffer = np.zeros(30)
        conf_cnt = 0
        prog_bar = 30
        while run:
            img = cam.read()
            if img is not None:
                cols, rows, x = img.shape
                brightness = np.sum(img) / (255 * cols * rows)
                ratio = brightness / minimum_brightness
                if ratio < 1:
                    img = cv2.convertScaleAbs(img, alpha = (1 / ratio), beta = 0)
                #faces = faceDetector.detect(img)
                dets, landmarks = mtcnn.detect(img, minsize=200)
                
     
                #print('{} face(s) found'.format(len(dets)))
                #print(dets)
                #dets = np.array([[300, 100, 1000, 800, 9.980469e-01]])
                if dets.any():
                    old_dets = dets
                    myROICnt = 0
                    img, confidence, class_id = FaceMaskObj.detect(roi=dets,image=img)
                    if (class_id) and (confidence > 0.85):
                        confidence_buffer[conf_cnt] = confidence
                        conf_cnt = conf_cnt + 1
                        prog_bar = prog_bar + 20
                        cv2.rectangle(img, (30, 0), (prog_bar, 50), (255, 255, 0), -1)
                    else:
                        confidence_buffer.fill(0.0)
                        conf_cnt = conf_cnt + 1
                        prog_bar = 100   
                elif myROICnt < 6:
                    myROICnt = myROICnt + 1
                    img, confidence, class_id = FaceMaskObj.detect(roi=old_dets,image=img)
                    if (class_id) and (confidence > 0.85):
                        confidence_buffer[conf_cnt] = confidence
                        conf_cnt = conf_cnt + 1
                        prog_bar = prog_bar + 20
                        cv2.rectangle(img, (100, 0), (prog_bar, 50), (255, 255, 0), -1)
                    else:
                        confidence_buffer.fill(0.0)
                        conf_cnt = conf_cnt + 1
                        prog_bar = 100                    
                else:
                    confidence_buffer.fill(0.0)
                    prog_bar = 0
                    
                if (conf_cnt >= 30):
                    conf_cnt = 0

                print(confidence_buffer)
                print(np.mean(confidence_buffer))
                conf_mean = np.mean(confidence_buffer)
                if (conf_mean >= 0.9):
                    run = False
                    cv2.putText(img, "Mask Successfully Detected", (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA, False)
                    
                #img = show_faces(img, dets, landmarks)
                img = show_fps(img, fps)
                h, w, d = img.shape
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                pixbuf = GdkPixbuf.Pixbuf.new_from_data(img.tostring(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w*d)                

                GLib.idle_add(image.set_from_pixbuf,pixbuf.copy()) 
                       
                                   
                toc = time.time()
                curr_fps = 1.0 / (toc - tic)
                # calculate an exponentially decaying average of fps number
                fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
                tic = toc

    def MyThread():
        state = 1
        while True:
            if state == 1:
                Mask_Detect_Phase()
                time.sleep(2)
                GLib.idle_add(redraw_screen) 
                state = 2
                print ("changing state")
            elif state == 2:
                time.sleep(0.2)
                GLib.idle_add(update_progess)
           


    win.show_all()

    thread = threading.Thread( target = MyThread )
    thread.daemon=True 
    thread.start()




def loop_and_detect(cam, minsize):

    print("\n.............object created...............\n")
    while True:
        if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
            break
        img = cam.read()
        if img is not None:
            cols, rows, x = img.shape
            brightness = np.sum(img) / (255 * cols * rows)
            ratio = brightness / minimum_brightness
            if ratio < 1:
                img = cv2.convertScaleAbs(img, alpha = (1 / ratio), beta = 0)
            #faces = faceDetector.detect(img)
            dets, landmarks, class_id = mtcnn.detect(img, minsize=minsize)

 
            #print('{} face(s) found'.format(len(dets)))
            #print(dets)
            #dets = np.array([[300, 100, 1000, 800, 9.980469e-01]])
            if dets.any():
                img = FaceMaskObj.detect(roi=dets,image=img)
            #img = show_faces(img, dets, landmarks)
            img = show_fps(img, fps)
            cv2.imshow(WINDOW_NAME, img)
            toc = time.time()
            curr_fps = 1.0 / (toc - tic)
            # calculate an exponentially decaying average of fps number
            fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
            tic = toc
        key = cv2.waitKey(1)
        if key == 27:  # ESC key: quit program
            break
        elif key == ord('F') or key == ord('f'):  # Toggle fullscreen
            full_scrn = not full_scrn
            set_display(WINDOW_NAME, full_scrn)


def main():
    
    bus.write_byte(STM32_ADDRESS, 0x03)
    app_main()
    Gtk.main()
    cam.release()
    


if __name__ == '__main__':
    main()
