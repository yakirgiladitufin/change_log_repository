import numpy as np
import cv2
import pyscreenshot as ImageGrab
from pyautogui import *

if __name__ == '__main__':
    screenshot = ImageGrab.grab()
    screenshot.save('screenshot.png')

    img_rgb = cv2.imread('screenshot.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('esc.png',0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    
    threshold = 0.8
    loc = np.where( res >= threshold)
   
    if loc[1]:
        x = loc[1][0] + w/2
        y = loc[0][0] + h/2

        counter = 0
        print(x,y)
        moveTo(x,y,0.2)

    # read('C_driver.png',0)
# cv2.imshow('image',img)
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key t
