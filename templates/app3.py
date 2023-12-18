from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['user_input']

    # Your chatbot logic goes here
    # For simplicity, let's assume the bot responds with a hardcoded message
    bot_response = "Hello! I'm a chatbot."

    return jsonify({'user_message': user_input, 'bot_message': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
