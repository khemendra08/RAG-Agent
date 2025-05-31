import streamlit as st
import os
import tempfile
import sys
import time
from dotenv import load_dotenv
from pathlib import Path

# Add the project directory to the path so we can import from pdf_rag
sys.path.append(str(Path(__file__).parent))
from src.pdf_rag.crew import PdfRag

# Load environment variables
load_dotenv(override=True)

# Set page configuration
st.set_page_config(
    page_title="PDF RAG Agent",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {text-align: center; margin-bottom: 30px; padding-top: 20px; padding-bottom: 20px;}
    .stButton>button {width: 100%; height: 3em; background-color: #4CAF50; color: white;}
    .upload-section {background-color: #f8f9fa; padding: 20px; border-radius: 10px;}
    .results-section {background-color: transparent; padding: 0; margin-top: 20px;}
    .sidebar-content {padding: 20px;}
    .footer {text-align: center; margin-top: 30px; font-size: 0.8em;}
    /* Adjust Streamlit padding but keep some for the header */
    .block-container {padding-top: 1rem !important; padding-bottom: 0 !important;}
    /* Adjust spacing for specific elements */
    div.stMarkdown > div > h1 {margin-top: 1rem !important; margin-bottom: 1rem !important;}
    /* Remove white space between elements but keep some for readability */
    div[data-testid="stVerticalBlock"] > div {margin-bottom: 0.5rem !important;}
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown("<h1 class='main-header'>📚 PDF RAG Agent</h1>", unsafe_allow_html=True)
st.markdown(
    """This application allows you to search through PDF documents and the web for information on a topic.
    Upload a PDF document and enter your search query to get started."""
)

# Initialize session state variables if they don't exist
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'pdf_name' not in st.session_state:
    st.session_state.pdf_name = None
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar for configuration
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.header("⚙️ Configuration")
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"],
        index=0
    )
    
    # Number of iterations
    iterations = st.slider(
        "Number of Iterations",
        min_value=1,
        max_value=10,
        value=1,
        help="Higher values may provide more comprehensive results but take longer"
    )
    
    # API key input
    api_key = st.text_input(
        "OpenAI API Key",
        value=os.environ.get("OPENAI_API_KEY", ""),
        type="password",
        help="Your OpenAI API key. This will be used for the RAG process."
    )
    
    # Update API key in environment
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    # Search history
    st.header("📜 Search History")
    if st.session_state.history:
        for i, (topic, pdf_name, timestamp) in enumerate(st.session_state.history):
            if st.button(f"{pdf_name}: '{topic}' - {timestamp}", key=f"history_{i}"):
                # Load this historical search
                st.session_state.topic = topic
                st.rerun()
    else:
        st.info("Your search history will appear here.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    # PDF upload section
    st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
    st.subheader("📄 Upload PDF Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.session_state.pdf_path = tmp_file.name
            st.session_state.pdf_name = uploaded_file.name
        
        st.success(f"PDF uploaded successfully: {uploaded_file.name}")
        
        # Display PDF info only
        import PyPDF2
        try:
            with open(st.session_state.pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                st.info(f"Pages: {num_pages}")
        except Exception as e:
            st.warning(f"Could not read PDF details: {e}")
    
    # Search query input
    st.subheader("🔍 Search Query")
    topic = st.text_input("Enter your search topic", value="AI LLMs")
    
    # Advanced options
    with st.expander("Advanced Options"):
        include_web_search = st.checkbox("Include web search", value=True)
        max_results = st.slider("Maximum results to return", 1, 20, 5)
    
    # Run button
    if st.button("🚀 Run Search", type="primary"):
        if not st.session_state.pdf_path:
            st.error("Please upload a PDF document first.")
        elif not api_key:
            st.error("Please enter your OpenAI API key.")
        else:
            st.session_state.processing = True
            with st.spinner("Processing your request... This may take a few minutes."):
                try:
                    # Create inputs dictionary
                    inputs = {"topic": topic}
                    
                    # Run the crew with the uploaded PDF path
                    crew_instance = PdfRag().crew(pdf_file_path=st.session_state.pdf_path)
                    result = crew_instance.kickoff(inputs=inputs)
                    
                    # Convert CrewOutput to string if needed
                    if hasattr(result, '__str__'):
                        result = str(result)
                    
                    # Store the result
                    st.session_state.results = result
                    
                    # Add to history
                    timestamp = time.strftime("%Y-%m-%d %H:%M")
                    st.session_state.history.append((topic, st.session_state.pdf_name, timestamp))
                    if len(st.session_state.history) > 10:  # Keep only the 10 most recent searches
                        st.session_state.history.pop(0)
                    
                    st.session_state.processing = False
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.session_state.processing = False
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Always display PDF viewer in the main column when a PDF is uploaded
    if 'pdf_path' in st.session_state and st.session_state.pdf_path:
        # Create a container for the PDF viewer
        st.subheader("📄 PDF Viewer")
        try:
            # Read PDF file as bytes
            import base64
            with open(st.session_state.pdf_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # Embed PDF viewer with consistent size regardless of results
            # Use a fixed height to prevent compression
            height = 500  # Fixed height for PDF viewer
            pdf_display = f'''
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{height}" type="application/pdf"></iframe>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not display PDF: {e}")
    # Results section - only show container when there are results
    if st.session_state.results or st.session_state.processing:
        st.markdown("<div class='results-section'>", unsafe_allow_html=True)
    
    # Only show search results header when processing or results exist
    if st.session_state.processing or st.session_state.results:
        st.subheader("📊 Search Results")
    
    if st.session_state.processing:
        # Display a more engaging loading animation
        with st.spinner():
            st.markdown("""
            <div style='text-align: center'>
                <p>Processing your request... Please wait.</p>
                <p>This may take a few minutes depending on the size of the document and complexity of the query.</p>
            </div>
            """, unsafe_allow_html=True)
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.1)
                progress_bar.progress(i + 1)
    
    if st.session_state.results:
        # Display only the text results below the PDF viewer
        st.markdown(st.session_state.results)
    else:
        # Don't show the info message to remove white space
        pass
    
    if st.session_state.results or st.session_state.processing:
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """<div class='footer'>
    <p>Created with ❤️ using Streamlit and CrewAI</p>
    <p> 2025 PDF RAG Agent</p>
    </div>""",
    unsafe_allow_html=True
)
