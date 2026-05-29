# 🔄 Convert Master

Convert Master is a premium, web-based utility platform built with **Streamlit** and **Python 3.14**. It offers a unified dashboard with an elegant, interactive glassmorphic UI to handle multiple file conversion and utility tasks seamlessly in one place.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## ✨ Features

### 🎛️ Interactive Dashboard (UI/UX)
- **Glassmorphic Hover Cards:** Smooth animations with real-time text-blurring effects and floating action buttons on mouse hover.
- **Unified Navigation:** Custom styled sidebar navigation tracking "Currently Active Tools" along with quick "Back to Home" routing.
- **Stretched HTML5 Anchors:** 100% bulletproof inside-card routing built to bypass native Streamlit iframe sandbox limitations.

### 🛠️ Core Utility Modules
- **📊 .xls to .xlsx Converter:** Batch convert legacy Excel sheets to modern optimized file formats (Supports up to 20 files simultaneously).
- **📄 PDF to Excel Converter:** Extract structural tables directly from PDF documents into spreadsheet formats (Supports up to 5 files).
- **📝 PDF to Word Converter:** Convert static PDF layouts into highly editable `.docx` files accurately.
- **🔀 Excel Merger (Joiner):** Seamlessly merge multiple Excel files sharing identical row headings into a single master file.
- **📚 Merge PDF (I Love PDF Style):** - Upload multiple PDFs at once.
  - Live page counting feature per file.
  - Interactive file sequence/priority ordering arrangement.
  - In-memory processing using `PdfWriter` buffers for instant download with a secure auto-reset system.

---

## 🚀 Installation & Local Setup

Follow these steps to clone and run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/prasanta-pk/Convert-Master.git](https://github.com/prasanta-pk/Convert-Master.git)
cd Convert-Master
