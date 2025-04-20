import speech_recognition as sr
import pyttsx3
import json
import os
from datetime import datetime

# Initialize components
recognizer = sr.Recognizer()
engine = pyttsx3.init()
memory_file = "assistant_memory.json"

# Load existing memory
def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            return json.load(f)
    return {"items": {}, "facts": {}}

# Save memory to file
def save_memory(data):
    with open(memory_file, 'w') as f:
        json.dump(data, f)

# Core functions
def remember_item(item, location):
    memory = load_memory()
    memory["items"][item.lower()] = location.lower()
    save_memory(memory)
    return f"I'll remember your {item} is in {location}"

def recall_item(item):
    memory = load_memory()
    item = item.lower()
    if item in memory["items"]:
        return f"Your {item} is in {memory['items'][item]}"
    return f"I don't remember where your {item} is"

def remember_fact(subject, fact):
    memory = load_memory()
    memory["facts"][subject.lower()] = fact.lower()
    save_memory(memory)
    return f"I'll remember that {subject} {fact}"

def recall_fact(subject):
    memory = load_memory()
    subject = subject.lower()
    if subject in memory["facts"]:
        return f"About {subject}: {memory['facts'][subject]}"
    return f"I don't know anything about {subject}"

# Conversation handler
def handle_conversation(text):
    memory = load_memory()
    text = text.lower()
    
    # Memory recall patterns
    if "remember that" in text:
        parts = text.split("remember that")[1].strip().split(" is ")
        if len(parts) == 2:
            return remember_fact(parts[0], parts[1])
    
    if "where is my" in text:
        item = text.split("where is my")[1].strip()
        return recall_item(item)
    
    if "my" in text and "is in" in text:
        parts = text.split("my")[1].split("is in")
        if len(parts) == 2:
            return remember_item(parts[0].strip(), parts[1].strip())
    
    # Add your existing command logic here
    # ...
    
    return "I'm not sure how to respond to that"

# Main loop
while True:
    try:
        with sr.Microphone() as mic:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic, timeout=5)
            
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            
            response = handle_conversation(text)
            print(f"Assistant: {response}")
            
            engine.say(response)
            engine.runAndWait()
            
    except sr.UnknownValueError:
        print("Assistant: I didn't catch that")
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break