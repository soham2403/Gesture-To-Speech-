import pickle
import cv2
import mediapipe as mp
import numpy as np
import time
data_list = [{'name': 'hiiii', 'index': 1}, {'name': 'demo1', 'index': 2}]
label_dict2 = {item['index'] - 1: item['name'] for item in data_list}

labels_dict1 = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
        10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
        19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
}

def hand_gesture_recognition1(labels_dict2,model_path1='./model.p', labels_dict1=labels_dict1, model_path2='./custom_model.p', camera_index=1):
    model_dict1 = pickle.load(open(model_path1, 'rb'))
    model1 = model_dict1['model']

    model_dict2 = pickle.load(open(model_path2, 'rb'))
    model2 = model_dict2['model']

    cap = cv2.VideoCapture(camera_index)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    characters_list = []
    start_time = None

    while True:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            data_aux = data_aux[:42]

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction1 = model1.predict([np.asarray(data_aux)])
            prediction2 = model2.predict([np.asarray(data_aux)])

            confidence1 = model1.predict_proba([np.asarray(data_aux)]).max()
            confidence2 = model2.predict_proba([np.asarray(data_aux)]).max()

            current_character1 = labels_dict1[int(prediction1[0])]
            current_character2 = labels_dict2[int(prediction2[0])]

            # print("Prediction:", prediction2[0])
            # print("Keys in labels_dict2:", labels_dict2.keys())
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)

            if confidence1 + confidence2 >= 1:
                chosen_character = current_character1 if confidence1 > confidence2 else current_character2
            else:
    # If the combined confidence is lower than 1, you can choose the character with the highest confidence individually
                chosen_character = current_character1 if confidence1 > confidence2 else current_character2


            if chosen_character not in characters_list:
                if start_time is None:
                    start_time = time.time()
                elif time.time() - start_time >= 3:
                    characters_list.append(chosen_character)
                    start_time = None

            cv2.putText(frame, chosen_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27:  # Check if the escape key is pressed (ASCII value for escape key is 27)
            break

    cap.release()
    cv2.destroyAllWindows()

    return characters_list

def hand_gesture_recognition2(model_path='./model.p', camera_index=1):
    model_dict = pickle.load(open(model_path, 'rb'))
    model = model_dict['model']

    cap = cv2.VideoCapture(camera_index)

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    labels_dict = {
        0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
        10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
        19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
    }

    characters_list = []
    start_time = None

    while True:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            data_aux = data_aux[:42]

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction = model.predict([np.asarray(data_aux)])

            current_character = labels_dict[int(prediction[0])]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)

            if current_character not in characters_list:
                if start_time is None:
                    start_time = time.time()
                elif time.time() - start_time >= 3:
                    characters_list.append(current_character)
                    start_time = None

            cv2.putText(frame, current_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                        cv2.LINE_AA)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27:  # Check if the escape key is pressed (ASCII value for escape key is 27)
            break

    cap.release()
    cv2.destroyAllWindows()

    return characters_list