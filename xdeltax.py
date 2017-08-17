"""A program using OpenCV and the aruco contrib package to provide a robust
distance and speed caclulating application.  Developed for work on an ongoing
drone project it is a useful resource for any robotics that have a camera
available"""

import sys
import numpy as np
import cv2
import cv2.aruco as aruco
import random
import string

class Camera:
    """This is the main class that holds camera calibration information,
    identification, as well as the necessary distance and speed functions"""

    def __init__(self, session, name, cam_index, length_constant, known_width):
        self.session = session
        self.name = name
        self.cam_index = cam_index
        self.lengthConstant = length_constant
        self.knownWidth = known_width
        self.focalLength = 0
        self.distCoeffs = []
        self.cameraMatrix = np.zeros((3,3))
        self.imgSize = []
        self.cap = None

        with np.load('%s.npz' % self.name) as X:
            self.cameraMatrix, self.distCoeffs, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

        self.focalLength = (self.cameraMatrix[0][0] + self.cameraMatrix[1][1]) / 2


    def __enter__(self):
        self.cap = cv2.VideoCapture(self.cam_index)
        ret, frame = self.cap.read()
        self.imgSize = frame.shape

        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.cap.release()
        cv2.destroyAllWindows()

        if exc_type is not None:
            print exc_type, exc_value, traceback

    def widthInPixels(self, corners):
        topLeft = tuple(corners[0][0])
        topRight = tuple(corners[0][1])
        bottomRight = tuple(corners[0][2])
        bottomLeft = tuple(corners[0][3])

        topWidth = np.sqrt( (topLeft[0] - topRight[0])** 2 + (topLeft[1] - topRight[1])**2)
        bottomWidth = np.sqrt( (bottomLeft[0] - bottomRight[0])** 2 + (bottomLeft[1] - bottomRight[1])**2)
        leftWidth = np.sqrt( (topLeft[0] - bottomLeft[0])** 2 + (bottomLeft[1] - topLeft[1])**2)
        rightWidth = np.sqrt( (topRight[0] - bottomRight[0])** 2 + (bottomRight[1] - topRight[1])**2)

        return (topWidth + bottomWidth + leftWidth + rightWidth) / 4

    def distanceToCamera(self, knownWidth, focalLength, pixWidth):
        # compute and return the distance from the maker to the camera
        return (self.knownWidth * self.focalLength) / pixWidth * self.lengthConstant

    def returnFrame(self):
        aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        parameters =  aruco.DetectorParameters_create()
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        if ids is not None:
            corners = np.array(corners[0])
            rvecs, tvecs = aruco.estimatePoseSingleMarkers(corners, 95.4, self.cameraMatrix, self.distCoeffs)
            rotation = np.zeros((3,3))
            rotation = cv2.Rodrigues(rvecs, rotation)
            points = np.zeros((1,4,2))
            pointsNew = cv2.undistortPoints(corners, self.cameraMatrix, self.distCoeffs, points, rotation[0], self.cameraMatrix)
            width = self.widthInPixels(pointsNew)
            distance = self.distanceToCamera(self.knownWidth, self.focalLength, width)
            cv2.putText(frame, "%.2fft" % (distance), (frame.shape[1] - 300, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        return frame


session = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
name = 'green-black'
cam_index = 1
length_constant = 0.00216995378585
known_width = 95.4

with Camera(session, name, cam_index, length_constant, known_width) as drone:
    while(True):
        frame = drone.returnFrame()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

