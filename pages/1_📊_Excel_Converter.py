import streamlit as st
import pandas as pd
import io
import zipfile

# Page Configuration for this specific tool
st.set_page_config(page_title="Excel Converter - Convert Master", page_icon="📊", layout="wide")

# Custom CSS for spacing and width reduction
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .back-btn-container { margin-top: 25px; margin-bottom: 20px; }
    
    /* Styling back button page link to look secondary/neutral */
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

# Centered 3-column layout to keep the upload box neat (Width Control)
left_space, center_content, right_space = st.columns([1, 2, 1])

with center_content:
    # Back to Dashboard Link with safety top margin
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    st.page_link("app.py", label="Back to Dashboard", icon="⬅️")
    st.markdown('</div>', unsafe_allow_html=True)
        
    st.title(".xls to .xlsx Converter")
    st.write("Upload your old (.xls) files (Maximum 20 files). All files will be automatically converted and packaged into a single .zip file for download.")

    # Form layout for safe reset
    with st.form("converter_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Choose .xls files", 
            type=["xls"], 
            accept_multiple_files=True
        )
        submit_button = st.form_submit_button("Process Files", use_container_width=True)

    # Core Conversion Logic
    if submit_button and uploaded_files:
        if len(uploaded_files) > 20:
            st.error("You can upload a maximum of 20 files at a time. Please remove the extra files and try again.")
        else:
            st.info(f"Total {len(uploaded_files)} file(s) selected. Processing started...")
            
            # Setup zip memory buffer
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                success_count = 0
                
                for uploaded_file in uploaded_files:
                    try:
                        # Convert XLS to Dataframe using xlrd
                        df = pd.read_excel(uploaded_file, engine='xlrd')
                        
                        # Write Dataframe to XLSX openpyxl buffer
                        excel_buffer = io.BytesIO()
                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                            df.to_excel(writer, index=False)
                        
                        # Prepare filename and push to zip archive
                        new_filename = uploaded_file.name.replace(".xls", ".xlsx")
                        zip_file.writestr(new_filename, excel_buffer.getvalue())
                        success_count += 1
                    except Exception as e:
                        st.error(f"Error converting {uploaded_file.name}: {e}")
                
            # If at least one file successfully converted
            if success_count > 0:
                st.success(f"Successfully converted {success_count} file(s)!")
                st.download_button(
                    label="Download All (.xlsx) Files as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="converted_excel_files.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                st.markdown("---")
                st.info("💡 To start a new process, click 'Clear / Reset Form' below or drop new files.")

    # Standalone Clear Form button
    if st.button("Clear / Reset Form", type="secondary", use_container_width=True):
        st.rerun()