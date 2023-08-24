import os
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


def word_similarity(registered_voice_folder, auth_file_path):
    auth_text = get_transcription(auth_file_path)

    registered_files = []
    for folderpath, _, filenames in os.walk(registered_voice_folder):
        for filename in filenames:
            if filename.lower().endswith(".wav"):
                registered_files.append(os.path.join(folderpath, filename))

    best_match_score = 0
    best_match_file = None

    print("Scores:")

    for reg_file_path in registered_files:
        reg_text = get_transcription(reg_file_path)
        similarity_score = calculate_similarity_score(auth_text, reg_text)
        print(f"{reg_file_path}: {similarity_score:.2%}")

        if similarity_score > best_match_score:
            best_match_score = similarity_score
            best_match_file = reg_file_path
            best_match_text = reg_text

    print(f"\nBest Match File: {best_match_file} with Score: {best_match_score:.2%}")
    print(f"Provided audio text: {auth_text}")
    print(f"Best Match Text: {best_match_text}")
    if best_match_score >= 0.75:
        match_found = True
    else:
        match_found = False

    return match_found


if __name__ == "__main__":
    registered_voice_folder = "registered_voice"
    auth_file_path = 'authentication_folder/sg_ZLMnAkFSszy2wfn5DTTTs7/sg_ZLMnAkFSszy2wfn5DTTTs7.wav'
    auth_text = get_transcription(auth_file_path)

    registered_files = []
    for folderpath, _, filenames in os.walk(registered_voice_folder):
        for filename in filenames:
            if filename.lower().endswith(".wav"):
                registered_files.append(os.path.join(folderpath, filename))

    best_match_score = 0
    best_match_file = None

    print("Scores:")

    for reg_file_path in registered_files:
        reg_text = get_transcription(reg_file_path)
        similarity_score = calculate_similarity_score(auth_text, reg_text)
        print(f"{reg_file_path}: {similarity_score:.2%}")

        if similarity_score > best_match_score:
            best_match_score = similarity_score
            best_match_file = reg_file_path
            best_match_text = reg_text

    print(f"\nBest Match File: {best_match_file} with Score: {best_match_score:.2%}")
    print("Provided audio text:")
    print(auth_text)
    print("Best Match Text:")
    print(best_match_text)
