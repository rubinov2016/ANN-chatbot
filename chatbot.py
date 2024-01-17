import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import re
import tkinter as tk
from tkinter import scrolledtext

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

for intent in intents["intents"]:
    intent["patterns"] = [pattern.lower() for pattern in intent["patterns"]]

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.keras')

#Clean up the sentences
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

#Convert the sentences into a bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence) #bow: Bag Of Words, feed the data into the neural network
    res = model.predict(np.array([bow]))[0] #res: result. [0] as index 0

    ERROR_THRESHOLD = 0.5
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # Use the flag to debugging
    if decrease_error_threshold:
        while results == [] and ERROR_THRESHOLD > 0.1:
            ERROR_THRESHOLD -= 0.01
            results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
    # Own addition. Handle an exception
    except IndexError:
        result = "I don't know. Please rephrase your question"
    # end of Own addition
    return result

print("COM727 Chatbot is here!")

# Own addition. Logs all chatbot history
from datetime import datetime
import socket
computer_name = socket.gethostname()
file_name = f"{computer_name}_chat_log.txt"

# Load replacement.json to change underscored words from dataset (readme.md)
json_file = 'replacements.json'
# Load the JSON file as a dictionary
with open(json_file, 'r') as file:
    replacements = json.load(file)


def replace_words(text, replacements):
    for key, value in replacements.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        text = re.sub(pattern, value, text)
    return text

def send_response():
    try:
        message = user_entry.get()
        if message.lower() == 'exit':
            root.quit()
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            num_words = len(message.split())
            if num_words >= 3 or message.lower() in ["hello", "hi", "hey", "hello!", "hi!", "hey!"]:
                message = replace_words(message, replacements)
                ints = predict_class(message)
                response = get_response(ints, intents)
                if show_details:
                    response = response + "          " + json.dumps(ints)
            else:
                response = "Your question is too short, can you restate it?"
            log_data = {
                "timestamp": timestamp,
                "input_message": message,
                "output_response": response
            }

            # Display conversation in the text widget
            conversation_text = f"{timestamp} - You: {user_entry.get()}\n com727: {response}\n\n"
            conversation.insert(tk.END, conversation_text)
            conversation.see(tk.END)

            # Save conversation log to a file
            if show_details:
                with open(file_name, 'a') as log_file:
                    log_file.write(json.dumps(log_data) + '\n')

            # Clear the message entry
            user_entry.delete(0, tk.END)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Create the main window or root window
root = tk.Tk()
root.title("World Cup 2022")

# Entry field where the user can type messages
user_entry = tk.Entry(root, width=90)
user_entry.grid(row=1, column=0, padx=12, pady=12)

# Create button Send
send_button = tk.Button(root, text="SEND", command=send_response, font=("Helvetica", 14))
send_button.grid(row=1, column=1, padx=12, pady=12)

user_entry.focus()
# Enter button invoke sending the message
user_entry.bind('<Return>', lambda event=None: send_response())

# Create a scrolled text widget to display the conversation
conversation = scrolledtext.ScrolledText(root, width=90, height=20, wrap=tk.WORD)
conversation.grid(row=0, column=0, padx=12, pady=12, columnspan=2)

# Create the greeting message
greeting = "Welcome to Coding Avengers! Ask me about World Cup 2022"
conversation.insert(tk.END, f" com727: {greeting}\n\n")
conversation.see(tk.END)

# Set 'show_details' to True if you want to display additional details
show_details = False
# Set 'decrease_error_threshold' to True if you want to debug predicting below Threshold
decrease_error_threshold = False

# Run the interface
root.mainloop()

