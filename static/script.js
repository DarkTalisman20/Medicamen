// This script is responsible for handling the chat functionality on the client side.
document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatWindow = document.getElementById('chat-window');
    const resetChatButton = document.getElementById('resetChatButton');
    let awaitingNewConversationDecision = false; // State management

    // Function to display messages in the chat window
    function displayMessage(message, sender, isHTML = false) {
        const messageElement = document.createElement('div');
        // Check if the message should be interpreted as HTML
        if (isHTML) {
            messageElement.innerHTML = message; // Interpret as HTML
        } else {
            messageElement.textContent = message;
        }
        messageElement.className = sender;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom
    }

    // Function to reset the chat window
    function resetChat() {
        chatWindow.innerHTML = '';
        userInput.value = '';
        userInput.disabled = false; // Enable text box
        sendButton.disabled = false; // Enable send button
        displayMessage("Hello! I am your HealthCare chatbot Medicamen. How can I assist you today?", 'bot-message');
        awaitingNewConversationDecision = false; // Reset state
    }

    // Function to disable the chat window
    function disableChat() {
        userInput.value = '';
        userInput.disabled = true; 
        sendButton.disabled = true; 
    }

    // Function to handle the user's decision to start a new conversation
    function handleNewConversationDecision(decision) {
        displayMessage(decision, 'user-message'); // Display user's decision as a message
        // Check if the user wants to start a new conversation
        if (decision === 'yes') {
            resetChat();
        } else if (decision === 'no') {
            displayMessage("Thank you for chatting with me. I'm here whenever you need medical assistance. Stay healthy and take care!", 'bot-message');
            disableChat(); // Disable chat after thanking the user
        } else {
            // Handle invalid input
            userInput.value = '';
            displayMessage("Please respond with 'Yes' or 'No'.", 'bot-message');
            // Do not reset awaitingNewConversationDecision to keep the chat in decision mode
        }
        // Only reset the state if a valid decision ('yes' or 'no') was made
        if (decision === 'yes' || decision === 'no') {
            awaitingNewConversationDecision = false; // Reset state
        }
    }

    // Function to send the user's message to the server
    function sendMessage() {
        // Get the user's message and trim any whitespace
        const message = userInput.value.trim();
        // Check if the message is not empty
        if (message) {
            if (awaitingNewConversationDecision) {
                handleNewConversationDecision(message.toLowerCase());
                return; // Early return to avoid sending message when deciding on new conversation
            }
            displayMessage(message, 'user-message');
            userInput.value = '';
            // Disable the text box and send button while waiting for the response
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            })
            // Parsing the JSON response
            .then(response => response.json())
            .then(data => {
                const formattedResponse = data.response.replace(/\n/g, '<br>'); // Replacing newlines of json input with <br>
                displayMessage(formattedResponse, 'bot-message', true); // Rendering response as HTML
                if (!data.final_verdict) {
                    // If the conversation is not concluded, we wait for more input
                } else {
                    displayMessage("Do you want to start a new conversation? (Yes/No)", 'bot-message');
                    awaitingNewConversationDecision = true; // Setting state to true
                }
            });
        }
    }

    // Function to fetch the description from the server
    function fetchDescription() {
        fetch('data.json')
            .then(response => response.json())
            .then(data => {
                const description = data.description.replace(/\n/g, '<br>');
                displayMessage(description, 'bot-message', true); // Using true to render HTML
            })
            .catch(error => console.error('Error fetching the data:', error));
    }

    resetChat(); // Initializing chat on load
    sendButton.addEventListener('click', sendMessage);
    resetChatButton.addEventListener('click', resetChat);

    fetchDescription(); // Fetching and displaying the description on load
});
