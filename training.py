import random
import json
import pickle
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
#from keras.layers import Conv1D, GlobalMaxPooling1D
#from keras.layers import LSTM
from keras.optimizers.legacy import SGD

# from tensorflow.keras.optimizer import SGD

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())

# Own addition 1. Lower case
for intent in intents["intents"]:
    intent["patterns"] = [pattern.lower() for pattern in intent["patterns"]]
# end of own  addition 1

# Own addition 2. Create a dictionary for words with underscore (readme.md)
def find_and_create_replacements(data, key_intents, key_patterns):
    replacements = {}
    for intent in data[key_intents]:
        # Iterate through the patterns in each intent
        for pattern in intent[key_patterns]:
            words = pattern.split()  # Split the pattern into words
            # Process the words in the pattern
            for word in words:
                # Check if the word contains underscores
                if '_' in word:
                    # Split the word into parts by underscores
                    parts = word.split('_')
                    replacements[f"{parts[0]} {parts[1]}"] = word
    return replacements


replacements = find_and_create_replacements(data=intents, key_intents='intents', key_patterns='patterns')
output_file = 'replacements.json'
# Save the replacements to the JSON file
with open(output_file, 'w') as file:
    json.dump(replacements, file, indent=4)
# end of Own addition 2

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', '/', '@']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        pos_tags = nltk.pos_tag(word_list)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

stop_words = set(stopwords.words('english'))
# Own addition 3. Lower case
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
# end of Own addition 3
words = sorted(set(words))

classes = sorted(set(classes))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
#model.add(Conv1D(128, 5, activation='relu', input_shape=(len(train_x[0]), 1)))
#model.add(GlobalMaxPooling1D())
#model.add(LSTM(128, input_shape=(len(train_x[0]), 1), activation='relu'))

model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
# model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.keras', hist)
print('Done')

