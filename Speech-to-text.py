import pyttsx3
import threading
from queue import Queue
import speech_recognition as sr
import spacy
from datetime import datetime
import requests

# Load the NLP model for processing text
nlp = spacy.load("en_core_web_sm")

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()
stop_flag = False  # Flag to control stopping the recording
tts_queue = Queue()  # Queue for managing text-to-speech tasks
engine_busy = False  # Flag to indicate if engine is busy

def speak_text():
    """Consume text from the queue and speak it."""
    global engine_busy
    while True:
        text = tts_queue.get()
        if text is None:  # Break the loop if a None value is encountered
            break
        while engine_busy:
            continue  # Wait if the engine is busy
        engine_busy = True  # Set the engine as busy
        engine.say(text)
        engine.runAndWait()
        engine_busy = False  # Mark the engine as not busy
        tts_queue.task_done()

# Start the text-to-speech thread
tts_thread = threading.Thread(target=speak_text, daemon=True)
tts_thread.start()

def enqueue_speech(text):
    """Add text to the queue for speaking."""
    tts_queue.put(text)

def process_nlp_command(text):
    """Process the recognized text and respond based on NLP interpretation."""
    doc = nlp(text)
    if "time" in text.lower():
        now = datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {now}."
        enqueue_speech(response)
    elif "weather" in text.lower():
        # Example of a simple weather query (Replace with a valid API endpoint for actual data)
        response = "The weather is sunny today."
        enqueue_speech(response)
    elif "save" in text.lower():
        output_text(text)  # Save the recognized text to a file
        enqueue_speech("Text saved to file.")
    else:
        enqueue_speech("Sorry, I didn't understand the command.")

def record_text():
    """Record speech using the microphone and return the transcribed text."""
    global stop_flag
    try:
        with sr.Microphone() as source2:
            print("Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(source2, duration=3)
            enqueue_speech("I am ready. Please speak now.")
            print("Listening... (Type 'stop recording' to end)")

            while not stop_flag:
                try:
                    audio2 = r.listen(source2, timeout=5)  # Timeout to check the flag periodically
                    print("Processing your input...")
                    # Recognize speech using Google Web Speech API
                    MyText = r.recognize_google(audio2)
                    print(f"You said: {MyText}")
                    yield MyText  # Return recognized text dynamically
                except sr.WaitTimeoutError:
                    # Skip the timeout if no speech is detected
                    continue
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    enqueue_speech("Sorry, I couldn't understand. Please speak again.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    enqueue_speech("Sorry, I couldn't process your request.")
                    return
    except Exception as e:
        print(f"An error occurred: {e}")
        enqueue_speech("An error occurred while recording.")
        return

def output_text(text):
    """Save the recognized text to a file."""
    with open("output.txt", "a") as f:  # Use 'a' to append text to the file
        f.write(text)
        f.write("\n")
    print("Text saved to output.txt")

def listen_for_stop():
    """Monitor user input to stop the recording."""
    global stop_flag
    while not stop_flag:
        user_input = input()
        if user_input.lower() == "stop recording":
            stop_flag = True
            enqueue_speech("Stopping the recording. Goodbye!")
            print("Recording stopped by user input.")

# Start the keyboard listener in a separate thread
stop_thread = threading.Thread(target=listen_for_stop, daemon=True)
stop_thread.start()

# Main loop to handle continuous speech recognition
print("Activating microphone...")
try:
    for recognized_text in record_text():  # Get text dynamically from the generator
        if recognized_text:  # Only process non-empty text
            output_text(recognized_text)
            enqueue_speech(f"I recorded: {recognized_text}")
            process_nlp_command(recognized_text)  # Process text through NLP
except KeyboardInterrupt:
    print("Recording interrupted.")
    enqueue_speech("Recording interrupted.")
finally:
    # Signal the TTS thread to terminate and clean up
    tts_queue.put(None)
    tts_thread.join()
    print("Program has ended.")
