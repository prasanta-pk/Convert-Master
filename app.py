import streamlit as st

# App Configuration
st.set_page_config(page_title="Convert Master", page_icon="🔄", layout="wide")

# Custom CSS for Pure In-Card Hover, Clickable Links & Sidebar Title
st.markdown("""
    <style>
    /* Main dashboard background and spacing */
    .block-container { 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
    }
    
    /* --- SIDEBAR CUSTOM NAVIGATION TITLE --- */
    /* Streamlit-er home page sidebar list-er opore custom text injection */
    [data-testid="stSidebarNav"]::before {
        content: "Currently Active Tools";
        display: block;
        padding: 20px 20px 10px 20px;
        font-size: 18px;
        font-weight: 700;
        color: #bf4e19; /* Theme orange color */
        border-bottom: 1px solid #eef2f5;
        margin-bottom: 15px;
    }
    
    /* --- CARD WRAPPER (Parent container) --- */
    .card-wrapper {
        position: relative;
        overflow: hidden; 
        margin-bottom: 24px;
        border-radius: 12px;
        height: 220px; /* Fixed height */
    }
    
    /* --- CARD CONTAINER --- */
    .card-box-active {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eef2f5; 
        height: 100%; 
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        transition: all 0.25s ease-in-out;
    }
    
    /* Smooth scaling effect on wrapper hover */
    .card-wrapper:hover .card-box-active {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: #d1d9e0;
        border-left: 5px solid #bf4e19 !important;
    }
    
    /* --- THE BLURRED OVERLAY LAYER --- */
    .card-blur-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.2);
        opacity: 0;
        transition: all 0.25s ease-in-out;
        z-index: 5; /* Above text, below button */
        pointer-events: none;
        border-radius: 12px;
    }
    
    /* Activate blur overlay only on hover */
    .card-wrapper:hover .card-blur-overlay {
        opacity: 1;
        backdrop-filter: blur(6px);
    }
    
    /* Static Card Style for Coming Soon */
    .card-box-disabled {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eef2f5; 
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        margin-bottom: 24px;
        opacity: 0.75;
    }
    
    /* Icon and Text Styling */
    .card-icon { font-size: 32px; margin-bottom: 12px; }
    .card-title { font-size: 18px; font-weight: 700; color: #2c3e50; margin-bottom: 8px; }
    .card-desc { font-size: 13px; color: #7f8c8d; line-height: 1.4; }
    
    /* Coming Soon Badge */
    .badge-soon {
        background-color: #f1f2f6; 
        color: #a5b1c2; 
        font-size: 11px;
        padding: 2px 6px; 
        border-radius: 4px; 
        font-weight: bold;
        align-self: flex-start; 
        margin-top: auto;
    }
    
    /* --- PURE HTML HOVER BUTTON --- */
    .html-action-btn {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -20%);
        background-color: #bf4e19; 
        color: white !important;
        padding: 12px 28px;
        border-radius: 30px; 
        font-weight: 700;
        font-size: 15px;
        box-shadow: 0 4px 15px rgba(191, 78, 25, 0.4);
        opacity: 0;
        visibility: hidden;
        transition: all 0.25s ease-in-out;
        z-index: 8; 
        white-space: nowrap;
        text-align: center;
    }
    
    /* Reveal HTML button on Hover */
    .card-wrapper:hover .html-action-btn {
        opacity: 1;
        visibility: visible;
        transform: translate(-50%, -50%);
    }
    
    /* --- THE 100% BULLETPROOF LINK LAYER --- */
    .card-main-link {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 15; 
        text-decoration: none !important;
        background-color: rgba(0,0,0,0); 
    }
    </style>
""", unsafe_allow_html=True)

# Dashboard Headers
st.title("🔄 Convert Master")
st.write("Your all-in-one web utility platform for seamless file conversion and processing.")
st.info("💡 Move your mouse over any active card and click to instantly open that tool!")
st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Available Tools & Features")

# Grid Layout (4 Columns per row)
col1, col2, col3, col4 = st.columns(4)

# --- ROW 1 ---

# CARD 1: Live Excel Converter
with col1:
    st.markdown("""
        <div class="card-wrapper">
            <div class="card-box-active">
                <div class="card-icon">📊</div>
                <div class="card-title">.xls to .xlsx Converter</div>
                <div class="card-desc">Convert legacy Excel files into optimized modern formats in bulk (Max 20 files).</div>
            </div>
            <div class="card-blur-overlay"></div>
            <div class="html-action-btn">Convert ➔</div>
            <a href="/Excel_Converter" target="_self" class="card-main-link"></a>
        </div>
    """, unsafe_allow_html=True)

# CARD 2: Live PDF to Excel Converter
with col2:
    st.markdown("""
        <div class="card-wrapper">
            <div class="card-box-active">
                <div class="card-icon">📄</div>
                <div class="card-title">PDF to Excel Converter</div>
                <div class="card-desc">Extract tabular data from PDF files directly into modern Excel sheets (Max 5 files).</div>
            </div>
            <div class="card-blur-overlay"></div>
            <div class="html-action-btn">Convert ➔</div>
            <a href="/PDF_to_Excel" target="_self" class="card-main-link"></a>
        </div>
    """, unsafe_allow_html=True)

# CARD 3: Live PDF to Word Converter
with col3:
    st.markdown("""
        <div class="card-wrapper">
            <div class="card-box-active">
                <div class="card-icon">📝</div>
                <div class="card-title">PDF to Word Converter</div>
                <div class="card-desc">Convert PDF documents into editable Word (.docx) files accurately (Max 5 files).</div>
            </div>
            <div class="card-blur-overlay"></div>
            <div class="html-action-btn">Convert ➔</div>
            <a href="/PDF_to_Word" target="_self" class="card-main-link"></a>
        </div>
    """, unsafe_allow_html=True)

# CARD 4: Live Excel Merger (Joiner)
with col4:
    st.markdown("""
        <div class="card-wrapper">
            <div class="card-box-active">
                <div class="card-icon">🔀</div>
                <div class="card-title">Excel Merger (Joiner)</div>
                <div class="card-desc">Combine multiple Excel files with the same headings into a single unified file (No Limits).</div>
            </div>
            <div class="card-blur-overlay"></div>
            <div class="html-action-btn">Join ➔</div>
            <a href="/Excel_Merger" target="_self" class="card-main-link"></a>
        </div>
    """, unsafe_allow_html=True)


# --- ROW 2 ---
col5, col6, col7, col8 = st.columns(4)

# CARD 5: Active Merge PDF (I Love PDF Style)
with col5:
    st.markdown("""
        <div class="card-wrapper">
            <div class="card-box-active">
                <div class="card-icon">📚</div>
                <div class="card-title">Merge PDF</div>
                <div class="card-desc">Combine multiple PDF documents into a single file in the exact order you want.</div>
            </div>
            <div class="card-blur-overlay"></div>
            <div class="html-action-btn">Merge ➔</div>
            <a href="/Merge_PDF" target="_self" class="card-main-link"></a>
        </div>
    """, unsafe_allow_html=True)

# CARD 6: Split PDF
with col6:
    st.markdown("""
        <div class="card-box-disabled">
            <div class="card-icon">✂️</div>
            <div class="card-title">Split PDF</div>
            <div class="card-desc">Extract specific pages from a PDF file or split each page into independent files.</div>
            <div class="badge-soon">COMING SOON</div>
        </div>
    """, unsafe_allow_html=True)

# CARD 7: Compress PDF
with col7:
    st.markdown("""
        <div class="card-box-disabled">
            <div class="card-icon">📉</div>
            <div class="card-title">Compress PDF</div>
            <div class="card-desc">Reduce your PDF file size drastically while maximizing document quality.</div>
            <div class="badge-soon">COMING SOON</div>
        </div>
    """, unsafe_allow_html=True)

# CARD 8: Image Optimizer
with col8:
    st.markdown("""
        <div class="card-box-disabled">
            <div class="card-icon">🖼️</div>
            <div class="card-title">Image Optimizer</div>
            <div class="card-desc">Compress, resize, or optimize PNG/JPEG files for faster web loading.</div>
            <div class="badge-soon">COMING SOON</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Convert Master v2.9 • Integrated Merge PDF Routing Layer")