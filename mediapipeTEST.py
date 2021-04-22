import cv2
import mediapipe as mp
import pyautogui, sys
import time #only used to make a break in between printing the coordinates of the fingers
from scipy.spatial import distance
import logging as log

#logging format
log.basicConfig(filename='Kopi.log', filemode= 'w' , encoding='utf-8', level=log.DEBUG, format='%(asctime)s %(message)s') #Makes a log file that resests every time we restart the program
#log.basicConfig(filename='Kopi.log', encoding='utf-8', level=log.DEBUG, format='%(asctime)s %(message)s') #Makes log file that saves the log from previous runs of our program

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screen_size = pyautogui.size() #returns screen resolution as a tuple list: [x-cordinate, y-coordinate]
window_size_x = screen_size[0] 
window_size_y = screen_size[1] 



# For webcam input:
cap = cv2.VideoCapture(0) #initiates the webcam for use (0 = inbuild camera)

with mp_hands.Hands(
    max_num_hands = 1,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.1) as hands:

  while cap.isOpened():
    pyautogui.FAILSAFE = False
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
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #converts frames to from RGB to BGR
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
          
            
      #move the mouse
      mouseX_offset = window_size_x * (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * 2) # It's the multiplication of 2 that makes the program able to reach the corners
      mouseY_offset = window_size_y * (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * 2)

      middle_finger_mcp_posX = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * mouseX_offset
      middle_finger_mcp_posY = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * mouseY_offset
      pyautogui.moveTo(middle_finger_mcp_posX, middle_finger_mcp_posY, 0.1) # 0.1 makes mouse update in a smoother manor
      
    
      # Index finger tip position
      index_finger_posX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
      index_finger_posY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

      # Thumb tip position
      thumb_posX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
      thumb_posY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

      # Index finger mcp position
      index_finger_mcp_posX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
      index_finger_mcp_posY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

      # Pinky mcp position
      pinky_mcp_posX = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
      pinky_mcp_posY = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y

      # Middle finger tip position
      middle_finger_posX = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
      middle_finger_posY = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

      # Ring finger tip position
      ring_finger_tip_posX = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
      ring_finger_tip_posY = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y

      # Pinky tip position
      pinky_mcp_posX = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
      pinky_mcp_posY = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

      # Left click 
      left_click_dist = round(distance.euclidean([thumb_posX, thumb_posY], [index_finger_mcp_posX, index_finger_mcp_posY]), 3)
      left_click = 0.07
      # print (left_click_dist)
      if left_click_dist < left_click:
        pyautogui.click() 
        print('Left click')
        log.warning (f'Left click registered! Click on X axis:{middle_finger_mcp_posX} Click on Y axis:{middle_finger_mcp_posY}') #Logs a click with coordinates



      # Right click
      right_click_dist = round(distance.euclidean([index_finger_posX, index_finger_posY], [middle_finger_posX, middle_finger_posY]), 3)
      right_click = 0.1
      # print (right_click_dist)
      if right_click_dist > right_click:
        for i in range (0, 2):
          pyautogui.keyDown('command')
          pyautogui.keyUp('command')
          log.warning (f'Right click registered! Click on X axis:{middle_finger_mcp_posX} Click on Y axis:{middle_finger_mcp_posY}') #Logs a click with coordinates
          time.sleep(0.1)

  
      # Mouse drag  
      # drag_dist = round(distance.euclidean([index_finger_posX, index_finger_posY], [index_finger_mcp_posX, index_finger_mcp_posY]), 3)
      # print(drag_dist)
      # drag = 0.05
      # if drag_dist < drag:
      #   pyautogui.drag(button='left')
      #   print('Drag')

      # Scroll down
      scroll_down_dist = round(distance.euclidean([middle_finger_posX, middle_finger_posY], [ring_finger_tip_posX, ring_finger_tip_posY]), 3)
      scroll_down = 0.05
      if scroll_down_dist > scroll_down:
        pyautogui.scroll(-10)
        print('Scroll down')

      
      # Scroll up
      scroll_up_dist = round(distance.euclidean([ring_finger_tip_posX, ring_finger_tip_posY], [pinky_mcp_posX, pinky_mcp_posY]), 3)
      # print(scroll_down_dist)
      scroll_up = 0.09
      if scroll_up_dist > scroll_up:
        pyautogui.scroll(10)
        print('Scroll up')

      
  
    # cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break


  
cap.release()
