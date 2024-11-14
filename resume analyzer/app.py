import os
from flask import Flask, render_template, request, redirect, url_for
from docx import Document
import PyPDF2
import language_tool_python

# Initialize the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool('en-US')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def analyze_resume(filepath):
    """Analyze the resume and return scores and feedback."""
    file_extension = os.path.splitext(filepath)[1].lower()
    resume_text = ""

    if file_extension == '.docx':
        # For DOCX files
        doc = Document(filepath)
        for para in doc.paragraphs:
            resume_text += para.text + "\n"
    elif file_extension == '.pdf':
        # For PDF files
        resume_text = extract_text_from_pdf(filepath)
    else:
        raise ValueError("Unsupported file type. Please upload a .docx or .pdf file.")

    # Grammar check
    matches = tool.check(resume_text)
    grammar_score = max(0, 100 - len(matches))  # Simple grammar score based on error count
    
    # Extract feedback messages for each grammar issue
    grammar_feedback = []
    for match in matches:
        message = f"Issue: {match.message}, Context: {match.context}, Suggestion: {', '.join(match.replacements)}"
        grammar_feedback.append(message)

    # Alignment and presentation scores (fixed for demonstration)
    alignment_score = 95  
    presentation_score = 85  

    return grammar_score, alignment_score, presentation_score, grammar_feedback


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Analyze the uploaded resume
    grammar_score, alignment_score, presentation_score, grammar_feedback = analyze_resume(filepath)

    # Calculate overall score as an average (for demonstration)
    overall_score = (grammar_score + alignment_score + presentation_score) / 3

    return render_template('index.html', 
                           grammar_score=grammar_score,
                           alignment_score=alignment_score,
                           presentation_score=presentation_score,
                           overall_score=overall_score,
                           grammar_feedback=grammar_feedback)

if __name__ == '__main__':
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
