import streamlit as st
import pandas as pd
import io
import zipfile
import pdfplumber

# Page Configuration
st.set_page_config(page_title="PDF to Excel - Convert Master", page_icon="📄", layout="wide")

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
        
    st.title("📄 PDF to Excel Converter")
    st.write("Upload your PDF files containing tables (Maximum 5 files). Data will be extracted into modern (.xlsx) format.")

    # Form layout for safe reset
    with st.form("pdf_converter_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Choose PDF files", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        submit_button = st.form_submit_button("Extract Data & Process", use_container_width=True)

    # Core Logic (Using pdfplumber - No Java Needed!)
    if submit_button and uploaded_files:
        # Rule 1: Max 5 files limit check
        if len(uploaded_files) > 5:
            st.error("You can upload a maximum of 5 PDF files at a time. Please reduce files and try again.")
        else:
            st.info(f"Total {len(uploaded_files)} file(s) selected. Processing PDF tables...")
            
            converted_files = {} # Stores processed excel data byte chunks
            
            for uploaded_file in uploaded_files:
                try:
                    excel_buffer = io.BytesIO()
                    
                    # Open PDF with pdfplumber
                    with pdfplumber.open(uploaded_file) as pdf:
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            table_count = 0
                            
                            # Loop through all pages to find tables
                            for page_idx, page in enumerate(pdf.pages):
                                tables = page.extract_tables()
                                
                                for t_idx, table in enumerate(tables):
                                    if table:
                                        # Convert extracted layout to DataFrame
                                        df = pd.DataFrame(table)
                                        
                                        # Clean data: Use the first row as columns if valid
                                        if not df.empty:
                                            df.columns = df.iloc[0]
                                            df = df[1:].reset_index(drop=True)
                                            
                                        # Save table to Excel Sheet
                                        table_count += 1
                                        df.to_excel(writer, sheet_name=f"Page{page_idx+1}_Table{t_idx+1}", index=False)
                            
                            # Fallback: If no structured tables found, extract raw text lines
                            if table_count == 0:
                                text_data = []
                                for page in pdf.pages:
                                    text = page.extract_text()
                                    if text:
                                        text_data.extend([line.split() for line in text.split('\n')])
                                
                                if text_data:
                                    df = pd.DataFrame(text_data)
                                    df.to_excel(writer, sheet_name="Extracted_Text", index=False)
                                else:
                                    pd.DataFrame(["No legible tables or text found."]).to_excel(writer, sheet_name="Blank", index=False)
                                    
                    new_filename = uploaded_file.name.replace(".pdf", ".xlsx")
                    converted_files[new_filename] = excel_buffer.getvalue()
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")

            # Download Handling Logic
            if len(converted_files) > 0:
                st.success(f"Successfully processed {len(converted_files)} file(s)!")
                
                # Rule 3: Single file upload -> Direct download .xlsx
                if len(converted_files) == 1:
                    filename, data = list(converted_files.items())[0]
                    st.download_button(
                        label=f"Download {filename}",
                        data=data,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                # Rule 4: More than one file upload -> Download packaged .zip
                elif len(converted_files) > 1:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for filename, data in converted_files.items():
                            zip_file.writestr(filename, data)
                            
                    st.download_button(
                        label="Download All (.xlsx) Files as ZIP",
                        data=zip_buffer.getvalue(),
                        file_name="pdf_converted_sheets.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                st.markdown("---")
                st.info("💡 To start over, simply click 'Clear / Reset Form' below or drop new files.")

    # Reset Button
    if st.button("Clear / Reset Form", type="secondary", use_container_width=True):
        st.rerun()