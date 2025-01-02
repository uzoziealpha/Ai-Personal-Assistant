from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
import requests
from textblob import TextBlob
import sqlite3
from googletrans import Translator
from werkzeug.utils import secure_filename
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fpdf import FPDF

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
translator = Translator()

# Replace with your DeepSeek API key
DEEPSEEK_API_KEY = ""

# DeepSeek API endpoint (replace with the actual endpoint)
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Example endpoint

# Load knowledge base
loader = TextLoader("knowledge_base.txt")
documents = loader.load()

# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Add memory for context-aware responses
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Email configuration (replace with your email credentials)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'your-email@gmail.com'
EMAIL_PASSWORD = 'your-email-password'

# Tool Integration
def query_database(query):
    return "Database response for: " + query

def send_email(content):
    return "Email sent with content: " + content

# Multilingual Support
def translate_text(text, target_language="en"):
    """
    Translates text into the target language using Google Translate API.
    """
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return the original text if translation fails

# Sentiment Analysis
def analyze_sentiment(text):
    """
    Analyzes the sentiment of the text and returns a polarity score.
    """
    analysis = TextBlob(text)
    return analysis.sentiment.polarity  # Returns a value between -1 (negative) and 1 (positive)

# Metrics Dashboard
def log_query(query, response):
    """
    Logs the user query and response in a database.
    """
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS queries (query TEXT, response TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("INSERT INTO queries (query, response) VALUES (?, ?)", (query, response))
    conn.commit()
    conn.close()

# DeepSeek API Call
def call_deepseek_api(query, target_language="en"):
    """
    Calls the DeepSeek API and translates the response if needed.
    """
    # Translate the query if the target language is not English
    if target_language != "en":
        query = translate_text(query, target_language)
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Replace with the correct model name
        "messages": [
            {"role": "user", "content": query}
        ]
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        response_text = response.json()["choices"][0]["message"]["content"]
        # Translate the response back to the target language
        if target_language != "en":
            response_text = translate_text(response_text, target_language)
        # Adapt the response based on sentiment
        sentiment = analyze_sentiment(query)
        if sentiment < -0.5:
            response_text = f"I'm sorry to hear that. {response_text}"
        elif sentiment > 0.5:
            response_text = f"Great to hear! {response_text}"
        return response_text
    else:
        return f"Error: {response.status_code} - {response.text}"

# Tool List
tools = [
    Tool(name="Query Database", func=query_database, description="Query an external database"),
    Tool(name="Send Email", func=send_email, description="Send an email"),
    Tool(name="Call DeepSeek API", func=call_deepseek_api, description="Call the DeepSeek API for creative responses")
]

# File Upload
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully", "filename": filename})
    return jsonify({"error": "File type not allowed"}), 400

# Gamification
user_scores = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    language = data.get('language', 'en')
    user_id = data.get('user_id', 'default_user')  # Add user ID for gamification

    # Call DeepSeek API for the response
    response = call_deepseek_api(query, target_language=language)

    # Update user score
    user_scores[user_id] = user_scores.get(user_id, 0) + 1

    # Log the query and response
    log_query(query, response)

    return jsonify({"response": response, "score": user_scores[user_id]})

# Metrics route to fetch logged queries
@app.route('/metrics', methods=['GET'])
def metrics():
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute("SELECT query, response, timestamp FROM queries")
    data = cursor.fetchall()
    conn.close()

    # Format data for the frontend
    metrics_data = [
        {"query": row[0], "response": row[1], "timestamp": row[2]} for row in data
    ]
    return jsonify(metrics_data)

# Export logs as PDF
@app.route('/export-pdf', methods=['GET'])
def export_pdf():
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute("SELECT query, response, timestamp FROM queries")
    data = cursor.fetchall()
    conn.close()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for row in data:
        pdf.cell(200, 10, txt=f"Query: {row[0]}", ln=True)
        pdf.cell(200, 10, txt=f"Response: {row[1]}", ln=True)
        pdf.cell(200, 10, txt=f"Timestamp: {row[2]}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)  # Add space between entries

    pdf_file = "logs.pdf"
    pdf.output(pdf_file)

    return send_file(pdf_file, as_attachment=True)

# Send logs via email
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email address is required"}), 400

    # Create PDF
    pdf_file = "logs.pdf"
    export_pdf()  # Generate the PDF

    # Send email with PDF attachment
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = "Chatbot Logs"

    with open(pdf_file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={pdf_file}",
        )
        msg.attach(part)

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)