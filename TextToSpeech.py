from gtts import gTTS
import os

# Get the text to convert to speech from the user
text = input("Enter the text to convert to speech: ")
out = input("Enter the save file name with format: ")

# Create a gTTS object with the text
tts = gTTS(text)

# Save the audio file
tts.save(out)

# Play the audio file
os.system(out)
