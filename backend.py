from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
import requests
from textblob import TextBlob
import sqlite3

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

# Tool Integration
def query_database(query):
    return "Database response for: " + query

def send_email(content):
    return "Email sent with content: " + content

# Multilingual Support
def translate_text(text, target_language="en"):
    """
    Translates text into the target language using a translation API.
    Replace this with an actual translation API call (e.g., Google Translate).
    """
    # Simulate translation
    return f"Translated text: {text} (to {target_language})"

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
    cursor.execute("CREATE TABLE IF NOT EXISTS queries (query TEXT, response TEXT)")
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