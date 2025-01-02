from flask import Flask, request, jsonify, render_template, send_from_directory
from backend import memory, call_deepseek_api, log_query

app = Flask(__name__)

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# Root route
@app.route("/")
def home():
    return render_template("index.html")

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query")
    target_language = request.json.get("language", "en")  # Default to English
    
    # Use the DeepSeek API for all responses
    response = call_deepseek_api(user_query, target_language)
    
    # Log the interaction in memory
    memory.save_context({"input": user_query}, {"output": response})
    
    # Log the query and response in the metrics database
    log_query(user_query, response)
    
    # Return the response
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)