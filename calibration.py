import argparse
import os
import sys

parser = argparse.ArgumentParser(description='This script enables you to save your cameraMatrix as a numpy array which will be used for the processing of images in order to determine distance and speed from an aruco tag')
parser.add_argument('cam_index', metavar='C', type=int, nargs='+',
                    help='cam_index for opencv to read video from 0 is usally built in webcam')
parser.add_argument('output_filename', metavar='O', type=str, nargs='+',
                    help='name of output file to save np.array to')
args = parser.parse_args()
##checks file doesn't exist already
if os.path.isfile(args.output_filename[0] + ".npz"):
    print("File already exists")
    sys.exit()

import numpy as np
import cv2
import cv2.aruco as aruco
from tqdm import trange
import datetime

#Sets opencv camera
cam_index= args.cam_index[0]
cap=cv2.VideoCapture(cam_index)

#Sets aruco constants
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
board = aruco.CharucoBoard_create(5,7,0.03,0.019,aruco_dict)
parameters =  aruco.DetectorParameters_create()

#arrays
corners = []
ids = []
rejectedImagePoints = []
charucoCorners = []
charucoIds = []
allCharucoIds = []
allCharucoCorners = []

#calibration output variables
cameraMatrix = None
distCoeffs = None
rvecs = None
tvecs = None
calibrationFlags = 0

print("Aquiring Images For Calibration Move your Camera Around to Capture Different Angles")
for x in trange(15):
    charucoCorners = []
    while len(charucoCorners)<3:
        #read and process image
        ret, frame=cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #Detect Marker
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if len(corners) > 0:
            ret, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(corners, ids, gray, board)
            if charucoCorners is not None and charucoIds is not None and len(charucoCorners)>3:
                allCharucoCorners.append(charucoCorners)
                allCharucoIds.append(charucoIds)
                cv2.waitKey(3000)
                break

print("All images Aquired Running Calibration")
#release and close
cap.release()
cv2.destroyAllWindows()

imgSize = gray.shape
result, mtx, dist, rvecs, tvecs = aruco.calibrateCameraCharuco(allCharucoCorners, allCharucoIds, board, imgSize, None, None)
np.savez(args.output_filename[0], ret=result, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
