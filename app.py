## invoice exxtractor

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


#configure api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini pro vision model and get response from it
def get_gemini_response(input, image,prompt):
    #loading the gemini pro vision model
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_Image_setup(image_file):
    #load the image file
    if image_file is not None:
        bytes_data = image_file.getvalue()
        image_parts = [
            {
                "mime_type": image_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image file found")
    


## initialize the streamlit app

st.set_page_config(page_title="Invoice Extractor")

st.header("Invoice Extractor")

input = st.text_input("Enter the prompt", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)



submit_button = st.button("Submit")


input_prompt = """
you are an expert in invoice processing and data extraction. You will be provided with an invoice image and a user prompt.
You need to extract the data based on the user prompt. And also if the image is not of invoice then you need to give the output as "The image is not of an invoice"

"""


if submit_button:
    image_data = input_Image_setup(uploaded_file)
    response = get_gemini_response(input, image_data, input_prompt)
    st.subheader("The Response from the model")
    st.write(response)





