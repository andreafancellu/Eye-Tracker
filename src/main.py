from threading import Thread
from classes.key_data import KeyTime
from classes.gaze_data import GazeData
from modules.calibration import calibration_fase
from modules.audio import *
from modules.constants import *
from modules.tracking import *
import dlib
import cv2
import numpy as np


calibration_fase()

# text user will read 
text_list = []
with open('resources/text.txt', 'r') as f:
    text_list = f.readlines()

cap = cv2.VideoCapture(0)

dataset_gaze = np.array([])
dataset_face = np.array([])
dataset_face_all = np.array([])
dataset_keys = np.array([])

text_frame = np.zeros([1080, 1920, 3], dtype=np.uint8)
text_frame.fill(255)

key_pressed = KeyTime(0, 0)

click_counter = 0
once_counter = 0

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"resources\shape_predictor_68_face_landmarks.dat")

stopThread = False
thread_audio = Thread(target=record_audio)
thread_audio.start()

starting_time = time.time()

while True:

    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        ms = current_milli_time(starting_time)

        # Face Tracking
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 10), 2)
        landmarks = predictor(gray, face)
        cv2.polylines(frame, [DRAW_FACE], True, (255, 255, 255), 2)
        cv2.circle(frame, CENTER_FACE, radius=1, color=(0, 0, 255), thickness=1)

        # Blinking Detection
        left_eye_blink_ratio = get_blinking_ratio(LEFT_EYE_ARRAY, landmarks, frame)
        right_eye_blink_ratio = get_blinking_ratio(RIGHT_EYE_ARRAY, landmarks, frame)
        medium_blink_ratio = (right_eye_blink_ratio + left_eye_blink_ratio) / 2

        if medium_blink_ratio > 5.2:
            cv2.putText(frame, "BLINKING", (25, 300), FONT, 0.8, (255, 0, 0), 3)

        # Face Movement Detection
        face_ratio = get_face_ratio(FACE_REGION, landmarks, frame, ms)
        face_all_ratio = get_face_all_ratio(FACE_REGION, landmarks, frame, ms)

        # Gaze Detection X
        gaze_ratio_right_eye_X = get_gaze_ratio_X(RIGHT_EYE_ARRAY, landmarks, frame, gray)
        gaze_ratio_left_eye_X = get_gaze_ratio_X(LEFT_EYE_ARRAY, landmarks, frame, gray)
        gaze_ratio_X = round(((gaze_ratio_left_eye_X + gaze_ratio_right_eye_X) / 2), 2)

        if gaze_ratio_X > 2.5:
            gaze_ratio_X = 2.5
            
        cv2.putText(frame, str(gaze_ratio_X), (25, 150), FONT, 1, (0, 0, 255), 3)

        # Gaze Detection Y
        gaze_ratio_Y = round(get_gaze_ratio_Y(landmarks, frame),0)
        #cv2.putText(frame, str(gaze_ratio_Y), (25, 225), FONT, 0.9, (0, 255, 255), 3)

        # Graphic Interface
        if click_counter == 1:
            cv2.putText(text_frame, "INVIO: pagina successiva", (630, 400), FONT, 1, (0, 0, 0), 1)
            cv2.putText(text_frame, "BACKSPACE: pagina precedente", (630, 450), FONT, 1, (0, 0, 0), 1)
            cv2.putText(text_frame, "ESC: termina simulazione", (630, 500), FONT, 1, (0, 0, 0), 1)
            cv2.imshow('Text', text_frame)

        if click_counter == 2:
            if once_counter == 0:
                text_frame.fill(255)
                once_counter += 1
            cv2.imshow('Text', text_frame)
            for i in range(int(len(text_list)/2)):
                cv2.putText(text_frame, text_list[i].strip('\n'), (5, i*50+100), FONT, 0.85, (0, 0, 0), 1)

        if click_counter == 3:
            if once_counter == 1:
                text_frame.fill(255)
                once_counter += 1
            cv2.imshow('Text', text_frame)
            for i in range(int(len(text_list)/2), len(text_list)):
                cv2.putText(text_frame, text_list[i].strip('\n'), (5, (i-int(len(text_list)/2))*50+100), FONT, 0.85, (0, 0, 0), 1)

        if click_counter == 4:
            if once_counter == 2:
                text_frame.fill(255)
                once_counter += 1
            cv2.imshow('Text', text_frame)
            cv2.putText(text_frame, "Premi ESC per terminare", (400, 400), FONT, 2, (0, 0, 0), 1)

        # Saving Data
        gaze = GazeData(gaze_ratio_X, ms, gaze_ratio_Y)
        dataset_gaze = np.append(dataset_gaze, gaze)
        dataset_face = np.append(dataset_face, face_ratio)
        dataset_face_all = np.append(dataset_face_all, face_all_ratio)

    cv2.imshow('Eye Tracker', frame)
    key = cv2.waitKey(1)

    # Handling keys pressed 
    if key == 27: # ESC
        stopThread = True
        break
    if key == 13: # ENTER
        click_counter += 1
        key_pressed = KeyTime(key, ms)
    if key == 8: # BACKSPACE
        click_counter -= 1
        once_counter -= 2
        key_pressed = KeyTime(key, ms)

    if key_pressed.get_key() == 13 or key_pressed.get_key() == 8:
        dataset_keys = np.append(dataset_keys, key_pressed) 

cap.release()
cv2.destroyAllWindows()
thread_audio.join()

save_dataset(dataset_gaze, "data\gaze.txt")
save_dataset(list(dict.fromkeys(dataset_keys)), "data\keys.txt")
save_dataset(dataset_face, "data\\face.txt")
save_dataset(dataset_face_all, "data\\face_all.txt")
