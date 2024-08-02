import cv2 as cv
import mediapipe as mp
import serial as sr
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

time.sleep(1)
print("initialize serial communaication 'pyToArduino()' function protocol??(y/n)")
user_input = input("")
if(user_input == 'y'):
    ser = sr.Serial('COM6', 9600)
    time.sleep(1)


#determinant to which fingers are up and which ones are down to update the hand landmark list, which is later send to the
#pyToArduinoInterface for processing into strings to be sent to serial communications
def count1():
    if fin.multi_hand_landmarks:
        for hand_landmarks in fin.multi_hand_landmarks:

            middle_knuckle = hand_landmarks.landmark[9]
            thumbtip = hand_landmarks.landmark[4]
            thumb_knuckle = hand_landmarks.landmark[3]
            other_difference_length = abs(thumb_knuckle.y - middle_knuckle.y)
            difference_length = abs(thumbtip.y - middle_knuckle.y)
            #other_other_difference_length = abs(thumbtip.y - thumb_knuckle.y)
            thumb_to_middle_threshold = 0.033
            if difference_length < thumb_to_middle_threshold or other_difference_length > 0.3:
                finger_list_hand1[0] = 0
            if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                finger_list_hand1[1] = 1
            if hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y:
                finger_list_hand1[2] = 1
            if hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y:
                finger_list_hand1[3] = 1
            if hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y:
                finger_list_hand1[4] = 1


#encode and hand point info to arduino microcontroller to instruct which LED to turn on
def pyToArduinoInterface(finger_list_hand1):
    data = ','.join(map(str, finger_list_hand1)) + '\n'
    ser.write(data.encode('utf-8'))


vid = cv.VideoCapture(0);
while vid.isOpened():
    finger_list_hand1 = [1, 0, 0, 0, 0]
    totality = 0
    ret, frame = vid.read()
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    fin = hands.process(image)
    if fin.multi_hand_landmarks:
        for hand_landmarks in fin.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    image = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
    flipframe = cv.flip(frame, 1)
    cv.imshow('video',flipframe)
    count1()
    #Once update is given from the function count1() it will go through each index of a list array of finger_list_hand1.
    #At the moment the hand list index is currently updated in a for loop which goes through each index
    for i in range(0, len(finger_list_hand1)):
        totality = totality + finger_list_hand1[i]
    #then if you said yes to init the pyToArduinoInterface it will then send the ubdated substring.
    if(user_input == 'y'):
        pyToArduinoInterface(finger_list_hand1)
    print(f"Fingers: {finger_list_hand1}, Total:{totality}")
    if cv.waitKey(1) & 0xFF == ord('d'):
        break

vid.release()
cv.destroyAllWindows()
