
# Medicamen

Medicamen is a chatbot that can predict the disease based on the symptoms of the patient and give suggestions to the ease out the symptoms. 

## Disclaimer

It's very important to remember that the suggestions may not be able to cure the diseases and it's always important to get check-up with a certified medical officer. Suggestions give by the chatbot are only to help the patient with the symptoms at the spur of the moment.


## Acknowlegments
I have taken help from websites of a few government organizations for training our Chatbot model.

The links for the websites are as follows - 

1)https://www.who.int/

2)https://www.ninds.nih.gov/

3)https://www.ncbi.nlm.nih.gov/

## Setting up and Testing

### 1) Downloading the code


    On your terminal type the following command - 

    
        git clone https://github.com/DarkTalisman20/Medicamen.git
    


### 2) Downloading the requirements


    
        cd Medicamen/
        pip3 install -r requirements.txt
    


If you have python installed on your system instead of python3 then you can use 



    pip install -r requirements.txt


instead of pip3.

### 3) Training the chatbot model 



    python trainer.py


or 


    python3 trainer.py


### 4) Running the application  



    python app.py



or 


    python3 app.py


### 5) Opening the Chatbot on browser 

    type  http://localhost:5000/ 
    
    on you browser to see the application up and running.

## Code Overview

### Knowledge Base -
I have collected around 20-25 diseases very common diseases.
The websites were consulted to extract the common symptoms for diseases along with some suggestions to prevent diseases 
and keep the symptoms under control. This information has been kept together in the "intents.json" file.

### Training of the model - 
'trainer.py' implements the nltk module to convert the keywords(i.e the symptoms) to their root words. Using TensorFlow and Keras, I have prepared a linear stack of neural network layers. After connection of the layers and optimisation using SGD(Stochastic Gradient Descent) taking categorical crossentropy for observation of the losses.
Finally the model is splitted and trained with the help of the Scikit-Learn module. 

### Prediction of disease - 
'app.py' is the server-side handler of the chatbot that uses natural language processing techniques and a pre-trained neural network model to interpret user inputs and predict possible diseases.

### Response Handler - 
'script.js' is the response handler of the chatbot which takes in the user's response, passes it to the 'app.py' and fetches the predictions according to which it gives the visible response to the user through the 'index.html' and 'style.css'. It also takes care of the overall dialogue flow of the conversation along with exception handling.

### User Interface - 
'index.html' and 'style.css' together create a platform through which the user can interact with the disease predictor via 'script.js'


## Conlusion
Medicamen offers accurate medical assistance to users and aims to be a valuable resource for everyone. Your feedback is crucial for refining and improving the chatbot. Thank You.



