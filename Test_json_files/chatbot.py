import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

import time
import re
from datetime import datetime
import socket
import tkinter as tk


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('../intents.json').read())

#Ivan addition 1
#Lower case
for intent in intents["intents"]:
    intent["patterns"] = [pattern.lower() for pattern in intent["patterns"]]
#end of Ivan addition 1

words = pickle.load(open('../words.pkl', 'rb'))
classes = pickle.load(open('../classes.pkl', 'rb'))
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
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence) #bow: Bag Of Words, feed the data into the neural network
    res = model.predict(np.array([bow]))[0] #res: result. [0] as index 0
    # Ivan addition 2
    # ERROR_THRESHOLD = 0.25
    ERROR_THRESHOLD = 0.5
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    if show_details:
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
    result = ''
    try:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
    #Ivan addition 3
    except IndexError:
        result = "I don't know"
    # end of Ivan addition 3
    return result

print("COM727 Chatbot is here!")

# Ivan addition 4
json_file = '../replacements.json'
# Load the JSON file as a dictionary
with open(json_file, 'r') as file:
    replacements = json.load(file)

def replace_words(text, replacements):
    for key, value in replacements.items():
        pattern = r'\b' + re.escape(key) + r'\b'
        text = re.sub(pattern, value, text)
    return text
# end of Ivan addition 4


computer_name = socket.gethostname()
file_name = f"{computer_name}_chat_log.txt"
def send_message():
    ints = []
    response = ''
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
        with open(file_name, "a", encoding="utf-8") as log_file:
            json.dump(log_data, log_file, ensure_ascii=False)
            log_file.write('\n')
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "You: " + message + "\n")
        chat_history.insert(tk.END, "Bot: " + response + "\n")
        chat_history.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)


def on_enter(event):
    send_message()


show_details = True
# Set up the Tkinter window
root = tk.Tk()
root.title("COM727 Chatbot")

# Create the chat history text area
chat_history = tk.Text(root, state=tk.DISABLED)
chat_history.pack(pady=15)

# Create the user input entry box
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=15)
message_entry.bind("<Return>", on_enter)  # Bind 'Enter' key to on_enter function

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=15)

# Start the Tkinter main loop
root.mainloop()

