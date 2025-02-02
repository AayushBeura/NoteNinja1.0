import streamlit as st

def home_page():
    # Page config
    st.set_page_config(
        page_title="NoteNinja - AI Meeting Minutes Generator",
        page_icon="🎯",
        layout="wide"
    )

    # Try to load the logo
    image_path = "NoteNinja.png"
    try:
        st.image(image_path, use_container_width=True)
    except Exception as e:
        st.write(f"Error loading the image. Ensure that the image file: '{image_path}' exists in the same directory as 'main_app.py'. Error Details: {e}")

    st.markdown("<h1 style='text-align: center; font-family: Arial, sans-serif;'>Welcome to NoteNinja</h1>", unsafe_allow_html=True)

    if st.button("Get Started", key="get_started_btn", type="primary", help="Click to start using the application"):
        st.switch_page("pages/1_Program.py")

    # Custom CSS for button styling
    st.markdown(
        """
        <style>
          [data-testid="stButton"] {
             display: flex;
             justify-content: center;
             margin: 20px auto;
             border: none;
             border-radius: 5px;
             }
          [data-testid="stButton"] > button {
                color: white;
                padding: 15px 30px;
                font-size: 1.5em;
          }
       </style>
        """,
         unsafe_allow_html=True
    )

    # About section
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 20px;">
           <h2 style='font-family: Arial, sans-serif;'>About NoteNinja</h2>
           <p style='font-family: Arial, sans-serif;'>NoteNinja is a Streamlit application that uses the power of AI to transcribe and summarize meetings. It allows users to record or upload audio and generate accurate minutes. It has support for microphone and system audio, as well as support for file upload.</p>
           <p style='margin-top: 30px;
              font-size: 1.3em;
              font-style: bold;
              color: gray'><b>Tech Stack Used:</b> Python, HTML, CSS, Streamlit, Google Gemini AI, SpeechRecognition API, NumPy, SoundDevice, FPDF</p>
           <div style="margin-top: 30px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    home_page()
