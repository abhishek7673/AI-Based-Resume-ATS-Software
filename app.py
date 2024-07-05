from dotenv import load_dotenv   #type: ignore

load_dotenv()

import streamlit as st #type: ignore
import os
import base64
import io
from PIL import Image #type: ignore
import pdf2image #type: ignore
import google.generativeai as genai # type: ignore

genai.configure(api_key=os.getenv("GOOGLE_API_KEYS"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    ##convert pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No such file uploaded")
    

##streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("Percentage match")

submit3 = st.button("Suggestion Based on Resume")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of Data Science, Full Stack Web Development, 
Big Data Engineering, DEVOPS, Data Analyst, your task is to review the provided resume against the job description
for these profiles. Please share your professional evaluation on whether the candidate's profile aligns with 
highlight the strength and weaknesses of the applicant in relation to the specified job recommendations"""

input_prompt2 = """
You are an skilled ATS (Application Tracking System) scanner with a deep undrstanding of Data Science, Web Development,
Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality, your task is to evaluate the resume against
the provided job description. give me the percentage of match if the resume matches the job description. 
First thee output should come as percentage and then keywords missing in the resume"""

input_prompt3 = """
You are a job recommendation system. Your task is to provide me with the external links for the job based on the resume
scanned. """

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

     
