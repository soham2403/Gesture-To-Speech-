import os
import cv2
import pickle
import numpy as np
import mediapipe as mp

import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def collect_data(number_of_classes, dataset_size):
    DATA_DIR = './data'
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    cap = cv2.VideoCapture(0)
    for j in range(number_of_classes):
        if not os.path.exists(os.path.join(DATA_DIR, str(j))):
            os.makedirs(os.path.join(DATA_DIR, str(j)))

        print('Collecting data for class {}'.format(j))

        done = False
        while True:
            ret, frame = cap.read()
            cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                        cv2.LINE_AA)
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) == ord('q'):
                break

        counter = 0
        while counter < dataset_size:
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            cv2.waitKey(25)
            cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

            counter += 1

    cap.release()
    cv2.destroyAllWindows()

def create_data_and_train():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    DATA_DIR = './data'

    data = []
    labels = []
    for dir_ in os.listdir(DATA_DIR):
        for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
            data_aux = []

            x_ = []
            y_ = []

            img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:
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

                data.append(data_aux)
                labels.append(dir_)

    f = open('data.pickle', 'wb')
    pickle.dump({'data': data, 'labels': labels}, f)
    f.close()
    
    
    
    
    data_dict = pickle.load(open('./data.pickle', 'rb'))

    # Initialize lists to store valid data and labels
    valid_data = []
    valid_labels = []

    # Iterate through data and labels, skipping elements with inconsistent shapes
    for d, label in zip(data_dict['data'], data_dict['labels']):
        if np.asarray(d).shape != (42,):  # Adjust desired_shape as per your requirement
            continue
        valid_data.append(d)
        valid_labels.append(label)

    # Convert valid data and labels into NumPy arrays
    data = np.asarray(valid_data)
    labels = np.asarray(valid_labels)

    # Perform train-test split
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

    # Initialize and train the model
    model = RandomForestClassifier()
    model.fit(x_train, y_train)

    # Make predictions
    y_predict = model.predict(x_test)

    # Calculate accuracy
    score = accuracy_score(y_predict, y_test)

    # Print accuracy
    print('{}% of samples were classified correctly !'.format(score * 100))

    # Save the trained model
    with open('custom_model.p', 'wb') as f:
        pickle.dump({'model': model}, f)
