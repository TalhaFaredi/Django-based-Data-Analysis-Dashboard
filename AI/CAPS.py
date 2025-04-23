import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import PIL.Image
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key='AIzaSyBCtDh8zy-3OyaX3SWR5k7jqQwh5is7wzY')
google = genai.GenerativeModel('gemini-pro')

# Load the pre-trained run-out prediction model
model_path = 'path.h5'  # Replace with the actual path to your saved model
model = tf.keras.models.load_model(model_path)

# Define class labels for the run-out prediction model
class_labels = {0: 'not out', 1: 'out'}

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
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Run Out Prediction", "AI CHAT"])

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

elif page == "Run Out Prediction":
    # Run Out Prediction and AI Chat Page
    st.markdown('<h2 class="header">Run Out Prediction</h2>', unsafe_allow_html=True)

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

            prediction = model.predict(img_array)
            predicted_class = int(round(prediction[0][0]))
            predicted_label = class_labels[predicted_class]

            st.markdown('<h4 class="subheader">Prediction Result:</h4>', unsafe_allow_html=True)
            st.markdown(f'<p class="description">The model predicts: {predicted_label} (Class {predicted_class})</p>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")

elif page == "AI CHAT":
    # AI Chat Section
    st.markdown('<h2 class="header">Cricket Response Generator</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description">It Contains Data About Cricket Strategy, Rules, Teams\' Previous Performance, and Players\' Data All Limited to April 2023.</p>', unsafe_allow_html=True)
    cricket="Answer In Context of Cricket Sports"

    prompt = st.text_input("")
    updated_prompt = cricket + prompt

    # Button to generate response
    if st.button("Generate Response", key="generate_response"):
        response = google.generate_content(updated_prompt)
        response_text = response.text
        st.text_area("Response", response_text, height=150)
    
    model = genai.GenerativeModel('gemini-pro-vision')
    uploaded_file = st.file_uploader("Choose an image...", type="jpg")
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        img = PIL.Image.open(uploaded_file) 
        response = model.generate_content(["Explain Each and Everything in the image and also make a conclusion of 1 line bold the conclusion and write in next line", img])
        st.write(response.text)
