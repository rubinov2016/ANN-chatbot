import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

#Ivan addition 1
#Lower case
for intent in intents["intents"]:
    intent["patterns"] = [pattern.lower() for pattern in intent["patterns"]]
#end of Ivan addition 1

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.keras')

#Clean up the sentences
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    # sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

#Converts the sentences into a bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    # print(sentence_words)
    # print(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence) #bow: Bag Of Words, feed the data into the neural network
    res = model.predict(np.array([bow]))[0] #res: result. [0] as index 0
    # ERROR_THRESHOLD = 0.25
    # Ivan addition 2
    ERROR_THRESHOLD = 0.5
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    while results == [] and ERROR_THRESHOLD > 0.1:
        ERROR_THRESHOLD -= 0.01
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # end of Ivan addition 2

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
    #Ivan addition
    except IndexError:
        result = "I don't know"
    # end of Ivan addition
    return result

print("COM727 Chatbot is here!")

# Ivan addition 3
import time
from datetime import datetime
import socket
computer_name = socket.gethostname()
file_name = f"{computer_name}_chat_log.txt"

import re


json_file = 'replacements.json'
# Load the JSON file as a dictionary
with open(json_file, 'r') as file:
    replacements = json.load(file)


def replace_words(text, replacements):
    for key, value in replacements.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        text = re.sub(pattern, value, text)
    return text
# end of Ivan addition 3


def send_message():
    try:
        message = message_entry.get()
        if message.lower() == 'exit':
            root.quit()
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            num_words = len(message.split())
            if num_words >= 3 or message in ["hello", "hi", "hey"]:
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
            conversation_text = f"{timestamp} - You: {message}\n com728: {response}\n\n"
            text_widget.insert(tk.END, conversation_text)

            # Save conversation log to a file
            with open(file_name, 'a') as log_file:
                log_file.write(json.dumps(log_data) + '\n')

            # Clear the message entry
            message_entry.delete(0, tk.END)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

import tkinter as tk
from tkinter import scrolledtext
# GUI setup
root = tk.Tk()
root.title("World cup 2022")

# Create and configure the message entry widget
message_entry = tk.Entry(root, width=50)
message_entry.grid(row=1, column=0, padx=10, pady=10)

# Create a button to send messages
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)
# ready for the user to type their next message.
message_entry.focus()
#enter button sends the message
message_entry.bind('<Return>', lambda event=None: send_message())

# Create a scrolled text widget to display the conversation
text_widget = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
text_widget.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Set show_details to True if you want to display additional details
show_details = False

# Run the GUI
root.mainloop()