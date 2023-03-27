import speech_recognition as sr
import openai
from gtts import gTTS
import os

# Initialize OpenAI API credentials
openai.api_key = "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"

# Initialize the speech recognition engine
r = sr.Recognizer()

# Use microphone as audio source
with sr.Microphone() as source:
    print("Speak something...")
    # Adjust ambient noise for better recognition
    r.adjust_for_ambient_noise(source)
    # Listen for audio input
    audio = r.listen(source)

# Convert speech to text
try:
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand your audio.")
except sr.RequestError as e:
    print("Sorry, could not request results from speech recognition service; {0}".format(e))


# Define a function to capture the user's speech input
def get_audio():
    with sr.Microphone() as source:
        r = sr.Recognizer(source=source)
        audio = r.listen(source)
        try:
            audio_text = r.recognize_google(audio)
            print(f"You: {audio_text}")
            return audio_text
        except:
            error_message = "Sorry, I could not understand your audio please try again."
            print(f"Assistant: {error_message}")
            return error_message

# Define a function to generate a response to the user's query using OpenAI API
def generate_response(query):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt="what is Python?",
            max_tokens=50,
            n=1,
             sample_rate_hertz=16000,
            frequency_penalty=0.6,
            presence_penalty=0.6,
            stop="\n",
            temperature=0.5,
        )
        return response.choices[0].text
    except:
        error_message = "Sorry, I could not generate a response for your query."
        print(f"Assistant: {error_message}")
        return error_message

# Define a function to convert the response text into speech using gTTS
def speak(response):
    tts = gTTS(text=response, lang='en-US')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")
    

# Define the main loop to keep the conversation going
def main():
    conversation_history = ""
    while True:
        # Capture the user's speech input
        audio_text = get_audio()
        # Append the user's input to the conversation history
        conversation_history += "You: " + audio_text + "\n"
        # Generate a response to the user's query
        response_text = generate_response(conversation_history)
        # Append the response to the conversation history
        conversation_history += "Assistant: " + response_text + "\n"
        # Convert the response text into speech and read it back to the user
        speak(response_text)

