# -*- coding: utf-8 -*-
#
#
# Author: alex
# Created Time: 2018年12月30日 星期日 15时36分26秒
import cv2
import numpy as np
from copy import deepcopy
import math

# parameters
cap_region_width = 320
cap_region_height = 400
threshold = 60  # BINARY threshold
blurValue = 41  # GaussianBlur parameter

# Length of the history
bgHistoryLen = 10

# 背景移除的方差阀值，用于判断当前像素是前景还是背景。
# 一般默认16，如果光照变化明显，如阳光下的水面，建议设为25,36，
# 值越大，灵敏度越低；
bgSubThreshold = 50

# learningRate(0~1)配置背景更新方法，
# 0表示不更新，
# 1表示根据最后一帧更新，
# 负数表示自动更新，(0~1)数字越大，背景更新越快。
learningRate = 0

# variables
isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works


def print_threshold(thr):
    print("Changed threshold to "+str(thr))


def remove_bg(frame):
    # 背景分割器
    fgmask = bgModel.apply(frame, learningRate=learningRate)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res


def calculate_fingers(res, drawing):  # -> finished bool, cnt: finger count
    #  convexity defect
    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        # if type(defects) != type(None):  # avoid crashing.   (BUG not found)
        if defects is not None:  # avoid crashing.   (BUG not found)
            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            return True, cnt
    return False, 0


def get_output_drawing(thresh):
    """"""
    thresh1 = deepcopy(thresh)
    _, contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    if length == 0:
        return None

    maxArea = -1
    for i in range(length):  # find the biggest contour (according to area)
        temp = contours[i]
        area = cv2.contourArea(temp)
        if area > maxArea:
            maxArea = area
            ci = i

    res = contours[ci]
    hull = cv2.convexHull(res)
    drawing = np.zeros(img.shape, np.uint8)
    cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

    isFinishCal, cnt = calculate_fingers(res, drawing)
    if triggerSwitch is True and isFinishCal is True and cnt <= 2:
        print(cnt)

    return drawing


# Camera
camera = cv2.VideoCapture(0)
camera.set(10, 200)
cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, print_threshold)

# read background image
bg_img = cv2.imread('./bg.png')

while camera.isOpened():
    _, frame = camera.read()
    threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    point_x = frame.shape[1] - cap_region_width
    point_y = cap_region_height
    cv2.rectangle(frame, (point_x, 0), (frame.shape[1], point_y),
                  (255, 0, 0), 2)
    cv2.imshow('original', frame)

    # Main operation
    img = None
    if isBgCaptured == 1:  # this part wont run until background captured
        img = frame
        img = img[0:point_y, point_x:frame.shape[1]]  # clip the ROI
        img = remove_bg(img)
        new_img = cv2.erode(img, None, iterations=1)
        new_img = cv2.dilate(new_img, None, iterations=1)
        mask_img = deepcopy(bg_img)
        for x in range(cap_region_width):
            for y in range(cap_region_height):
                if all(new_img[y, x]) is False:
                    continue
                mask_img[y, x] = img[y, x]

        cv2.imshow('mask', mask_img)

        """
        # convert the image into binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        cv2.imshow('blur', blur)
        _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('ori', thresh)

        # get the coutours
        drawing = get_output_drawing(thresh)
        if drawing is not None:
            cv2.imshow('output', drawing)
        """

    # Keyboard OP
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break
    elif k == ord('b'):  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorMOG2(bgHistoryLen,
                                                     bgSubThreshold)
        isBgCaptured = 1
        print('Background Captured: MOG2!')
    elif k == ord('k'):  # press 'b' to capture the background
        bgModel = cv2.createBackgroundSubtractorKNN(bgHistoryLen,
                                                    bgSubThreshold)
        isBgCaptured = 1
        print('Background Captured: KNN!')
    elif k == ord('g'):
        bgModel = cv2.bgsegm.createBackgroundSubtractorGMG(bgHistoryLen,
                                                           bgSubThreshold)
        isBgCaptured = 1
        print('Background Captured: GMG!')
    elif k == ord('r'):  # press 'r' to reset the background
        bgModel = None
        triggerSwitch = False
        isBgCaptured = 0
        print('Reset BackGround!')
    elif k == ord('n'):
        if triggerSwitch is False:
            triggerSwitch = True
            print('Trigger On!')
        else:
            triggerSwitch = False
            print('Trigger Off!')
    elif k == ord('d'):
        print("point: %d  %d" % (point_x, point_y), frame.shape)
        print(frame[0, 0])
        print(img[0, 0])
