import streamlit as st

def contact():
    st.set_page_config(
        page_title="Contact Us - NoteNinja",
        page_icon="📞",
        layout="wide"
    )
    
    st.title("Contact Us 📞")
    
    # Contact form with enhanced styling
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            background-color: #f0f2f6;
        }
        .stTextArea > div > div > textarea {
            background-color: #f0f2f6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Get in Touch")
        
        # Contact form
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        subject = st.selectbox("Subject", [
            "General Inquiry",
            "Technical Support",
            "Feature Request",
            "Bug Report",
            "Business Proposal"
        ])
        message = st.text_area("Message", height=150)
        
        if st.button("Send Message", type="primary"):
            if name and email and subject and message:
                # Here you would typically implement the email sending functionality
                st.success("Thank you for your message! We'll get back to you soon.")
                # Clear the form (you might want to implement this based on your needs)
            else:
                st.error("Please fill in all fields!")
                
    with col2:
        st.header("Quick Connect")
        
        # Social Media Links
        st.markdown("""
        ### Connect With Us
        [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/AayushBeura)
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/AayushBeura)
        [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AayushBeura)
        """)
        
        st.markdown("""
        ### Office Hours
        Monday - Friday: 9:00 AM - 6:00 PM
        Saturday: 10:00 AM - 2:00 PM
        Sunday: Closed
        
        ### Location
        📍 KIIT Deemed to be University
        Bhubaneswar, Odisha
        
        ### Support
        📧 support@noteninja.com
        ☎️ +91 XXXXX XXXXX
        """)

if __name__ == "__main__":
    contact()
