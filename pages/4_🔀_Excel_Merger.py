import streamlit as st
import pandas as pd
import io

# Page Configuration
st.set_page_config(page_title="Excel Merger - Convert Master", page_icon="🔀", layout="wide")

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
        
    st.title("🔀 Excel Merger (With Heading Validation)")
    st.write("Merge multiple Excel files (.xlsx or .xls) into a single file. **System will validate headings automatically before merging.**")

    # Form layout for safe reset
    with st.form("excel_merger_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Upload Excel files (No Limit)", 
            type=["xlsx", "xls"], 
            accept_multiple_files=True
        )
        submit_button = st.form_submit_button("Merge Files Now", use_container_width=True)

    # Core Merger Logic with Dynamic Heading Validation
    if submit_button and uploaded_files:
        if len(uploaded_files) < 2:
            st.error("Please upload at least 2 Excel files to perform a merge.")
        else:
            st.info(f"Analyzing and validating headings of {len(uploaded_files)} file(s)...")
            
            all_dfs = []
            base_columns = None
            base_file_name = ""
            validation_failed = False
            
            for uploaded_file in uploaded_files:
                try:
                    engine_type = 'xlrd' if uploaded_file.name.endswith('.xls') else 'openpyxl'
                    df = pd.read_excel(uploaded_file, engine=engine_type)
                    
                    if not df.empty:
                        current_columns = list(df.columns)
                        
                        # প্রথম ফাইলের কলামকে আমরা বেঞ্চমার্ক/বেস হিসেবে ধরব
                        if base_columns is None:
                            base_columns = current_columns
                            base_file_name = uploaded_file.name
                            all_dfs.append(df)
                        else:
                            # পরবর্তী ফাইলগুলোর কলাম বেস ফাইলের সাথে মিলছে কিনা তা চেক হবে
                            if current_columns == base_columns:
                                all_dfs.append(df)
                            else:
                                validation_failed = True
                                st.error(f"❌ **Heading Mismatch Found!** File **'{uploaded_file.name}'** does not match with base file **'{base_file_name}'**.")
                                
                                # ইউজারকে সহজে বোঝানোর জন্য কলামের পার্থক্যগুলো দেখানো
                                with st.expander(f"View Heading Difference for {uploaded_file.name}"):
                                    st.write(f"**Expected Headings (from {base_file_name}):** {base_columns}")
                                    st.write(f"**Found Headings (in {uploaded_file.name}):** {current_columns}")
                                    
                except Exception as e:
                    validation_failed = True
                    st.error(f"Could not read {uploaded_file.name}: {e}")
            
            # ডেটা কম্বাইন করার চুড়ান্ত সিদ্ধান্ত
            if validation_failed:
                st.warning("⚠️ **Merge Aborted!** Please fix the column structure/headings of the incorrect files and try again.")
            elif all_dfs:
                try:
                    # সবগুলো ফাইলের কলাম সেম থাকলে তবেই এখানে আসবে
                    merged_df = pd.concat(all_dfs, ignore_index=True)
                    
                    output_buffer = io.BytesIO()
                    with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
                        merged_df.to_excel(writer, index=False, sheet_name="Merged_Data")
                    
                    st.success(f"🎉 **Success!** All {len(all_dfs)} files matched perfectly and merged! Total Rows: {len(merged_df)}")
                    
                    # ডাউনলোড বাটন
                    st.download_button(
                        label="Download Merged Excel File (.xlsx)",
                        data=output_buffer.getvalue(),
                        file_name="merged_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"An unexpected error occurred during processing: {e}")
            else:
                st.error("No valid data found in the uploaded files.")

            st.markdown("---")
            st.info("💡 To start a new merge session, click 'Clear / Reset Form' below.")

    # Reset Button
    if st.button("Clear / Reset Form", type="secondary", use_container_width=True):
        st.rerun()