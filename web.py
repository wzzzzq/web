from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")  # Ensure Flask looks in the "templates" folder
CORS(app)  # Allow requests from other devices

messages = []  # Store all received messages

# ✅ Homepage route
@app.route('/')
def index():
    return render_template('index.html', messages=messages)  # Pass messages to the template

# ✅ Handle incoming messages
@app.route('/send-message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    messages.append(user_message)  # Store message

    response_message = f"Server received: {user_message}"
    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
