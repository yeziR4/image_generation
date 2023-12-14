import requests
import io
from PIL import Image
import speech_recognition as sr
import time

# Hugging Face API for image generation
IMAGE_API_URL = "https://api-inference.huggingface.co/models/openskyml/dalle-3-xl"
IMAGE_HEADERS = {"Authorization": "Bearer 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"}

# Hugging Face API for speech recognition
SPEECH_API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
SPEECH_HEADERS = {"Authorization": "Bearer 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"}
recognizer = sr.Recognizer()

def query_image(payload):
    response = requests.post(IMAGE_API_URL, headers=IMAGE_HEADERS, json=payload)
    return response.content

def query_speech(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(SPEECH_API_URL, headers=SPEECH_HEADERS, data=data)
    return response.json()
def is_model_loading():
    response = requests.get(SPEECH_API_URL)
    return response.json().get('status', '') == 'loading'

def wait_for_model_loading():
    while is_model_loading():
        print("Waiting for the speech recognition model to finish loading...")
        time.sleep(20)



# ... (previous code)

def get_prompt():
    wait_for_model_loading()
    
    user_input = input("Choose input method ('text' or 'speech'): ").lower()

    if user_input == "text":
        return input("Enter a prompt for image generation: "), None
    elif user_input == "speech":
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Recording will start in 3 seconds. Get ready!")
            time.sleep(3)  # Give the user a moment to prepare
            print("Recording... Speak now!")

            try:
                audio = recognizer.listen(source, timeout=10)  # 10-second timeout
            except sr.WaitTimeoutError:
                print("Recording timed out after 10 seconds.")
                return "", None

        # Save the recorded audio to a file
        audio_file = "recorded_audio.flac"
        with open(audio_file, "wb") as f:
            f.write(audio.get_flac_data())

        # Use speech recognition to get the prompt
        speech_output = query_speech(audio_file)
        print("Speech Output:", speech_output)
        
        # Print the recognized text
        recognized_text_key = "text"
        recognized_text = speech_output.get(recognized_text_key, "")
        print("Recognized Text:", recognized_text)
        
        return recognized_text
    else:
        print("Invalid input method. Please choose 'text' or 'speech'.")
        return get_prompt()

# Get prompt input from the user
prompt = get_prompt()
# Query the image generation API with the prompt
image_bytes = query_image({"inputs": prompt})

# Open the image using PIL
image = Image.open(io.BytesIO(image_bytes))

# Save the image to a file
image.save("generated_image.jpg")

# Print additional information
print("Image mode:", image.mode)
print("Image size:", image.size)

# Display the image
image.show()


# Query the image generation API with the prompt

image_bytes = query_image({"inputs": prompt})

# Print the content of image_bytes for inspection
print("Image Bytes:", image_bytes)

# Open the image using PIL
image = Image.open(io.BytesIO(image_bytes))


# Open the image using PIL
image = Image.open(io.BytesIO(image_bytes))

# Save the image to a file
image.save("generated_image.jpg")

# Print additional information
print("Image mode:", image.mode)
print("Image size:", image.size)

# Display the image
image.show()










