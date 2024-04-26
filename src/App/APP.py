import os
from flask import Flask, request, render_template
from fastai.vision.all import *
import torch

app = Flask(__name__)
# Load the saved model
model_path = '' 
##'
learn = load_learner(model_path) 

# Function to predict the image
def predict_image(image_path):
    img = PILImage.create(image_path)
    pred_class, pred_idx, probs = learn.predict(img)
    return pred_class, probs[pred_idx]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    error = None
    uploaded_image = None

    if request.method == 'POST':
        if 'file' not in request.files:
            error = 'No file part'
        else:
            file = request.files['file']
            if file.filename == '':
                error = 'No selected file'
            elif file and file.filename.lower().endswith(('.jpg', '.jpeg')):
                # Save the uploaded image to a temporary location
                uploaded_image_path = os.path.join(app.root_path, 'static', 'uploaded_image.jpg')
                file.save(uploaded_image_path)

                # Predict the image
                prediction, confidence = predict_image(uploaded_image_path)

                # Delete the temporary uploaded image
                ## os.remove(uploaded_image_path)

                uploaded_image = 'uploaded_image.jpg'

            else:
                error = 'Invalid file format. Only JPEG images are allowed.'

    return render_template('index.html', prediction=prediction, confidence=confidence, error=error, uploaded_image=uploaded_image)

if __name__ == '__main__':
    app.run(debug=True)