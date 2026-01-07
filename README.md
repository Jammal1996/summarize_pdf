AI PDF SUMMARIZER - HOW TO RUN THE APP
================================

This document explains how to run the AI PDF Summarizer application
(step by step) on your local machine.

--------------------------------------------------
1. PREREQUISITES
--------------------------------------------------

Make sure you have the following installed:

- Python 3.9 or higher
- pip (Python package manager)
- A modern web browser (Chrome, Firefox, Edge)

(Optional but recommended)
- Virtual environment support (venv)


--------------------------------------------------
2. PROJECT STRUCTURE
--------------------------------------------------

Your project folder should look like this:

pdf_summarizer_api/
│
├── app.py
├── requirements.txt
├── uploads/
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js


--------------------------------------------------
3. CREATE A VIRTUAL ENVIRONMENT (RECOMMENDED)
--------------------------------------------------

Open a terminal inside the project folder and run:

Windows:
    python -m venv venv
    venv\Scripts\activate

macOS / Linux:
    python3 -m venv venv
    source venv/bin/activate


--------------------------------------------------
4. INSTALL DEPENDENCIES
--------------------------------------------------

Install all required Python packages using:

    pip install -r requirements.txt

This will install:
- Flask
- Transformers
- Torch
- LangChain
- PyPDF
- Other required libraries


--------------------------------------------------
5. RUN THE APPLICATION
--------------------------------------------------

Start the Flask application by running:

    python app.py

You should see output similar to:

    Running on http://127.0.0.1:5000


--------------------------------------------------
6. OPEN THE WEB APPLICATION
--------------------------------------------------

Open your browser and go to:

    http://localhost:5000

From the web page you can:
- Upload a PDF file
- Choose summary length (short / medium / long)
- Enable dark mode
- Download the generated summary


--------------------------------------------------
7. USING THE API (OPTIONAL)
--------------------------------------------------

You can also use the API directly.

Endpoint:
    POST /summarize

Required form-data:
- file   : PDF file
- length : short | medium | long

Example using curl:

    curl -X POST http://localhost:5000/summarize \
         -F "file=@document.pdf" \
         -F "length=medium"


--------------------------------------------------
8. COMMON ISSUES
--------------------------------------------------

1) Models take time to load on first run
   -> This is normal, especially on CPU.

2) 'undefined' appears on the web page
   -> Make sure you uploaded a valid text-based PDF.

3) Dark mode text not visible
   -> Ensure you are using the latest style.css file.

4) GPU not detected
   -> The app works on CPU by default.
      GPU is optional, not required.


--------------------------------------------------
9. STOPPING THE APP
--------------------------------------------------

To stop the server, press:

    CTRL + C

in the terminal where the app is running.


--------------------------------------------------
10. NOTES
--------------------------------------------------

- This application is intended for educational and experimental use.
- AI-generated summaries may not always be 100% accurate.
- Large PDFs may take longer to process.

--------------------------------------------------
Enjoy using the AI PDF Summarizer!
--------------------------------------------------
