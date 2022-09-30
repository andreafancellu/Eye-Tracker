#Gaze-Tracker

Eye Tracking program in Python that collects data on a user's reading of a text via a laptop webcam and record the audio of the reading.

it's written in Python and the following libraries are needed to run it:

  * cmake
  * opencv-pythhon
  * dlib
  * ffmpeg
  * keyboard
  * numpy
  * pydub
  * scipy
  * sounddevice
  * speechrecognition

The use of a virtual environment is recommended to avoid conflicts with previously installed libraries
  
The code is organized as follows:

  * main: run this file to execute the program
  * classes: contains several classes to represent the data (face_data, gaze_data, key_data)
  * modules: contains several modules that implements the functions used in the main
