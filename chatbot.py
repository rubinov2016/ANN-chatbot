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
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
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
    except IndexError:
        result = "I don't know"
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


while True:
    ints =[]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = input("You: ")
    #Ivan addition 4
    message = message.lower()
    if message == 'exit':
        break
    num_words = len(message.split())
    if num_words >= 2 or message in ["hello", "hi", "hey"]:
        message = replace_words(message, replacements)
        ints = predict_class(message)
        res = get_response(ints, intents)
        res = res + "          " + json.dumps(ints)
        # print(ints)
        # print(intents)
    else:
        res = "Your question is too short, can you restate it?"
    log_data = {
        "timestamp": timestamp,
        "input_message": message,
        "output_response": res
    }
    with open(file_name, "a", encoding="utf-8") as log_file:
        json.dump(log_data, log_file, ensure_ascii=False)
        log_file.write('\n')  # Add a newline to separate entries
    #end of  Ivan addition 4
    print(res)