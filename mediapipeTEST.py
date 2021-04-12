import cv2
import mediapipe as mp
import pyautogui, sys
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
window_size_x = 1280
window_size_y = 800

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        """ print(
          f'Thumb tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y})'
      )  """

      #Makes the mouse move
      pyautogui.moveTo(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x * window_size_x, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * window_size_y)
      
      #Euclidean distance index finger tip
      # index_finger_posX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
      # index_finger_posY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

      #Euclidean distance thumb tip
      thumb_posX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
      thumb_posY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

      # Euchlidean distance index finger mcp
      index_finger_mcp_posX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
      index_finger_mcp_posY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

      #index_finger = np.array((index_finger_posX, index_finger_posY))
      thumb = np.array((thumb_posX, thumb_posY))
      index_finger_mcp = np.array((index_finger_mcp_posX, index_finger_mcp_posY))
      
      dist = np.linalg.norm(thumb - index_finger_mcp)
      print(dist)
      click = 0.04
      if dist < click:
        pyautogui.click() 
        print('Click')
  
    cv2.imshow('MediaPipe Hands', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
      break
    
cap.release()