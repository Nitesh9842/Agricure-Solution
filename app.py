import joblib
import pandas as pd
from flask import Flask, request, render_template, redirect


# Read the data from the CSV file(data.csv)
data = pd.read_csv('data.csv')
crops = sorted(data['Crop'].unique())
fertilizers = sorted(data['Fertilizer'].unique())


# Define the prediction function
def predict_output(crop, fertilizer):
    # Load the model, crop encoder and fertilizer encoder from the disk
    loaded_model = joblib.load('./fertilizer_multi_output_model.pkl')
    le_crop = joblib.load('./crop_encoder')  # Load the crop label encoder
    le_fertilizer = joblib.load('./fertilizer_encoder')  # Load the fertilizer label encoder

    ###################### Prepare the input data ######################
    try:
        crop_encoded = le_crop.transform([crop])[0]
        fertilizer_encoded = le_fertilizer.transform([fertilizer])[0]
    except ValueError:
        return {
            'Crop': crop,
            'Fertilizer': fertilizer,
            'Hazardous Effects': 'Not Found',
            'Eco-friendly Alternatives': 'Not Found',
            'Mitigation Techniques': 'Not Found'
        }
    X_input = pd.DataFrame([[crop_encoded, fertilizer_encoded]], columns=['Crop', 'Fertilizer'])

    # Make predictions
    predictions = loaded_model.predict(X_input)

    return {
        'Crop': crop,
        'Fertilizer': fertilizer,
        'Hazardous Effects': predictions[0, 0],
        'Eco-friendly Alternatives': predictions[0, 1],
        'Mitigation Techniques': predictions[0, 2]
    }

# Initialize the Flask app
app = Flask(__name__)

# Index route, shows the form
@app.route('/')
def index():
    return render_template('index.html', prediction_text='', crops=crops, fertilizers=fertilizers)


# Prediction route, redirects to the index route if the request is GET
@app.route('/predict', methods=['GET'])
def predict_form():
    return redirect('/')


# Prediction route, returns the predictions if the request is POST
@app.route('/predict', methods=['POST'])
def predict():
    crop = request.form['crop']
    fertilizer = request.form['fertilizer']
    output = predict_output(crop, fertilizer)
    return render_template('index.html', prediction_text=output, crops=crops, fertilizers=fertilizers)

# Run the app
if __name__ == '__main__':
    app.run(debug=False)
