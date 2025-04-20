import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import datetime
import random

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure voice properties
engine.setProperty('rate', 180)  # Speed of speech
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for different voices

# Command Functions
def open_settings():
    subprocess.run('start ms-settings:', shell=True)
    speak("Opening Settings")

def open_chrome():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open('https://www.google.com')
    speak("Opening Google Chrome")

def open_website(url, name):
    webbrowser.open(url)
    speak(f"Opening {name}")

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def get_date(): 
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today is {today}")

# Conversation Responses
greetings = ["Hi there!", "Hello!", "Nice to hear you!", "Greetings!"]
morning_responses = [
    "Good morning! How are you today?",
    "Morning sunshine! Ready for the day?",
    "Top of the morning to you!"
]
farewells = ["Goodbye!", "See you later!", "Have a great day!"]

# Main Loop
speak("Assistant activated. How can I help you today?")
while True:
    try:
        with sr.Microphone() as mic:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic, timeout=5)
            
            text = recognizer.recognize_google(audio).lower()
            print(f"You: {text}")
            
            # Command Handling
            if "open google chrome" in text:
                open_chrome()
                
            elif "open settings" in text:
                open_settings()
                
            elif "open youtube" in text:
                open_website("https://youtube.com", "YouTube")
                
            elif "open facebook" in text:
                open_website("https://facebook.com", "Facebook")
                
            elif "what time is it" in text or "current time" in text:
                get_time()
                
            elif "what's today's date" in text or "current date" in text:
                get_date()
                
            # Conversation Handling
            elif any(greeting in text for greeting in ["hi", "hello", "hey"]):
                speak(random.choice(greetings))
                
            elif "good morning" in text:
                speak(random.choice(morning_responses))
                
            elif any(farewell in text for farewell in ["bye", "goodbye", "see you"]):
                speak(random.choice(farewells))
                break
                
            elif "how are you" in text:
                speak("I'm doing great! How about you?")
                
            elif "your name" in text:
                speak("I'm your personal voice assistant!")
                
            else:
                speak("I didn't understand that command. Can you repeat please?")
                
    except sr.UnknownValueError:
        speak("I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        speak("Sorry, I'm having trouble with the speech service")
    except sr.WaitTimeoutError:
        speak("I didn't hear anything. Are you still there?")
    except KeyboardInterrupt:
        speak("Goodbye!")
        break