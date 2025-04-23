import streamlit as st
import joblib
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import PIL.Image
import google.generativeai as genai

# Load the ODI model and label encoders
model_odi = joblib.load('rf_model.pkl')
label_encoders_odi = joblib.load('label_encoders.pkl')
data_odi = pd.read_csv('odi.csv')

# Load the T20 model and label encoders
model_t20 = joblib.load('rf_t20_model.pkl')
label_encoders_t20 = joblib.load('t20_label_encoders.pkl')
data_t20 = pd.read_csv('t20.csv')

# Load the Run Out Prediction model
run_out_model = tf.keras.models.load_model('path.h5')
class_labels = {0: 'not out', 1: 'out'}

# Configure Google Generative AI
genai.configure(api_key='AIzaSyBCtDh8zy-3OyaX3SWR5k7jqQwh5is7wzY')
google = genai.GenerativeModel('gemini-pro')

# HTML and CSS for Custom Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
    }
    .title {
        color: #4CAF50;
        text-align: center;
        animation: fadeIn 2s;
    }
    .header {
        color: #f44336;
        text-align: center;
        animation: fadeIn 2s;
    }
    .subheader {
        color: #2196F3;
        text-align: center;
        animation: fadeIn 3s;
    }
    .description {
        color: #000;
        text-align: justify;
        animation: fadeIn 3s;
    }
    .img-container {
        text-align: center;
    }
    .fadeIn {
        animation: fadeIn 2s;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app layout
st.markdown('<h1 class="title">Cricket AI Web App</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("AI Modules of CAPS")
st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to", ["Home", "ODI Match Predictor", "T20 Match Predictor", "Run Out Prediction", "AI Chat"])

if page == "Home":
    # Home Page
    st.markdown('<h2 class="header">Your Inspiring Headline</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description">A captivating description of your business or passion.</p>', unsafe_allow_html=True)
    if st.button("Explore More", key="explore"):
        st.write("Explore More Clicked")

    # Image Grid
    st.markdown('<h3 class="subheader">Image Grid</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("not4.jpg", caption="Image 1", use_column_width=True)
        st.markdown('<p class="description">Title 1</p>', unsafe_allow_html=True)
        st.markdown('<p class="description">Short description.</p>', unsafe_allow_html=True)
    with col2:
        st.image("out5.jpg", caption="Image 2", use_column_width=True)
        st.markdown('<p class="description">Title 2</p>', unsafe_allow_html=True)
        st.markdown('<p class="description">Short description.</p>', unsafe_allow_html=True)

    # CEO Section
    st.markdown('<h3 class="subheader">CEO\'s Message</h3>', unsafe_allow_html=True)
    ceo_col1, ceo_col2 = st.columns(2)
    with ceo_col1:
        st.image('f.JPG', caption="CEO Image", use_column_width=True)
    with ceo_col2:
        st.markdown('<p class="description">Inspiring quote from your CEO.</p>', unsafe_allow_html=True)
        if st.button("Read More", key="read_more"):
            st.write("Read More Clicked")

    # Testimonials Section
    st.markdown('<h3 class="subheader">What People Say</h3>', unsafe_allow_html=True)
    st.image("afridi.jpg", use_column_width=True)
    st.markdown('<p class="description">"Fantastic service! Highly recommend them!"</p>', unsafe_allow_html=True)
    st.markdown('<p class="description">- Shahid AFRIDI The Brand Embassadar</p>', unsafe_allow_html=True)
elif page == "ODI Match Predictor":
    # ODI Match Predictor Page
    st.title('ODI Match Winner Predictor')

    # Team1 selection
    team1 = st.selectbox('Select Team 1', label_encoders_odi['team1'].classes_)

    # Filter team2 options based on team1 selection
    team2_options = [team for team in label_encoders_odi['team2'].classes_ if team != team1]
    team2 = st.selectbox('Select Team 2', team2_options)

    # Filter venue options based on team1 and team2 selection
    venues = data_odi[(data_odi['team1'] == team1) | (data_odi['team2'] == team1) |
                      (data_odi['team1'] == team2) | (data_odi['team2'] == team2)]['venue'].unique()
    venue = st.selectbox('Select Venue', venues)

    # Predict button
    if st.button('Predict Winner'):
        if team1 not in label_encoders_odi['team1'].classes_ or \
            team2 not in label_encoders_odi['team2'].classes_ or \
            venue not in label_encoders_odi['venue'].classes_:
            st.write("Error: One of the inputs is not recognized.")
        else:
            team1_enc = label_encoders_odi['team1'].transform([team1])[0]
            team2_enc = label_encoders_odi['team2'].transform([team2])[0]
            venue_enc = label_encoders_odi['venue'].transform([venue])[0]
            prediction_enc = model_odi.predict([[team1_enc, team2_enc, venue_enc]])[0]
            prediction = label_encoders_odi['winner'].inverse_transform([prediction_enc])[0]
            st.write(f'Predicted Winner: {prediction}')

    # Instructions
    st.write("""
    ## Instructions
    1. Select Team 1.
    2. Select Team 2 (Team 2 options will not include the selected Team 1).
    3. Select the venue (Venue options are limited to where both selected teams have played).
    4. Click the 'Predict Winner' button to see the prediction.
    """)

elif page == "T20 Match Predictor":
    # T20 Match Predictor Page
    st.title("T20 Match Winner Predictor")
    # Input fields from dataset columns
    bat_first = st.selectbox('Select Team Batting First', sorted(data_t20['Bat First'].unique()))
    bat_second_options = sorted([team for team in data_t20['Bat Second'].unique() if team != bat_first])
    bat_second = st.selectbox('Select Team Batting Second', bat_second_options)

    # Filter venues based on selected teams
    venues_both_teams_played = data_t20[data_t20['Bat First'].isin([bat_first, bat_second]) & 
                                         data_t20['Bat Second'].isin([bat_first, bat_second])]['Venue'].unique()
    venue = st.selectbox('Select Venue', sorted(venues_both_teams_played))

    def predict_winner(bat_first, bat_second, venue):
        bat_first_enc = label_encoders_t20['Bat First'].transform([bat_first])[0]
        bat_second_enc = label_encoders_t20['Bat Second'].transform([bat_second])[0]
        venue_enc = label_encoders_t20['Venue'].transform([venue])[0]
        prediction_enc = model_t20.predict([[bat_first_enc, bat_second_enc, venue_enc]])[0]
        prediction = label_encoders_t20['Winner'].inverse_transform([prediction_enc])[0]
        return prediction

    if st.button('Predict Winner'):
        result = predict_winner(bat_first, bat_second, venue)
        st.write(f'Predicted winner: {result}')

elif page == "Run Out Prediction":
    st.title("Run Out Prediction")
    # Run Out Prediction Section
    st.markdown('<h3 class="subheader">Run Out Prediction</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image for run-out prediction...", type="jpg")
    if uploaded_file is not None:
        try:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            img = image.load_img(uploaded_file, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0

            prediction = run_out_model.predict(img_array)
            predicted_class = int(round(prediction[0][0]))
            predicted_label = class_labels[predicted_class]

            st.markdown('<h4 class="subheader">Prediction Result:</h4>', unsafe_allow_html=True)
            st.markdown(f'<p class="description">The model predicts: {predicted_label} (Class {predicted_class})</p>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")

elif page == "AI Chat":
    # AI Chat Section
    st.title("Cricket Response Generator")
    cricket = "Answer In Context of Cricket Sports"
    prompt = st.text_input("")

    updated_prompt = cricket + prompt

    # Button to generate response
    if st.button("Generate Response", key="generate_response"):
        response = google.generate_content(updated_prompt)
        response_text = response.text
        st.write(response_text)
        # st.text_area("Response", response_text, height=150)

    model = genai.GenerativeModel('gemini-pro-vision')
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            img = PIL.Image.open(uploaded_file) 
            response = model.generate_content(["Explain Each and Everything in the image and also make a conclusion of 1 line bold the conclusion and write in next line", img])
            st.write(response.text)
