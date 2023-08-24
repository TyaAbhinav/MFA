import speech_recognition as sr
import Levenshtein


def get_transcription(file_path):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(file_path)
    with audio as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data)


def calculate_similarity_score(text1, text2):
    distance = Levenshtein.distance(text1, text2)
    max_length = max(len(text1), len(text2))
    similarity_score = 1.0 - distance / max_length
    return similarity_score


if __name__ == "__main__":
    file1_path = 'registered_voice/shubham2_QGKGGVA2DQUYkXAZ68dMcS/shubham2_QGKGGVA2DQUYkXAZ68dMcS.wav'
    file2_path = 'authentication_folder/sg_ZLMnAkFSszy2wfn5DTTTs7/sg_ZLMnAkFSszy2wfn5DTTTs7.wav'

    text1 = get_transcription(file1_path)
    text2 = get_transcription(file2_path)

    similarity_score = calculate_similarity_score(text1, text2)

    print(f"Similarity Score: {similarity_score:.2%}")
