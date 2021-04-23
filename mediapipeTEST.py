# Controlling a computer through motioncapture
# The project was created for the exam handin for the course Interactive Digital System at Roskilde University
# Created by: Max de Visser, William Dyrnesli Kristensen, Simon Hindsgaul, Martin Emil Daa Funder and Sebastian Rohr

# -----------------------------------SETUP-------------------------------------------- #

import mediapipe as mp
import pyautogui, sys, cv2
from scipy.spatial import distance
import logging as log
import speech_recognition as sr

#logging format
log.basicConfig(filename='Kopi.log', filemode= 'w' , encoding='utf-8', level=log.DEBUG, format='%(asctime)s %(message)s') #Makes a log file that resests everytime the program is ran
#log.basicConfig(filename='Kopi.log', encoding='utf-8', level=log.DEBUG, format='%(asctime)s %(message)s') #This line can be used instead if we want to make new logfiles each time

mp_drawing = mp.solutions.drawing_utils # the 'drawing' of the handdetection model. 
mp_hands = mp.solutions.hands # initializing MediaPipes hand landmark model

screen_size = pyautogui.size() #returns screen resolution as a tuple: [x-cordinate, y-coordinate]
window_size_x = screen_size[0] # a variable to represent the screen width
window_size_y = screen_size[1] # a variable to represent the screen height
# OBS: PyAutoGui sees the screen as a cartesian coordinate-system with the origin (0,0) being the upper left corner

# using OpenCV for webcamera input:
cap = cv2.VideoCapture(0) #instanciates a VideoCapture object needed for capturing live video from webcam (0 is usually the build-in camera). 
# OBS: If using an external webcamera, try different numbers (1, 2, 3 etc.)

r = sr.Recognizer() # Initialize the speech-recognizer

with mp_hands.Hands( # with-statement ensures we handle possible exceptions thrown
    max_num_hands = 1, # Declares how many hands the model will track at once.
    min_detection_confidence = 0.5, # a normalized value (0-1) that indicates how confident the model needs to be before considering detection of a hand succesfull
    min_tracking_confidence = 0.1) as hands: # a normalized value (0-1) that indicates how confident the models needs to be before considering tracking of hand landmarks succesfull. Otherwise, the model will automatically invoke handdetection on the next input frame
    
# --------------------------------MAIN LOOP---------------------------------------- #

  while cap.isOpened(): # while the webcamera is running
    pyautogui.FAILSAFE = False #Auto failsafe turned off, so that we can move the mouse to any of the corners, without closing the program
    
    success, image = cap.read() # capture frame-by-frame
    if not success: # error handling if capturing of a frame fails
      print("Ignoring empty camera frame.") 
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) # flips the image vertically and converts the image from BGR to RGB. This is because mediaPipe uses RGB values
    image.flags.writeable = False # to improve performance we mark the image as not writeable to pass by reference
    
    results = hands.process(image) # processes a RGB image and returns the hand land marks detected in a tuple called 'multi_hand_landmarks'

    
    # --- Draw the hand annotations on the image ---
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # we then convert the image back into BGR because openCV uses BGR
    
    if results.multi_hand_landmarks: # if the hand landmark model has found a hand                            
      for hand_landmarks in results.multi_hand_landmarks:       
        mp_drawing.draw_landmarks(                              
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)     
     
      # ------------ GETTING POSITIONS USED -------------------
      # Middle finger mcp position
      middle_finger_posX = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x 
      middle_finger_posY = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
    
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
        
      # --------------------- ACTIONS ------------------------
      # move the mouse
      mouseX_offset = window_size_x * middle_finger_posX * 2 #It's the multiplication of 2 that makes the program able to reach the outer sides of the screen 
      mouseY_offset = window_size_y * middle_finger_posY * 2 
      # NOTE.: we create a mouse offset since pyAutoGui and MediaPipe perceives the screen size differently.
     
      middle_finger_mcp_posX = middle_finger_posX * mouseX_offset 
      middle_finger_mcp_posY = middle_finger_posY * mouseY_offset
        
      pyautogui.moveTo(middle_finger_mcp_posX, middle_finger_mcp_posY, 0.1) # 0.1 makes mouse update in a smoother manor

      # Left click functionality
      left_click_dist = round(distance.euclidean([thumb_posX, thumb_posY], [index_finger_mcp_posX, index_finger_mcp_posY]), 3)
      left_click = 0.07 # threshhold
      if left_click_dist < left_click: # if the euclidean distance is less than the threshold, invoke a click
        pyautogui.click() 
        print('Left click')
        log.warning (f'Left click registered! Click on X axis:{middle_finger_mcp_posX} Click on Y axis:{middle_finger_mcp_posY}') #Logs a click with coordinates

      # Voice activation functionality
      right_click_dist = round(distance.euclidean([index_finger_posX, index_finger_posY], [middle_finger_posX, middle_finger_posY]), 3)
      right_click = 0.1 # threshold
      if right_click_dist > right_click:
        try:
          with sr.Microphone() as source2: # use the microphone as source for input
                
            # wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level 
            r.adjust_for_ambient_noise(source2, duration=0.01)
              
            #listens for the user's input 
            print("Listening...")
            audio2 = r.listen(source2)
              
            # Using google api to recognize audio
            MyText = r.recognize_google(audio2, language="en-GB").lower() # Lowercase letters only so we can detect words without running into capitalized letter problems
            print(f"You said: '{MyText}'")

            # Voice activation commands. If the full message is:
            if MyText == "enter":
              pyautogui.press('enter') 
            elif MyText == "delete":
              pyautogui.hotkey('option','backspace')
            elif MyText == "single delete":
              pyautogui.press('backspace')
            elif MyText == "clear":
              pyautogui.hotkey('command', 'backspace')
            elif MyText == "space":
              pyautogui.press('space')
            elif MyText == "exit" or MyText == "quit":
              sys.exit()

            # If the message contains:
            elif "period" in MyText:
              pyautogui.write(MyText) 
              pyautogui.press('backspace', presses=6) #or 7 if said at the end of a sentence.
              pyautogui.press('.')
              
            # Had to use "questionpoint", instead of "question mark" as that word is predetermined to always be "_" and therefore cant be changed.
            elif 'questionpoint' in MyText or 'question point ' in MyText:
              pyautogui.write(MyText)
              pyautogui.press('backspace', presses=14) #or 13 if said after the end of a sentence.
              pyautogui.hotkey("shift","-") # American keyboard layout: _ = ?

            else: # else write what was detected
              pyautogui.write(MyText)
          
        except sr.UnknownValueError:
          print("Unknown error occured")

        log.warning ('Speech recognizion activated') #Logs when speech recognizion is activated

      # Scroll down
      scroll_down_dist = round(distance.euclidean([middle_finger_posX, middle_finger_posY], [ring_finger_tip_posX, ring_finger_tip_posY]), 3)
      scroll_down = 0.05 # threshold
      if scroll_down_dist > scroll_down:
        pyautogui.scroll(-5) # scrolls down on the screen
        print('Scroll down')

      # Scroll up
      scroll_up_dist = round(distance.euclidean([ring_finger_tip_posX, ring_finger_tip_posY], [pinky_mcp_posX, pinky_mcp_posY]), 3)
      scroll_up = 0.09 # threshold 
      if scroll_up_dist > scroll_up:
        pyautogui.scroll(5) # scrolls up on the screen
        print('Scroll up')

    # cv2.imshow('MediaPipe Hands', image) # shows the webcamera to the screen when the application is running
    
    if cv2.waitKey(5) & 0xFF == 27: # if the escape key is pressed, the application closes
      break

cap.release()
