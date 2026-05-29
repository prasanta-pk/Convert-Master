import streamlit as st
import os
import io
import zipfile
import tempfile
from pdf2docx import Converter

# Page Configuration
st.set_page_config(page_title="PDF to Word - Convert Master", page_icon="📝", layout="wide")

# Custom CSS for spacing and look
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .back-btn-container { margin-top: 25px; margin-bottom: 20px; }
    
    .back-btn-container .stPageLink a {
        background-color: #f0f2f6 !important;
        color: #31333f !important;
        border: 1px solid #d1d9e0 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        display: inline-flex !important;
        width: auto !important;
    }
    .back-btn-container .stPageLink a:hover {
        background-color: #e4e6eb !important;
        border-color: #b0b8c1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Centered layout for width control
left_space, center_content, right_space = st.columns([1, 2, 1])

with center_content:
    # Back to Dashboard
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    st.page_link("app.py", label="Back to Dashboard", icon="⬅️")
    st.markdown('</div>', unsafe_allow_html=True)
        
    st.title("📝 PDF to Word Converter")
    st.write("Upload your PDF documents (Maximum 5 files). The system will convert them into editable Word (.docx) files.")

    # Form layout for safe reset
    with st.form("pdf_word_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Choose PDF files", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        submit_button = st.form_submit_button("Convert to Word", use_container_width=True)

    # Core Conversion Logic
    if submit_button and uploaded_files:
        # Rule 1: Max 5 files limit check
        if len(uploaded_files) > 5:
            st.error("You can upload a maximum of 5 PDF files at a time. Please reduce files and try again.")
        else:
            st.info(f"Total {len(uploaded_files)} file(s) selected. Starting conversion...")
            
            converted_files = {} # Stores filename and its docx byte data
            
            for uploaded_file in uploaded_files:
                try:
                    # pdf2docx require physical file paths, so we use temporary files safely
                    with tempfile.TemporaryDirectory() as temp_dir:
                        input_pdf_path = os.path.join(temp_dir, uploaded_file.name)
                        output_docx_name = uploaded_file.name.replace(".pdf", ".docx")
                        output_docx_path = os.path.join(temp_dir, output_docx_name)
                        
                        # Save uploaded bytes to temp PDF
                        with open(input_pdf_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Convert PDF to DOCX using pdf2docx
                        cv = Converter(input_pdf_path)
                        cv.convert(output_docx_path, start=0, end=None)
                        cv.close()
                        
                        # Read converted file back into memory bytes
                        with open(output_docx_path, "rb") as f:
                            converted_files[output_docx_name] = f.read()
                            
                except Exception as e:
                    st.error(f"Error converting {uploaded_file.name}: {e}")

            # Download Handling Logic
            if len(converted_files) > 0:
                st.success(f"Successfully converted {len(converted_files)} file(s)!")
                
                # Rule 2 & 3: Single file upload -> Direct download .docx
                if len(converted_files) == 1:
                    filename, data = list(converted_files.items())[0]
                    st.download_button(
                        label=f"Download {filename}",
                        data=data,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                
                # Rule 4: More than one file upload -> Download packaged .zip
                elif len(converted_files) > 1:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for filename, data in converted_files.items():
                            zip_file.writestr(filename, data)
                            
                    st.download_button(
                        label="Download All (.docx) Files as ZIP",
                        data=zip_buffer.getvalue(),
                        file_name="pdf_converted_word_files.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                st.markdown("---")
                st.info("💡 To start over, click 'Clear / Reset Form' below or drop new files.")

    # Reset Button
    if st.button("Clear / Reset Form", type="secondary", use_container_width=True):
        st.rerun()