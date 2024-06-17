from flask import Flask, request, jsonify, render_template
import os
# Suppressing TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import json
import pickle
import numpy as np
from tensorflow.keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

app = Flask(__name__)
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Loading the intents file and the model along with the words and classes
lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

# Get the set of English stopwords
stop_words = set(stopwords.words('english'))

# Functions to clean up the sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    # Filter out stopwords from the tokenized words
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words if word.lower() not in stop_words]
    return sentence_words

# Function to create a bag of words from the sentence
def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

# Function to predict the class of the sentence
def predict_class(sentence, model=model, words=words):
    bow = bag_of_words(sentence, words)
    # Reshaping the bag of words to fit the model
    res = model.predict(np.array([bow]))[0]
    # Setting a threshold for the error
    ERROR_THRESHOLD = 0.2
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    # Returning the intent/intents with the highest probability
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Function to get the response
def get_response(intents_list, intents_json):
    response = {"message": "", "final_verdict": False}
    relevant_intents = [intent for intent in intents_list if float(intent['probability']) > 0.2]
    # If there are multiple intents with a probability greater than 0.3, ask for more details
    if len(relevant_intents) > 1:
        response["message"] = "Your symptoms are common to multiple diseases. Could you provide more details?"
    # If there is only one intent with a probability greater than 0.3, provide the disease information
    elif len(relevant_intents) == 0:
        response["message"] = "I'm sorry, but I couldn't find any diseases that match your symptoms. Could you provide more details?"
    # If there is only one intent with a probability greater than 0.3, provide the disease information
    else:
        tag = relevant_intents[0]['intent']
        for i in intents_json['intents']:
            # If the intent matches the tag, we provide the disease information
            if i['disease'] == tag:
                description = ' '.join(i['description']) if isinstance(i['description'], list) else i['description']
                response["message"] = f"You might have {i['disease']}.\n{description}"
                response["final_verdict"] = True
                break
        # If the intent does not match any disease, ask for more details
        if not response["final_verdict"]:
            response["message"] = "I'm sorry, but I couldn't find any diseases that match your symptoms. Could you provide more details?"
    return response

# API endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Get the message from the request
    data = request.get_json(force=True)
    message = data['message']
    print(f"Received message: {message}")
    ints = predict_class(message)
    for intent in ints:
        # Print the predicted disease and its probability on console for debugging
        print(f"Predicted disease: {intent['intent']}, Probability: {intent['probability']}")
    res = get_response(ints, intents)
    return jsonify({"response": res['message'], "final_verdict": res['final_verdict']})

@app.route('/')
def home():
    # Render the home page
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)