"""
Changes display brightness to match webcam brightness.
2021-05-05 v1.0 by Cees Timmerman
2021-05-06 v1.0.1 tested on Debian 10 in VMware.
"""
import sys
import time

import cv2
import numpy as np
from numpy.linalg import norm
import screen_brightness_control as sbc


def get_brightness(img):
    """Returns average brightness, 0 to 1.
    https://stackoverflow.com/a/62780132/819417"""
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return (np.average(norm(img, axis=2)) / np.sqrt(3)) / 255
    else:
        # Grayscale
        return np.average(img)/255


def main(camera=-1, display=0, debug=False):
    if debug:
        cv2.namedWindow("preview")

    for i in range(camera, 10):
        vc = cv2.VideoCapture(i)
        if vc.isOpened():
            print(f"Using camera {i} {vc}")
            vc.set(cv2.CAP_PROP_FOURCC,
                   cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            vc.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            vc.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
            vc.set(cv2.CAP_PROP_FPS, 1)
            break

    original_brightness = sbc.get_brightness(display)
    brightness = original_brightness
    try:
        while True:
            rval, frame = vc.read()
            if not rval:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if debug:
                cv2.imshow("preview", frame)

            # Change brightness to match webcam brightness.
            brightness = int(100 * get_brightness(frame))
            sbc.set_brightness(brightness, display)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    sbc.set_brightness(original_brightness)
    vc.release()
    if debug:
        cv2.destroyWindow("preview")


if __name__ == "__main__":
    camera = -1
    display = 0
    debug = False
    try:
        camera = int(sys.arv[1])
        display = int(sys.argv[2])
        debug = "debug" in sys.argv
    except:
        pass
    main(camera, display, debug)