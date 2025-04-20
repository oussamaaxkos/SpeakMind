document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const sendBtn = document.getElementById('sendBtn');
    const textInput = document.getElementById('textInput');
    const statusDiv = document.getElementById('status');
    const conversationDiv = document.getElementById('conversation');
    
    let recognition;
    let isListening = false;
    
    // Check for browser support
    if (!('webkitSpeechRecognition' in window)) {
        statusDiv.textContent = "Speech recognition not supported in this browser";
        startBtn.disabled = true;
    }
    
    // Initialize speech recognition if supported
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isListening = true;
            statusDiv.textContent = "Listening...";
            startBtn.disabled = true;
            stopBtn.disabled = false;
        };
        
        recognition.onend = function() {
            if (isListening) {
                recognition.start();
            }
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[event.results.length - 1][0].transcript;
            addMessage('user', transcript);
            processCommand(transcript);
        };
        
        recognition.onerror = function(event) {
            statusDiv.textContent = "Error: " + event.error;
            stopListening();
        };
    }
    
    // Button event listeners
    startBtn.addEventListener('click', startListening);
    stopBtn.addEventListener('click', stopListening);
    sendBtn.addEventListener('click', sendTextCommand);
    textInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendTextCommand();
        }
    });
    
    function startListening() {
        if (recognition) {
            try {
                recognition.start();
            } catch (e) {
                statusDiv.textContent = "Error starting recognition: " + e.message;
            }
        } else {
            statusDiv.textContent = "Speech recognition not available";
        }
    }
    
    function stopListening() {
        isListening = false;
        if (recognition) {
            recognition.stop();
        }
        statusDiv.textContent = "Ready";
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
    
    function sendTextCommand() {
        const command = textInput.value.trim();
        if (command) {
            addMessage('user', command);
            textInput.value = '';
            processCommand(command);
        }
    }
    
    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender + '-message';
        messageDiv.textContent = (sender === 'user' ? 'You: ' : 'Assistant: ') + text;
        conversationDiv.appendChild(messageDiv);
        conversationDiv.scrollTop = conversationDiv.scrollHeight;
    }
    
    function processCommand(command) {
        fetch('/process_command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: command })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('assistant', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('assistant', "Sorry, I encountered an error processing your request");
        });
    }
    
    // Initial greeting
    addMessage('assistant', 'Assistant activated. How can I help you today?');
});