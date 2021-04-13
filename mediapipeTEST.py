import cv2
import mediapipe as mp
import pyautogui, sys
import numpy as np
import time #only used to make a break in between printing the coordinates of the fingers

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

screen_size = pyautogui.size() #returns screen resolution as a tuple list: [x-cordinate, y-coordinate]
window_size_x = screen_size[0]
window_size_y = screen_size[1]

# For webcam input:
cap = cv2.VideoCapture(0) #initiates the webcam for use (0 = inbuild camera)
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
            #alters whether the coordinates of the fingers are printed to the terminal
        """ print(
          f'Thumb tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y})'
      )  """

      #Makes the mouse move
      pyautogui.moveTo(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].x * 
      window_size_x, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * window_size_y)
      
      # #Euclidean distance index finger tip
      # index_finger_posX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
      # index_finger_posY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

      # #Euclidean distance thumb tip
      # thumb_posX = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
      # thumb_posY = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

      # #Euclidean distance index finger mcp
      # index_finger_mcp_posX = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
      # index_finger_mcp_posY = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y

      # #Euchlidean distiance pinky mcp
      # pinky_mcp_posX = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x
      # pinky_mcp_posY = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y

      index_finger = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y))
      thumb = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x,hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y))
      index_finger_mcp = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y))
      pinky_mcp = np.array((hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x, hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y))

      index_finger_rounded = np.round(index_finger, 2)
      thumb_rounded = np.round(thumb, 2)
      index_finger_mcp_rounded = np.round(index_finger_mcp, 2)
      pinky_mcp_rounded = np.round(pinky_mcp, 2)

      # index_finger = np.around([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x], decimals= 3), np.around([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y], decimals= 3)
      # thumb = np.around([hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x], decimals= 3), np.around([hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y], decimals= 3)
      # index_finger_mcp = np.around([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x], decimals= 3), np.around([hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y], decimals= 3)
      # pinky_mcp = np.around([hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x], decimals= 3), np.around([hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y], decimals= 3)

      # index_finger = np.array((round(index_finger_posX, 3), round(index_finger_posY, 3)))
      # thumb = np.array((round(thumb_posX, 3), round(thumb_posY, 3)))
      # index_finger_mcp = np.array((round(index_finger_mcp_posX, 3), round(index_finger_mcp_posY, 3)))
      # index_finger = np.array((round(index_finger_posX, 3), round(index_finger_posY, 3)))
      # pinky_mcp = np.array((round(pinky_mcp_posX, 3), round(pinky_mcp_posY, 3)))

      

      # click functionalitet
      #Click 
      left_click_dist = np.linalg.norm(thumb - index_finger_mcp)
      left_click = 0.04
      #print(left_click_dist)
      if left_click_dist < left_click:
        pyautogui.click() 
        print('Left click')


      # Right click
      right_click_dist = np.linalg.norm(thumb - pinky_mcp)
      right_click = 0.04
      if right_click_dist < right_click:
        #pyautogui.click(button = 'right')
        print('Right click')
  
      # Mouse drag  
      drag_dist = np.linalg.norm(index_finger_mcp - index_finger_mcp)
      # print(drag_dist)
      drag = 0.05
      # if drag_dist > drag:
      #   pyautogui.mouseUp()
      # if drag_dist < drag:
      #   pyautogui.mouseDown()
      #   print('Drag')
      

    # cv2.imshow('MediaPipe Hands', image)
    
    if cv2.waitKey(5) & 0xFF == 27:
      break
    
cap.release()

