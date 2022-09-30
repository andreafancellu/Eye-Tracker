import dlib
import cv2
import numpy as np
from .constants import *
from .tracking import *


def calibration_fase():

    calibration_text =[]
    with open("resources\calibration.txt", "r") as file:
        calibration_text = file.readlines()
    file.close

    cap = cv2.VideoCapture(0)

    # schermata di lettura
    text_frame = np.zeros([1080, 1920, 3], dtype=np.uint8)
    text_frame.fill(255)

    # modelli per face detection
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(r"resources\shape_predictor_68_face_landmarks.dat")

    # contatori per gestire l'andamento del testo durante la calibrazione
    click_counter = 0
    once_counter = 0

    while True:
        
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:

            cv2.polylines(frame, [DRAW_FACE], True, (255, 255, 255), 2)
            cv2.circle(frame, CENTER_FACE, radius=1, color=(0, 0, 255), thickness=1)

            landmarks = predictor(gray, face)

            gaze_ratio_right_eye_X = get_gaze_ratio_X(RIGHT_EYE_ARRAY, landmarks, frame, gray)
            gaze_ratio_left_eye_X = get_gaze_ratio_X(LEFT_EYE_ARRAY, landmarks, frame, gray)
            gaze_ratio_X = round(((gaze_ratio_left_eye_X + gaze_ratio_right_eye_X) / 2), 2)
            cv2.putText(frame, str(gaze_ratio_X), (25, 255), FONT, 0.6, (0, 255, 255), 3)

            if click_counter == 0:
                cv2.putText(frame, "Posiziona il tuo volto al centro di quello evidenziato",
                            (10, 20), FONT, 0.7, (255, 255, 255), 1)
                cv2.putText(frame, "Premi INVIO per avviare la calibrazione",
                            (10, 50), FONT, 0.9, (255, 255, 255), 1)

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
                for i in range(len(calibration_text)):
                    cv2.putText(text_frame, calibration_text[i].strip('\n'), (10, i*50+100), FONT, 0.85, (0, 0, 0), 1)
                    
            if click_counter == 3:
                if once_counter == 1:
                    text_frame.fill(255)
                    once_counter += 1
                cv2.imshow('Text', text_frame)
                cv2.putText(text_frame, "Premi ESC per avviare la simulazione", (5, 400), FONT, 2, (0, 0, 0), 1)

        cv2.imshow('Calibrazione', frame)

        key = cv2.waitKey(1)
        if key == 27:
            stopThread = True
            break
        if key == 13:
            click_counter += 1
        if key == 8:
            click_counter -= 1
            once_counter -= 2


    cap.release()
    cv2.destroyAllWindows()
