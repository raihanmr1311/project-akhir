from streamlit_webrtc import webrtc_streamer
import av
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2
from playsound import playsound

EYE_ASPECT_RATIO_THRESHOLD = 0.2

EYE_ASPECT_RATIO_CONSEC_FRAMES = 60

face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")


def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear = (A+B) / (2*C)
    return ear

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

video_capture = cv2.VideoCapture(0)
time.sleep(2)

def video_frame_callback(frame, COUNTER = 0):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)

        face_rectangle = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in face_rectangle:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        for face in faces:
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

            leftEyeAspectRatio = eye_aspect_ratio(leftEye)
            rightEyeAspectRatio = eye_aspect_ratio(rightEye)

            eyeAspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(img, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(img, [rightEyeHull], -1, (0, 255, 0), 1)
            if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
                if COUNTER < EYE_ASPECT_RATIO_CONSEC_FRAMES:
                    COUNTER += 1
                    video_frame_callback(frame=frame, COUNTER=COUNTER)
                elif COUNTER >= EYE_ASPECT_RATIO_CONSEC_FRAMES:
                    cv2.putText(img, "Anda sedang mengantuk", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                    playsound(u'beep-warning.wav')
                    # return av.VideoFrame.from_ndarray(img, format="bgr24")
            else:
                COUNTER = 0
                # video_frame_callback(frame=frame, COUNTER=COUNTER)
                # return av.VideoFrame.from_ndarray(img, format="bgr24")
            return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback)