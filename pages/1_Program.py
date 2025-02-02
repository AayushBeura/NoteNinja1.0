import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import numpy as np
import os
import wave
import sounddevice as sd
import threading
import queue
from audio_recorder_streamlit import audio_recorder
import re
from datetime import date
from fpdf import FPDF
import io
from pypdf import PdfReader
import docx
import unicodedata

# --- API Keys and Setup ---
API_KEY = "AIzaSyBQG_7hh4KkpjM-P2jc0E2tbCAtGilyZNE"  # Replace with your API key
MODEL_NAME = "gemini-2.0-flash-exp"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# --- Audio Recording Setup ---
SAMPLE_RATE = 44100
CHANNELS = 2
CHUNK_SIZE = 1024
OUTPUT_FILE = "recorded_audio.wav"

# --- Global Variables ---
audio_queue = queue.Queue()
stop_event = threading.Event()
recording_thread = None

# --- Gemini AI Functions ---
def generate_text(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text if response else "Error: No response generated."
    except Exception as e:
        return f"Error: {e}"

# --- Audio Recording Function (System Audio) ---
def audio_recording_sounddevice(audio_queue, event, channels):
    try:
        print("Recording system audio using sounddevice (default output device)...")
        default_output_device = sd.query_devices(kind='output')

        with sd.RawInputStream(samplerate=SAMPLE_RATE, device=default_output_device['index'], channels=channels, dtype='int16') as stream:
            while event.is_set():
                audio_chunk, overflowed = stream.read(CHUNK_SIZE)
                if not overflowed:
                    audio_queue.put(audio_chunk.tobytes())
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None

# --- Speech Recognition (Transcription) ---
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            print("Transcribing audio...")
            audio = recognizer.record(source)
    except Exception as e:
        print(f"Transcription error {e}")
        return None
    try:
        text = recognizer.recognize_google(audio)  # Uses Google API
        print("Transcription Completed.")
        print("\nTranscribed Text:\n", text)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio.")
        return "Speech Recognition could not understand the audio."
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition.")
        return "Could not request results from Google Speech Recognition."

# --- Prompt Engineering for Audio ---
def prepare_mom_prompt_audio(transcript):
    today = date.today().strftime("%Y-%m-%d")
    date_pattern = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')  # check for YYYY-MM-DD
    match = date_pattern.search(transcript)
    if match:
        date_found = match.group(1)
    else:
        date_found = today

    prompt = (
        f"Prepare a MOM (Minutes of Meeting) for the following transcript in a suitable format. "
        f"Date: {date_found}. "
        f"Do not produce any pre- or post-texts. Generate insights based on the content logically. "
        f"Remove all unnecessary symbols or formatting: {transcript}"
    )
    return prompt

# --- Prompt Engineering for Files ---
def prepare_mom_prompt_files(transcript):
    today = date.today().strftime("%Y-%m-%d")
    date_pattern = re.compile(r'\b(\d{4}-\d{2}-\d{2})\b')  # check for YYYY-MM-DD
    match = date_pattern.search(transcript)
    if match:
        date_found = match.group(1)
    else:
        date_found = today

    prompt = (
        f"Provide a summary of the meeting in a suitable format. "
        f"Date: {date_found}. "
        f"Do not produce any pre- or post-texts. Summarize key insights logically. "
        f"Remove all unnecessary symbols or formatting: {transcript}"
    )
    return prompt

# --- PDF Generation Function for Audio ---
def generate_pdf_from_string_audio(input_string, filename="output.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, input_string)
    pdf_bytes = pdf.output(dest="S").encode('latin-1')
    return pdf_bytes

# --- PDF Generation Function for Files ---
def clean_text(text):
    """Removes unsupported characters to prevent encoding issues."""
    return ''.join(c for c in text if unicodedata.category(c)[0] != "C")  # Remove control characters

def generate_pdf_from_string_files(input_string, filename="output.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Use a Unicode-supported font (ensure 'DejaVuSans.ttf' is available)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)

    # Clean text to remove problematic characters
    cleaned_text = clean_text(input_string)
    
    pdf.multi_cell(0, 10, cleaned_text)

    # Output as bytes using UTF-8 encoding (fixes 'latin-1' issue)
    pdf_bytes = pdf.output(dest="S")  #No encoding done now
    return pdf_bytes
    
# --- Extract text from PDF file ---
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# --- Extract text from DOC file ---
def extract_text_from_doc(uploaded_file):
    doc = docx.Document(uploaded_file)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

# --- Normalize the extracted text by merging all the lines ---
def normalize_text(text):
      lines = text.splitlines()
      return " ".join(line.strip() for line in lines)

# --- Streamlit UI ---
def main_app():
    global recording_thread
    global stop_event
    st.title("🎙️ Meeting Minutes Generator 📝")

    audio_input_type = st.radio("Select Audio Input:", ("Microphone", "System Audio"))

    if audio_input_type == "Microphone":
        st.write("Click the button below to start the recording and then press again to stop the recording and process the audio:")
        audio_bytes = audio_recorder(pause_threshold=1000.0, sample_rate=41_000)
        if audio_bytes:
            try:
                with open(OUTPUT_FILE, "wb") as f:
                    f.write(audio_bytes)
                st.audio(audio_bytes, format="audio/wav")
                with st.spinner("Processing Audio"):
                    transcript = transcribe_audio(OUTPUT_FILE)
                    if transcript:
                        mom_prompt = prepare_mom_prompt_audio(transcript)
                        result = generate_text(mom_prompt)
                        st.write("\nGenerated MOM:\n", result)
                        pdf_file = generate_pdf_from_string_audio(result)
                        st.download_button(
                            label="Download MOM as PDF",
                             data = pdf_file,
                            file_name = "mom.pdf",
                            mime = "application/pdf",
                            key="audio_download"
                            )
                    else:
                        st.write("No transcript found.")
            except Exception as e:
                st.write(f"An error has occurred during audio processing: {e}")

    elif audio_input_type == "System Audio":
        st.write("Click the button to record and process the audio")
        start_recording = st.button("Start Recording", key = "start_system_audio")
        stop_recording = st.button("Stop Recording and Process", key = "stop_system_audio")
        transcript_chunks = []
        if start_recording:
            if recording_thread and recording_thread.is_alive():
                st.write("Already recording...")
            else:
                st.write("Starting the recording")
                stop_event.clear()
                default_output_device = sd.query_devices(kind='output')
                channels = default_output_device['max_output_channels']
                recording_thread = threading.Thread(target=audio_recording_sounddevice, args=(audio_queue, stop_event, channels))
                recording_thread.start()

        if stop_recording:
            if recording_thread and recording_thread.is_alive():
                stop_event.set()
                recording_thread.join()
                recording_thread = None #Set to none to avoid issues
            with st.spinner("Processing Audio...."):
                 try:
                    with wave.open(OUTPUT_FILE, 'wb') as wf:
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(2)
                        wf.setframerate(SAMPLE_RATE)
                        while not audio_queue.empty():
                            audio_data = audio_queue.get()
                            wf.writeframes(audio_data)

                    transcript = transcribe_audio(OUTPUT_FILE)
                    if transcript:
                        mom_prompt = prepare_mom_prompt_audio(transcript)
                        result = generate_text(mom_prompt)
                        st.write("\nGenerated MOM:\n", result)
                        pdf_file = generate_pdf_from_string_audio(result)
                        st.download_button(
                           label="Download MOM as PDF",
                           data = pdf_file,
                           file_name = "mom.pdf",
                           mime = "application/pdf",
                           key="system_audio_download"
                           )
                    else:
                        st.write("No transcript found.")
                 except Exception as e:
                    st.write(f"An error has occurred during audio processing: {e}")
    st.markdown("---")
    st.write("OR")
    st.write("Upload a file to generate MOM (PDF Only)")

    uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"], key="file_upload")

    if uploaded_file is not None:
          try:
             if uploaded_file.name.lower().endswith(".pdf"):
                 text = extract_text_from_pdf(uploaded_file)
             else:
                 st.write("Please upload a file that ends in '.pdf'")
                 return
             normalized_text = normalize_text(text)
             mom_prompt = prepare_mom_prompt_files(normalized_text)
             with st.spinner("Processing the file"):
                 result = generate_text(mom_prompt)
                 st.write("\nGenerated MOM:\n", result)
                 pdf_file = generate_pdf_from_string_files(result)
                 st.download_button(
                  label="Download MOM as PDF",
                 data = pdf_file,
                 file_name = "mom.pdf",
                 mime = "application/pdf",
                 key="file_download"
                )
          except Exception as e:
             st.write(f"Error: Could not process the file. {e}")

if __name__ == "__main__":
    main_app()