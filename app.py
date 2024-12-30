from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to AI Customer Support'})

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_input = data.get('query', '')
    response = {'response': f'You asked: {user_input}'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)