import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_community.document_loaders import YoutubeLoader

load_dotenv()

genai.configure(api_key="AIzaSyAlcc1wRi6O0XVJ2R8OryYjmHQsmFUajQc")
model = genai.GenerativeModel("gemini-1.0-pro")

prompt = """You are a youtube video summarizer. You will be taking the transcript text and 
summarizing the entire video and providing the important points in the summary. Please 
provide the summary of the text given here:
"""

def extract_transcript_details(url):
    try:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        documents = loader.load()
        return "".join([doc.page_content for doc in documents]).strip()
    except Exception as e:
        print(e)
        return None

st.title("YouTube Video Summarizer")
youtube_link = st.text_input("Enter Your Video link: ")

if youtube_link:
    video_id = youtube_link.split('/')[-1].split('?')[0]

    # Create the YouTube embed link
    youtube_embed_link = f"https://www.youtube.com/embed/{video_id}"

    # Display the YouTube video using an iframe
    st.markdown(
        f'<iframe width="700" height="394" src="{youtube_embed_link}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )

if st.button("Generate Summary"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        response = model.generate_content(prompt + transcript_text)
        st.markdown("## Detailed Notes: ")
        st.write(response.text)
    else:
        st.error("Failed to extract transcript from the provided video link.")
