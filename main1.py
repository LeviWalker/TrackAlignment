import os
from keras.models import load_model

# Get the absolute path
file_path = os.path.abspath("keras_model.h5")
model = load_model(file_path, custom_objects=None, compile=False, safe_mode=False)
print(file_path)
