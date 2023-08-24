import speech_recognition as sr


def recognize_speech(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {e}"


if __name__ == "__main__":
    wav_file_path = 'registered_voice/shubham2_QGKGGVA2DQUYkXAZ68dMcS/shubham2_QGKGGVA2DQUYkXAZ68dMcS.wav'
    recognized_text = recognize_speech(wav_file_path)
    print("Recognized text:", recognized_text)
