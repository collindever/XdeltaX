# XdeltaX
With the use of opencv and its aruco module this script allows for calibration of a video camera, and distance calculation of a charuco tag given its size.  The advantage of using the aruco library is it accounts for viewing angle and lens distortion.  This provide a more accurate measurement and does not require the object to be viewed head on.

## Calibration
This is simply a script that runs the [aruco.calibrateCameraCharuco](https://docs.opencv.org/3.3.0/da/d13/tutorial_aruco_calibration.html) function.  It requires command line arguments of the cam_index as well as a filename for the output [numpy matrix](https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html).  The more diverse viewing angles the more accurate the results that why there is a pause included for 3 seconds after the board is detected for you to move the camera to a different angle. The script capture 15 images before running the calibration and provides a progress bar.

## Distance
This loads a camera matrix created by the calibration script, and implements an instance of a camera class.  This was done to allow for use of threading in future applications. the class requires you to set the variables on lines 87 - 90 however you can use the provided values for lines 89 and 90 if you print out and use test_marker0.jpg at the size it is.
```python
name = "the name you gave the output of the calibration script"
cam_index = "camera your using"
length_constant = "since our calibration is in a unit of pixels this is a constant for pixel to feet conversion"
known_width = "this is the width of our aruco marker in pixels"
```
The distance is calculated for each side of the square and the value returned is an average of the 4. We were able to get readings with +/- 1cm accuracy with a standard definition camera.

### To-Do
* Add velocity calculation
* Make the units consistent removing the need for conversion
