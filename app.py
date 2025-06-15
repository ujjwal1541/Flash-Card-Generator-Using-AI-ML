import streamlit as st
import pandas as pd
from flashcard_generator import (
    generate_flashcards,
    extract_text_from_pdf,
    export_to_csv,
    export_to_json
)

# Set page config
st.set_page_config(
    page_title="AI Flashcard Generator",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 AI Flashcard Generator")
st.markdown("""
Generate high-quality flashcards from your educational content using AI.
Upload a PDF or text file, or paste your content directly.
""")

# Sidebar for subject selection
st.sidebar.header("Settings")
subject = st.sidebar.selectbox(
    "Select Subject Area (Optional)",
    ["General", "Biology", "Chemistry", "Physics", "Mathematics", "History", "Literature", "Computer Science"]
)

# Input method selection
input_method = st.radio(
    "Choose Input Method",
    ["Upload File", "Paste Text"]
)

# Initialize session state for flashcards
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = []

# File upload
if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        else:
            text = uploaded_file.getvalue().decode("utf-8")
        
        st.text_area("Extracted Text", text, height=200)
        
        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                st.session_state.flashcards = generate_flashcards(text, subject)

# Text input
else:
    text = st.text_area("Paste your text here", height=300)
    
    if st.button("Generate Flashcards"):
        if text:
            with st.spinner("Generating flashcards..."):
                st.session_state.flashcards = generate_flashcards(text, subject)
        else:
            st.warning("Please enter some text first.")

# Display and edit flashcards
if st.session_state.flashcards:
    st.header("Generated Flashcards")
    
    # Create a DataFrame for editing
    df = pd.DataFrame(st.session_state.flashcards)
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True
    )
    
    # Export options
    st.header("Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export to CSV"):
            export_to_csv(edited_df.to_dict('records'), "flashcards.csv")
            st.success("Flashcards exported to flashcards.csv")
    
    with col2:
        if st.button("Export to JSON"):
            export_to_json(edited_df.to_dict('records'), "flashcards.json")
            st.success("Flashcards exported to flashcards.json")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and OpenAI GPT") 