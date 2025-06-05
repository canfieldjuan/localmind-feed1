import speech_recognition as sr

def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError as e:
        return f"Voice recognition error: {e}"