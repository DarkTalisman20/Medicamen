import random
import json
import pickle
import nltk
nltk.download('all')
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

import numpy as np
from sklearn.model_selection import train_test_split

lemmatizer = WordNetLemmatizer()

# Load the intents file 
intents = json.loads(open("intents.json").read())

words = []
classes = []
documents = []

ignore_letters = ["?", "!", ".", ","]

# Adjusting the data to fit the model
for intent in intents["intents"]:
    for pattern in intent["keywords"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["disease"]))

        if intent["disease"] not in classes:
            classes.append(intent["disease"])

# Lemmatizing, lowering each word and remove duplicates
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# Saving the words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Creating the training data
input_vectors = []
output_vectors = []
template = [0] * len(classes)

for idx, (pattern_words, label) in enumerate(documents):
    bag = []
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    for w in words:
        bag.append(1 if w in pattern_words else 0)
    output_row = list(template)
    output_row[classes.index(label)] = 1
    
    input_vectors.append(np.array(bag))
    output_vectors.append(np.array(output_row))

# Converting lists of arrays to a single NumPy array
input_vectors = np.array(input_vectors)
output_vectors = np.array(output_vectors)

# Splitting and testing data
X_train, X_test, y_train, y_test = train_test_split(input_vectors, output_vectors, test_size=0.2)
model = Sequential()
model.add(Dense(256, input_shape=(len(X_train[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

# Compiling the model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Training and saving the model
hist = model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)
model.save("chatbot_model.h5")
print("Done!")