import streamlit as st
import joblib
import time

# Load the serialized model using joblib

# Set page title and favicon
st.set_page_config(
    page_title="Malicious URL Detector",
    page_icon="✅",
)
labels = ['benign', 'defacement', 'malware', 'phishing']
# Create a sidebar section for the model path input
st.sidebar.title("Model Configuration")

@st.cache_resource
def load_model(path, pathMC):
    try:
        model = joblib.load(path)
        modelMC = joblib.load(pathMC)

        st.sidebar.success("Model loaded successfully.")
        return model, modelMC
    except Exception as e:
        st.sidebar.error(f"Error loading the model: {str(e)}")
model_path = st.sidebar.text_input("Enter Model Path:", value="../model.sav")
model_mc_path = st.sidebar.text_input("Enter Multiclass Model Path:", value="../modelMC.sav")

model, modelMC = load_model(model_path, model_mc_path)

# Create a Streamlit app with a centered layout
st.title("Malicious URL Detection system")
st.write("Enter a URL to check if it looks malicious:")

# Create a text input field for the user to enter a value
user_input = st.text_input("Enter a value:")

# Create a button for prediction
if st.button("Check"):
    if user_input:
        # Use st.spinner to indicate that the app is working
        with st.spinner("Predicting..."):
            # Simulate a delay (replace this with your actual prediction)
            try:
                # Perform model classification on the user input
                #proba can be used if a different threshold want to be 
                prediction = model.predict_proba([user_input])[0]
                if prediction[1] > 0.55:
                    st.success("URL Looks benign")
                elif prediction[1] < 0.55 and prediction[1] > 0.45:
                    st.warning("Prediction not conclusive: URL might be malicious or benign")
                else:
                    type = modelMC.predict([user_input])
                    st.error(f"URL looks malicious (Possibly a {labels[type[0]]} URL)")
                print(model)
                print(prediction)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Add a footer at the bottom of the main content
st.write("")
st.write("---")
st.write("By Alejandro Pérez Moreno | [GitHub](https://github.com/aleradamantis99/MaliciousURLDetection)")