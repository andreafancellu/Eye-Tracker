from modules.operations import *
from classes.face_data import Face, FaceAll
from math import hypot
import numpy as np
import cv2

def get_blinking_ratio(eye_points, facial_landmarks, frame):

    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    # hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    # ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    ver_line_len = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    hor_line_len = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))

    if ver_line_len == 0:
        ver_line_len = 0.0000001

    ratio = hor_line_len / ver_line_len

    return ratio


def get_gaze_ratio_X(eye_points, facial_landmarks, frame, gray):

    eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                           (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                           (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                           (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                           (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                           (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)

    # massimo e minimo della regione dell'occhio
    min_x = np.min(eye_region[:, 0])
    max_x = np.max(eye_region[:, 0])
    min_y = np.min(eye_region[:, 1])
    max_y = np.max(eye_region[:, 1])

    # creo una maschera per selezionare solo l'occhio
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [eye_region], True, (255, 255, 255), 2)
    cv2.fillPoly(mask, [eye_region], (255, 255, 255))
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    gray_eye = eye[min_y:max_y, min_x:max_x]

    # conversione in immagine binaria
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height_eye, width_eye = threshold_eye.shape

    # conteggio parti bianche
    right_side = threshold_eye[0:height_eye, 0:int(width_eye / 2)]
    right_side_white = cv2.countNonZero(right_side)
    left_side = threshold_eye[0:height_eye, int(width_eye / 2):width_eye]
    left_side_white = cv2.countNonZero(left_side)

    #cv2.imshow("right", right_side)
    #cv2.imshow("left", left_side)

    if left_side_white == 0:
        left_side_white = 0.0000001

    gaze_ratio_sx_dx = right_side_white / left_side_white

    return gaze_ratio_sx_dx


def get_gaze_ratio_Y(facial_landmarks, frame):

    right_eye_up = midpoint(facial_landmarks.part(19), facial_landmarks.part(20))
    right_eye_down = midpoint(facial_landmarks.part(37), facial_landmarks.part(38))
    # cv2.line(frame, right_eye_up, right_eye_down, (255, 0, 0), 2)
    right_len = hypot((right_eye_up[0] - right_eye_down[0]), (right_eye_up[1] - right_eye_down[1]))

    left_eye_up = midpoint(facial_landmarks.part(23), facial_landmarks.part(23))
    left_eye_down = midpoint(facial_landmarks.part(43), facial_landmarks.part(44))
    # cv2.line(frame, left_eye_up, left_eye_down, (255, 0, 0), 2)
    left_len = hypot((left_eye_up[0] - left_eye_down[0]), (left_eye_up[1] - left_eye_down[1]))

    medium_len = (right_len + left_len) / 2

    return medium_len


def get_face_ratio(face_points, facial_landmarks, frame, ms):

    face_region = np.array([(facial_landmarks.part(face_points[0]).x, facial_landmarks.part(face_points[0]).y),
                           (facial_landmarks.part(face_points[1]).x, facial_landmarks.part(face_points[1]).y),
                           (facial_landmarks.part(face_points[2]).x, facial_landmarks.part(face_points[2]).y),
                           (facial_landmarks.part(face_points[3]).x, facial_landmarks.part(face_points[3]).y)], np.int32)

    height, width, _ = frame.shape
    half_height = height//2
    half_width = width//2
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [face_region], True, (255, 255, 255), 2)
    cv2.fillPoly(mask, [face_region], (255, 255, 255))
    #cv2.imshow("mask", mask)

    right_part = mask[:, :half_width]
    left_part = mask[:, half_width:]
    top_part = mask[:half_height, :]
    bottom_part = mask[half_height:, :]

    white_right_part = cv2.countNonZero(right_part)
    white_left_part = cv2.countNonZero(left_part)
    white_top_part = cv2.countNonZero(top_part)
    white_bottom_part = cv2.countNonZero(bottom_part)

    '''cv2.imshow("left", left_part)
    cv2.imshow("right", right_part)
    cv2.imshow("top", top_part)
    cv2.imshow("bottom", bottom_part)'''

    return Face(white_right_part, white_left_part, white_top_part, white_bottom_part, ms)


def get_face_all_ratio(face_points, facial_landmarks, frame, ms):

    face_region = np.array([(facial_landmarks.part(face_points[0]).x, facial_landmarks.part(face_points[0]).y),
                           (facial_landmarks.part(face_points[1]).x, facial_landmarks.part(face_points[1]).y),
                           (facial_landmarks.part(face_points[2]).x, facial_landmarks.part(face_points[2]).y),
                           (facial_landmarks.part(face_points[3]).x, facial_landmarks.part(face_points[3]).y)], np.int32)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [face_region], True, (255, 255, 255), 2)
    cv2.fillPoly(mask, [face_region], (255, 255, 255))
    face = cv2.countNonZero(mask)
    #cv2.imshow("mask", mask)

    return FaceAll(face, ms)