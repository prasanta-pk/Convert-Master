import streamlit as st
import io

# --- BULLETPROOF IMPORT FOR PYTHON 3.14 ---
try:
    from pypdf import PdfWriter, PdfReader
    has_writer = True
except ImportError:
    try:
        from PyPDF2 import PdfWriter, PdfReader  # type: ignore
        has_writer = True
    except ImportError:
        has_writer = False

# Page Configuration
st.set_page_config(page_title="Merge PDF - Convert Master", page_icon="📚", layout="wide")

# --- CUSTOM CSS FOR BACK TO HOME BUTTON & STYLING ---
st.markdown("""
    <style>
    /* Premium Styling for Back to Home Link */
    .back-home-container {
        margin-bottom: 25px;
    }
    .back-home-link {
        display: inline-flex;
        align-items: center;
        text-decoration: none !important;
        color: #7f8c8d !important;
        font-weight: 600;
        font-size: 15px;
        transition: color 0.2s ease-in-out;
    }
    .back-home-link:hover {
        color: #bf4e19 !important; /* Your theme orange color */
    }
    </style>
""", unsafe_allow_html=True)

# --- BACK TO HOME BUTTON ---
st.markdown("""
    <div class="back-home-container">
        <a href="/" target="_self" class="back-home-link">⬅ Back to Home Dashboard</a>
    </div>
""", unsafe_allow_html=True)

st.title("📚 Merge PDF Documents")
st.write("Combine multiple PDF files into a single document in your preferred sequence.")

# Initialize dynamic reset trigger in session state if not exists
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = "pdf_input_v1"
if "merged_pdf_data" not in st.session_state:
    st.session_state["merged_pdf_data"] = None
if "reset_form" not in st.session_state:
    st.session_state["reset_form"] = False

# Trigger form reset if requested in previous rerun
if st.session_state["reset_form"]:
    st.session_state["uploader_key"] = f"pdf_input_{st.time() if hasattr(st, 'time') else 123}" # Unique token to force redraw
    st.session_state["merged_pdf_data"] = None
    st.session_state["reset_form"] = False
    st.rerun()

if not has_writer:
    st.error("❌ Required PDF libraries are missing! Please run `pip install pypdf` in your terminal.")
else:
    # File Uploader with Dynamic Key for resetting
    uploaded_files = st.file_uploader(
        "Choose PDF files to merge", 
        type=["pdf"], 
        accept_multiple_files=True,
        key=st.session_state["uploader_key"]
    )

    if uploaded_files:
        st.markdown("---")
        st.subheader("🔄 Arrange File Sequence (I Love PDF Style)")
        st.info("💡 Adjust the order of files below by assigning them sequence numbers. The file with number 1 will appear first.")
        
        file_list = []
        
        # Layout for files configuration
        for idx, file in enumerate(uploaded_files):
            try:
                file.seek(0)
                pdf_reader = PdfReader(file)
                page_count = len(pdf_reader.pages)
                page_info = f"{page_count} pages"
            except:
                page_info = "Unknown pages"
                
            col_name, col_pages, col_order = st.columns([5, 2, 2])
            
            with col_name:
                st.markdown(f"**📄 {file.name}**")
            with col_pages:
                st.markdown(f"`{page_info}`")
            with col_order:
                order_num = st.number_input(
                    f"Position for File {idx+1}", 
                    min_value=1, 
                    max_value=len(uploaded_files), 
                    value=idx+1, 
                    key=f"order_{file.name}_{idx}"
                )
                file_list.append({"file": file, "order": order_num, "name": file.name})
                
        # Sort files according to user-defined priority numbers
        sorted_files = sorted(file_list, key=lambda x: x["order"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Preview of final order
        st.markdown("**Final Merge Sequence Preview:**")
        sequence_preview = " ➔ ".join([f"[{item['order']}] {item['name']}" for item in sorted_files])
        st.code(sequence_preview, language="text")

        # Action Button to Merge
        if st.button("🚀 Merge PDFs", type="primary", use_container_width=True):
            with st.spinner("Merging your PDF documents... Please wait..."):
                try:
                    writer = PdfWriter()
                    
                    for item in sorted_files:
                        current_file = item["file"]
                        current_file.seek(0) 
                        
                        reader = PdfReader(current_file)
                        for page in reader.pages:
                            writer.add_page(page)
                    
                    # Write output directly to RAM buffer
                    output_pdf = io.BytesIO()
                    writer.write(output_pdf)
                    writer.close()
                    output_pdf.seek(0)
                    
                    # Save bytes to state
                    st.session_state["merged_pdf_data"] = output_pdf.getvalue()
                    st.success("🎉 Successfully Merged All PDFs! Ready to download.")
                    
                except Exception as e:
                    st.error(f"An error occurred while merging: {str(e)}")
        
        # Display Download Button if merged data exists
        if st.session_state["merged_pdf_data"] is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Reset handler trigger via button click callback
            def handle_download_click():
                st.session_state["reset_form"] = True

            st.download_button(
                label="📥 Download Merged PDF & Reset Form",
                data=st.session_state["merged_pdf_data"],
                file_name="Merged_Document.pdf",
                mime="application/pdf",
                use_container_width=True,
                on_click=handle_download_click
            )
            
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("📂 Please upload two or more PDF files above to unlock sequencing and merging options.")