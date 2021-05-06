"""
Changes display brightness to match webcam brightness.
2021-05-05 v1.0 by Cees Timmerman
2021-05-06 v1.0.1 tested on Debian 10 in VMware.
"""
import sys
import time

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
        return np.average(img) / 255


def main(camera=-1, display=0, debug=False):
    if debug:
        # https://github.com/opencv/opencv/issues/14535
        import os

        os.environ["OPENCV_VIDEOIO_DEBUG"] = "1"

    import cv2

    if debug:
        try:
            cv2.namedWindow("preview")
        except Exception as ex:
            print(ex)

    if camera < 0:
        for camera in range(10):
            vc = cv2.VideoCapture(camera)
            if vc.isOpened():
                break

    if not vc.isOpened():
        print(f"Can't open camera {camera}, {vc}")
        return
    print(f"Using camera {camera}, {vc.getBackendName()}, {vc}")

    if debug:

        def cv2_prop_name(v):
            d = vars(cv2)
            return [k for k in d if d[k] == v and k.startswith("CAP_PROP_")]

        for i in range(100):
            names = cv2_prop_name(i)
            value = vc.get(i)
            if not names or value == -1.0:
                continue
            print(f"Prop {i}, {cv2_prop_name(i)}: {vc.get(i)}")

    vc.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
    vc.set(cv2.CAP_PROP_FPS, 1)

    original_brightness = sbc.get_brightness(display)
    brightness = original_brightness
    try:
        while True:
            rval, frame = vc.read()
            if not rval:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            if debug:
                try:
                    cv2.imshow("preview", frame)
                except:
                    pass

            # Change brightness to match webcam brightness.
            brightness = int(100 * get_brightness(frame))
            sbc.set_brightness(brightness, display)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    sbc.set_brightness(original_brightness)
    vc.release()
    if debug:
        try:
            cv2.destroyWindow("preview")
        except:
            pass


if __name__ == "__main__":
    camera = -1
    display = 0
    debug = False
    try:
        debug = "debug" in sys.argv
        camera = int(sys.argv[1])
        display = int(sys.argv[2])
    except (IndexError, ValueError):
        pass

    main(camera, display, debug)
