# 🎙️ NoteNinja 1.0 📝

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://note-ninja.streamlit.app)

NoteNinja 1.0 is a Streamlit application designed to simplify meeting documentation. It generates Minutes of Meeting (MOM) from audio input (microphone or system audio), uploaded audio files (WAV), or uploaded PDF files using Google's Gemini AI. This project is a fusion of speech recognition, AI-powered text generation, and PDF handling.

## ✨ Key Features

-   **Real-Time System Audio Recording & Transcription:** Capture audio from your system's default output device, transcribing it using Google's Speech Recognition API.
-   **Multi-threading for Audio Processing:** System audio is processed efficiently using a multithreading technique, by chunking the audio data for a smoother experience.
-   **Microphone Recording:** Record and transcribe audio directly from your microphone.
-   **Audio File Upload:** Transcribe and summarize audio from uploaded WAV files.
-    **PDF File Upload:** Upload and summarize text from PDF files.
-   **AI-Powered MOM Generation:** Generate informative meeting summaries using Gemini AI.
-   **Downloadable PDF Output:** Save generated MOMs as downloadable PDF files.
- **Robust Error Handling:** The app has more robust error handling and checks for various edge cases, especially while handling PDF files.
- **User-Friendly Instructions:** Easy to use, with clear user friendly instructions.

## 🚀 Currently Working

*   **Integrating System Audio:** Capture meetings, webinars, and other audio from your system.
*   **Implementing Multithreading:** Process audio with better efficiency through chunking data.

## 🛠️ Technologies Used

*   **Streamlit:** Used to create an interactive web application.
*   **Python:** Used for the coding environment since it includes the best environment for AI Implementation.
*   **HTML and CSS:** Used to modify the placings of different widgets on the main webpage.
*   **JavaScript:** Used for button clickability and redirection integration.
*   **Google Gemini API:** Used for natural language processing and text generation.
*   **SpeechRecognition:** Used for audio-to-text transcription.
*   **Sounddevice:** Used to access system audio input.
*   **audio-recorder-streamlit:** Used for easy microphone recording from the UI.
*   **NumPy:** Used to handle numerical audio data.
*   **Wave:** Used to work with WAV audio files.
*   **Threading:** Used to implement multithreading for system audio processing.
*   **Queue:** Used to manage thread-safe data handling.
*   **fpdf2:** Used for PDF document creation.
*   **pypdf:** Used for PDF text extraction.
*   **python-docx:** Used for DOCX extraction if that is implemented in the future.

## ⚙️ Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AayushBeura/NoteNinja1.0.git
    cd NoteNinja1.0
    ```
2.  **Run the Streamlit app:**
    ```bash
    streamlit run 0_Home.py
    ```

    The app will open in your default browser.

## 📝 Usage

1.  **Select Audio Input:** Choose between "Microphone" or "System Audio."
2.  **Upload Audio File:** Alternatively, you can upload a WAV audio file directly.
3.  **Upload PDF File:** Alternatively, you can upload a PDF file directly.
4.  **Start Recording:**
    *   If using "System Audio", press "Start Recording", and when done, press "Stop Recording and Process."
    *   If using "Microphone", press the record button and then stop to record the audio.
5.  **Process Audio:**  The app will transcribe and generate a MOM using Google's Gemini AI.
6.  **Download PDF:** A "Download MOM as PDF" button will be shown to save the minutes.
7.  **Upload a PDF:** You can upload the PDF file and after processing, you will be able to download a PDF file.

## ⚠️ Known Issues

*   **System Audio Input:** The website is unable to capture the system audio input currently and work is under progress.

## 💡 Future Improvements

*   **Support for More File Types:** Expand file upload support to include formats like DOCX or TXT.
*   **Speaker Identification:** Add speaker diarization for better multi-speaker meetings.
*   **Improved UI/UX:** Refine user interface and user experience.
*   **More Prompt Engineering:** Improve the Minutes of Meeting format via prompt engineering.
*   **Different Language support:** Allow the app to handle different languages using text to speech translation.

## 🙌 Contributions

Contributions are welcome! If you have feature requests, bug reports, or improvements, please open an issue or submit a pull request.

## 📄 License

[MIT License](LICENSE)

---

**Contact:**

[aayush.beura04@hotmail.com]
