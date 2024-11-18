from flask import Flask, redirect, url_for, request, session, jsonify, Response, flash
from datetime import timedelta
import cv2
from config import app, db
from models import SignUp,LabelDict
from inference_classifier import hand_gesture_recognition1, hand_gesture_recognition2
from collect_image import collect_data, create_data_and_train

UPLOAD_FOLDER = 'server/data'

app.secret_key = "your_secret_key"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

camera = cv2.VideoCapture(0)
label_dict2_global = {}

@app.route("/login", methods=["POST","GET"])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = SignUp.query.filter_by(username=username).first()
    if user and user.password == password:
        session.permanent = True
        session["user"] = username
        return jsonify({'message': 'Login successful', 'username': username, 'redirect_url': 'http://localhost:5173/optionPage'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return jsonify({'user': user}), 200
    else:
        return jsonify({'error': 'User not logged in'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json  # Assuming the frontend sends JSON data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    # Check if all required fields are present
    if not username or not email or not password or not confirmPassword:
        return jsonify({'error': 'All fields are required'}), 400

    # Check if passwords match
    if password != confirmPassword:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if a user with the same username or email already exists
    if SignUp.query.filter_by(username=username).first() or SignUp.query.filter_by(email=email).first():
        return jsonify({'error': 'User with this username or email already exists'}), 400

    # Process signup logic here (e.g., save user to database)
    new_user = SignUp(username=username, password=password, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Could not sign up. Please try again later."}), 500
    # Return success response
    return jsonify({'message': 'Signup successful','username': username, 'redirect_url': 'http://localhost:5173/optionPage'}), 200

@app.route('/detect', methods=['POST', 'GET'])
def video_feed():
    if request.method == "POST":
        data = request.json
        custom_sign_names = data.get('customSignNames')
        label_dict2 = {item['index'] : item['name'] for item in custom_sign_names}
        print(label_dict2)
        try:
            # Clear existing data in the table
            LabelDict.query.delete()

            # Store new data
            for key, value in label_dict2.items():
                entry = LabelDict(key=key, value=value)
                db.session.add(entry)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not store label dictionary. Please try again later."}), 500

        # Return success response
        return jsonify({'message': 'Label dictionary stored successfully'}), 200

    else:
        predicted_character = hand_gesture_recognition2(model_path='./model.p', camera_index=1)
        return jsonify({"predicted_character": predicted_character})

@app.route("/detectCustom")
def vid_feed():
    labels_dict1 = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
            10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
            19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
        }
    labels_from_db = LabelDict.query.all()
    label_dict2 = {label.key: label.value for label in labels_from_db}
    predicted_character = hand_gesture_recognition1(label_dict2, model_path1='./model.p', labels_dict1=labels_dict1, model_path2='./custom_model.p', camera_index=1)
    return jsonify({"predicted_character": predicted_character})

@app.route("/upload-image", methods=["POST"])
def upload_image():
    try:
        data = request.json
        no_of_classes = data.get("noOfClasses")
        data_size = data.get("dataSize")
        collect_data(no_of_classes, data_size)
        create_data_and_train()
        return {"message": "Model has been trained", "noOfClasses": no_of_classes, "dataSize": data_size}, 200
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
