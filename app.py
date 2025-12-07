from flask import Flask, render_template, jsonify, request
import pyttsx3
import webbrowser
import subprocess
import datetime
import random
import threading
import time

app = Flask(__name__)

# Initialize TTS engine with error handling
def get_tts_engine():
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        if engine.getProperty('voices'):
            engine.setProperty('voice', engine.getProperty('voices')[1].id)
        return engine
    except Exception as e:
        print(f"Failed to initialize TTS: {e}")
        return None

# Global engine with lock for thread safety
engine_lock = threading.Lock()
engine = get_tts_engine()

# Command and conversation handling
COMMAND_RESPONSES = {
    "open chrome": ("Opening Google Chrome", lambda: webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome.exe %s').open('https://www.google.com')),
    "open settings": ("Opening Settings", lambda: subprocess.run('start ms-settings:', shell=True)),
    "time": (lambda: f"It's {datetime.datetime.now().strftime('%I:%M %p')}", None),
    "date": (lambda: f"Today is {datetime.date.today().strftime('%B %d, %Y')}", None)
}

CONVERSATION_RESPONSES = {
    "greeting": ["Hello!", "Hi there!", "Greetings!"],
    "farewell": ["Goodbye!", "See you later!"],
    "how_are_you": ["I'm doing well!", "All systems operational!", "Great, thanks for asking!"],
    "default": "I can open apps or tell you the time/date."
}

def get_response(text):
    text = text.lower().strip()
    
    # Check commands
    for cmd, (response, action) in COMMAND_RESPONSES.items():
        if cmd in text:
            if action:
                threading.Thread(target=action).start()
            return response() if callable(response) else response
    
    # Handle conversation
    if any(word in text for word in ["hello", "hi", "hey"]):
        return random.choice(CONVERSATION_RESPONSES["greeting"])
    elif any(word in text for word in ["bye", "goodbye"]):
        return random.choice(CONVERSATION_RESPONSES["farewell"])
    elif "how are you" in text:
        return random.choice(CONVERSATION_RESPONSES["how_are_you"])
    
    return CONVERSATION_RESPONSES["default"]

def safe_speak(text):
    print(f"Assistant: {text}")
    if engine:
        with engine_lock:
            try:
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
    else:
        print("(TTS not available)")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.json.get('text', '')
    try:
        response = get_response(text)
        safe_speak(response)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': "Sorry, I encountered an error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
