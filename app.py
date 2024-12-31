from flask import Flask, request, jsonify
from backend import memory, call_deepseek_api  # Import the DeepSeek API tool

app = Flask(__name__)

# Root route
@app.route("/")
def home():
    return "Welcome to the AI Customer Support Agent! Use the /chat endpoint to interact with the chatbot."

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    
    # Use the DeepSeek API for all responses
    response = call_deepseek_api(user_query)
    
    # Log the interaction in memory
    memory.save_context({"input": user_query}, {"output": response})
    
    # Return the response
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)