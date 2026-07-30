# AI Resume Analyzer

## Generative AI Internship – Week 3 Project

The **AI Resume Analyzer** is a Generative AI-powered web application that analyzes a candidate's resume and evaluates how well it matches a selected target job role.

The application extracts text from an uploaded PDF resume and uses Google's Gemini API to identify skills, keywords, missing skills, strengths, weaknesses, and areas for improvement.

---

## Features

* 📄 Upload resume in PDF format
* 🔍 Extract text from the uploaded resume
* 🛠️ Identify technical and professional skills
* 🔑 Analyze important resume keywords
* ⚠️ Identify missing job-related keywords
* 📊 Generate a resume-job match score
* 💪 Identify resume strengths
* 🔧 Identify resume weaknesses
* 🤖 Generate AI-powered improvement suggestions
* 📥 Download the analysis report
* 🌐 Simple and responsive Streamlit interface

---

## Technologies Used

* **Python** – Application development
* **Streamlit** – Web application interface
* **Google Gemini API** – Generative AI analysis
* **PyPDF2** – PDF text extraction
* **python-dotenv** – Environment variable management

---

## Project Structure

```text
AI_Resume_Analyzer/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

## Requirements

Before running the project, make sure you have:

* Python 3.10 or above
* Internet connection
* Google Gemini API key

---

## Installation

### 1. Download or clone the project

Open the project folder in Visual Studio Code.

### 2. Create a virtual environment

Open the terminal and run:

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install required packages

Run:

```bash
pip install -r requirements.txt
```

---

## Gemini API Configuration

The application requires a Google Gemini API key.

Create an API key through Google AI Studio.

After obtaining the key, create a file named:

```text
.env
```

in the project folder.

Add:

```text
GEMINI_API_KEY=your_actual_gemini_api_key
```

Replace `your_actual_gemini_api_key` with your own API key.

### Important

Do not share your API key publicly.

The `.env` file should not be uploaded to GitHub or included in the final project submission.

The project includes `.env.example` as a template:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## Running the Application

After activating the virtual environment, run:

```bash
streamlit run app.py
```

The application will open in your browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

---

## How to Use

### Step 1 – Upload Resume

Upload your resume in **PDF format** using the file uploader.

### Step 2 – Enter Target Job Role

Enter the position you want to apply for.

Examples:

```text
Data Scientist
```

```text
Machine Learning Engineer
```

```text
Python Developer
```

### Step 3 – Analyze Resume

Click:

**Analyze Resume**

The AI will analyze the uploaded resume according to the selected job role.

### Step 4 – Review Results

The application displays:

* Resume Match Score
* Skills Found
* Keywords Found
* Missing Keywords
* Strengths
* Weaknesses
* AI Improvement Suggestions

### Step 5 – Download Report

Use the **Download Analysis Report** button to save the analysis results as a text file.

---

## Example Workflow

```text
Resume PDF
     ↓
PDF Text Extraction
     ↓
Target Job Role
     ↓
Google Gemini AI
     ↓
Resume Analysis
     ↓
┌──────────────────────────────┐
│ Resume Match Score           │
│ Skills                       │
│ Keywords                     │
│ Missing Keywords             │
│ Strengths                    │
│ Weaknesses                   │
│ Improvement Suggestions      │
└──────────────────────────────┘
     ↓
Download Report
```

---

## Security

The Gemini API key is stored locally in the `.env` file.

Never publish or share the `.env` file containing your real API key.

The `.gitignore` file is included to prevent sensitive files such as `.env` and the virtual environment from being committed accidentally.

---

## Limitations

* Currently supports PDF resumes.
* Scanned/image-only PDFs may not provide extractable text.
* AI-generated scores and suggestions should be treated as guidance rather than professional recruitment decisions.
* Analysis quality depends on the content and structure of the uploaded resume.

---

## Future Enhancements

Possible future improvements include:

* Support for DOCX resumes
* Job description upload and comparison
* ATS compatibility analysis
* Resume section classification
* Resume rewriting suggestions
* Skill-gap analysis
* Resume improvement recommendations
* Database for storing previous analyses
* Resume analytics dashboard
* Export reports as PDF

---

## Author

**Generative AI Internship – Week 3 Project**

### Project Title

**AI Resume Analyzer**

Built using Python, Streamlit, and Google Gemini Generative AI.
