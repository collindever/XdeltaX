"""A program using OpenCV and the aruco contrib package to provide a robust
distance and speed caclulating application.  Developed for work on an ongoing
drone project it is a useful resource for any robotics that have a camera
available"""

import sys

def main():
    """Main entry point for the script."""
    pass

if __name__ == '__main__':
    sys.exit(main())

class Camera:
    """This is the main class that holds camera calibration information,
    identification, as well as the necessary distance and speed functions"""

    def __init__(self, id):
        self.id = id
        
