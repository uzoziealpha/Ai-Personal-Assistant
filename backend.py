from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
import requests

# Replace with your DeepSeek API key
DEEPSEEK_API_KEY = ""

# DeepSeek API endpoint (replace with the actual endpoint)
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Example endpoint

def call_deepseek_api(query):
    """
    Calls the DeepSeek API to generate a response based on the user's query.
    """
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
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

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

tools = [
    Tool(name="Query Database", func=query_database, description="Query an external database"),
    Tool(name="Send Email", func=send_email, description="Send an email"),
    Tool(name="Call DeepSeek API", func=call_deepseek_api, description="Call the DeepSeek API for creative responses")
]