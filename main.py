#Used tensorflow==2.12

from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture("badTrack.mp4")

# Get the original video dimensions
frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create a named window
cv2.namedWindow("Rail Inspection - Status", cv2.WINDOW_NORMAL)

# Set the window size explicitly to the original video dimensions
cv2.resizeWindow("Rail Inspection - Status", frame_width, frame_height)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    if not ret:
        break  # If the frame is not read correctly, exit the loop

    # Resize the raw image into (224-height, 224-width) pixels for the model
    image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image_array = (image_array / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name)
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Display the prediction and confidence on the video frame
    text = f"{class_name} - {str(np.round(confidence_score * 100))[:-2]}%"
    cv2.putText(image, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Show the video at its original size
    cv2.imshow("Rail Inspection - Status", image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()