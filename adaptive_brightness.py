"""
Changes display brightness to match webcam brightness.
2021-05-05 v1.0 by Cees Timmerman
"""

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


def main(debug=False):
    if debug: cv2.namedWindow("preview")
    vc = cv2.VideoCapture(1)
    print(vc)

    if not vc.isOpened():
        print(f"Can't open cam! {vc}")

    original_brightness = sbc.get_brightness(display=0)
    brightness = original_brightness
    while True:
        rval, frame = vc.read()
        if not rval: break

        if debug: cv2.imshow("preview", frame)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

        # Change brightness to match webcam brightness.
        brightness = int(100 * get_brightness(frame))
        sbc.fade_brightness(brightness, display=0)
        time.sleep(1)

    vc.release()
    if debug: cv2.destroyWindow("preview")


if __name__ == "__main__":
    main()
