# Speech-to-Text and NLP-based Command Processing System

This project implements a speech-to-text system that listens for user commands, converts speech into text, and processes it using Natural Language Processing (NLP). The system supports real-time speech recognition, text-to-speech output, and specific NLP-based commands like telling the time, weather, and saving transcribed text to a file.

## Features

- **Speech Recognition**: Records audio through the microphone and transcribes it into text using Google Web Speech API.
- **Natural Language Processing (NLP)**: Processes the transcribed text and responds to commands like checking the time, weather, and saving text to a file.
- **Text-to-Speech (TTS)**: Provides verbal responses to the user, using a queue system to manage speech tasks efficiently.
- **Real-time Interaction**: The system listens continuously and responds in real-time to commands, with an option to stop the recording manually.


## Setup

1. **Clone the Repository**:  
   Clone this project to your local machine using the following command:
   ```bash
   git clone Speech-to-text
   ```

2. **Install Dependencies**:  
   Install the required Python libraries using pip:
   ```bash
   pip install pyttsx3 SpeechRecognition spacy requests
   python -m spacy download en_core_web_sm
   ```

3. **Run the Program**:  
   After installing the dependencies, run the main script to start the application:
   ```bash
   python Speech-to-text.py
   ```

4. **Stop Recording**:  
   To stop the recording, simply type `stop recording` in the terminal.

## How It Works

- **Speech Recognition**: The system listens for audio input, processes it, and converts it into text.
- **NLP Command Processing**: The transcribed text is analyzed using the `spaCy` NLP model to identify commands and saving the output texts.
- **Text-to-Speech**: The system responds to the user with verbal feedback using the `pyttsx3` library.
