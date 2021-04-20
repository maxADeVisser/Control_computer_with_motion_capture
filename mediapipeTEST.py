import cv2
import mediapipe as mp
import pyautogui, sys
import numpy as np
import time #only used to make a break in between printing the coordinates of the fingers
from scipy.spatial import distance
import logging as log

#logging format
log.basicConfig(filename='Kopi.log', filemode= 'w' , encoding='utf-8', level=log.DEBUG, format='%(asctime)s %(message)s') #Makes a log file that resests every time we restart the program
#log.basicConfig(filename='Kopi.log', encoding='utf-8', level=log.DEBUG, format='%(asctime)s %(message)s') #Makes log file that saves the log from previous runs of our program

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#screen_size = pyautogui.size() #returns screen resolution as a tuple list: [x-cordinate, y-coordinate]
#window_size_x = screen_size[0] 
#window_size_y = screen_size[1]

window_size_x = 1280 
window_size_y = 800  


# For webcam input:
cap = cv2.VideoCapture(0) #initiates the webcam for use (0 = inbuild camera)

with mp_hands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.1) as hands:

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
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
          
            
      #Makes the mouse move
      mouseX_offset = window_size_x * (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * 2)
      mouseY_offset = window_size_y * (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * 2)

      middle_finger_mcp_posX = round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x, 3) * mouseX_offset
      middle_finger_mcp_posY = round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y, 3) * mouseY_offset
      pyautogui.moveTo(middle_finger_mcp_posX, middle_finger_mcp_posY, 0.1)
      
      # Euclidean distance index finger tip
      index_finger_posX = round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, 3)
      index_finger_posY = round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y, 3)

      # Euclidean distance thumb tip
      thumb_posX = round(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x, 3)
      thumb_posY = round(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y, 3)

      # Euclidean distance index finger mcp
      index_finger_mcp_posX = round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x, 3)
      index_finger_mcp_posY = round(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y, 3)

      # Euchlidean distiance pinky mcp
      pinky_mcp_posX = round(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x, 3)
      pinky_mcp_posY = round(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y, 3)

      # Euchlidean distance middle finger tip
      middle_finger_posX = round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x, 3)
      middle_finger_posY = round(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y, 3)

      # Left click 
      # left_click_dist = np.linalg.norm(thumb - index_finger_mcp)
      left_click_dist = round(distance.euclidean([thumb_posX, thumb_posY], [index_finger_mcp_posX, index_finger_mcp_posY]), 3)
      left_click = 0.07
      # print (left_click_dist)
      if left_click_dist < left_click:
        pyautogui.click() 
        print('Left click')
        log.warning (f'Left click registered! Click on X axis:{thumb_cmc_posX} Click on Y axis:{thumb_cmc_posY}') #Logs a click with coordinates



      # Right click
      # right_click_dist = np.linalg.norm(thumb - pinky_mcp)
      right_click_dist = round(distance.euclidean([index_finger_posX, index_finger_posY], [middle_finger_posX, middle_finger_posY]), 3)
      right_click = 0.1
      # print (right_click_dist)
      if right_click_dist > right_click:
        for i in range (0, 2):
          pyautogui.keyDown('command')
          pyautogui.keyUp('command')
          log.warning (f'Right click registered! Click on X axis:{thumb_cmc_posX} Click on Y axis:{thumb_cmc_posY}') #Logs a click with coordinates
          time.sleep(0.1)


        # pyautogui.click(button = 'right')
        # print('Right click')
  
      # Mouse drag  
      # drag_dist = round(distance.euclidean([index_finger_posX, index_finger_posY], [index_finger_mcp_posX, index_finger_mcp_posY]), 3)
      # print(drag_dist)
      # drag = 0.05
      # if drag_dist < drag:
      #   pyautogui.drag(button='left')
      #   print('Drag')
      
    
    # cv2.imshow('MediaPipe Hands', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
      break


  
cap.release()
