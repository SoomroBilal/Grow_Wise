from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import sklearn
from sklearn.preprocessing import MinMaxScaler
import pickle

#  Predicting class labels for disease indentification model
def predicting_class(model_name):
    models_category = {
    'apple_model': ['Scab', 'Black Rot', 'Cedar Rust', 'Healthy'],
    'banana_model': ['Cordana Leaf Spot', 'Healthy', 'Pestalotiopsis', 'Sigatoka'],
    'cherry_model': ['Healthy', 'Powdery Mildew'],
    'cotton_model': ['Jassid', 'Mealybug', 'Aphid', 'Armyworm', 'Healthy', 'Thrips'],
    'grape_model':['Black root','Esca','Leaf Blight','Healthy'],
    'mango_model': ['Anthracnose','Becterial Canker', 'Cutting Weevil','Die Back','Gall Midge','Healthy','Powdery Mildew', 'Sooty Mould'],
    'maize_model': ['Gray Leaf spot','Common Rust','Northern Leaf Blight','Healthy'],
    'peach_model':['Bacterial Spot','Healthy'],
    'potato_model':['Early Blight','Late Blight','Healthy'],
    'pepper_model':['Healthy','Black Spot'],
    'rice_model':['Brown Spot','Healthy','Hispa','Leaf Blast'],
    'soybean_model':['Bacterial Pustule','Frogeye Leaf Spot','Healthy','Rust','Sudden Death Syndrome','Target Leaf Spot','Yellow Mosaic'],
    'strawberry_model':['Healthy','Leaf Scorch'],
    'tomato_model':['Bacterial Scab','Early Blight','Late Blight','Leaf Mould','Septoria Leaf Spot','Spider Mites','Target Spot','Yellow Leaf Curl Virus','Mosaic Virus','Healthy'],
    'wheat_model':['Brown Rust','Healthy','Septoria','Strip Rust']
    }
    categories = models_category.get(model_name)
    return categories

#  Loading the trained model and pre-process the input image for disease identification
def load_and_classify(model_name, image_path):
    script_dir = os.path.dirname(__file__)
    # Navigate to the 'models' folder using a relative path
    models_folder = os.path.join(os.pardir, 'model')
    model_path = os.path.join(models_folder, f'{model_name}.h5')
    model = load_model(model_path)
    uploaded_image = Image.open(image_path)
    uploaded_image = uploaded_image.resize((224, 224))
    uploaded_image = uploaded_image.convert('RGB') # convert the image to RGB
    # Preprocess the image
    uploaded_image = np.array(uploaded_image) / 255.0  # Normalize pixel values
    uploaded_image = np.expand_dims(uploaded_image, axis=0)  # Expand dimensions for batch processing

    # Make the prediction
    prediction = model.predict(uploaded_image)

    # Get the predicted class
    predicted_class = np.argmax(prediction)
    class_list = predicting_class(model_name)
    class_label = class_list[predicted_class]
    return class_label

# Recommender part
def recommendation(N, P, K, temperature, humidity, ph, rainfall):
    # Load the saved deep learning model
    loaded_model_path = "../model/crop_rec_model.h5"
    loaded_model =load_model(loaded_model_path)
    # Load the saved MinMaxScaler
    scaler_filename = "../model/scaler.pkl"
    with open(scaler_filename, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    # Scale the user input data using the loaded scaler
    user_input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    scaled_user_input = scaler.transform(user_input_data)
    # Make predictions with the loaded model
    prediction = loaded_model.predict(scaled_user_input)
    crop_names = {
        0: "Rice", 1: "Maize", 2: "Jute", 3: "Cotton", 4: "Coconut", 5: "Papaya",
        6: "Orange", 7: "Apple", 8: "Muskmelon", 9: "Watermelon", 10: "Grapes",
        11: "Mango", 12: "Banana", 13: "Pomegranate", 14: "Lentil", 15: "Blackgram",
        16: "Mungbean", 17: "Mothbeans", 18: "Pigeonpeas", 19: "Kidneybeans",
        20: "Chickpea", 21: "Coffee", 22: "Peas", 23: "Cowpeas", 24: "Groundnuts",
        25: "Beans", 26: "Soybeans", 27: "Wheat", 28: 'Tobacco'
    }
    
    crop_id = np.argmax(prediction)
    recommended_crop = crop_names[crop_id]
    return recommended_crop