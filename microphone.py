import pickle
from read_audio import read_file
from models import generate_codebook
from collections import defaultdict
import pyaudio
import wave
import os
from typing import Tuple, Dict, Union

def microphone_integration(full_output_path: str) -> None:
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 40000
    CHUNK = 1024
    RECORD_SECONDS = 5

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    frames = []
     
    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(full_output_path, 'wb') as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(frames))

def write_file_for_microphone(attempt: int, unique_filename: str, output_directory: str) -> Tuple[Union[Dict, defaultdict], str]:
    f_name = f"{attempt + 1}_{unique_filename}"
    full_output_path = os.path.join(output_directory, f_name)
    microphone_integration(full_output_path)

    input_file_path = full_output_path
    input_data = read_file(input_file_path)
    codes, _, _ = generate_codebook(input_data, size_codebook=10, epsilon=0.00001)
    
    try:
        with open(f"{output_directory}Voicerecognition.pkl", "rb") as pkl:
            existing_data = pickle.load(pkl)
            existing_data[f_name] = codes
            return existing_data, output_directory
    except FileNotFoundError:
        new_data = {f_name: codes}
        return new_data, output_directory

def file_call_microphone(username: str) -> None:
    file_name = username
    unique_filename = f"{file_name}.wav"
    output_directory = f"registered_voice/{file_name}/"
    os.makedirs(output_directory, exist_ok=True)

    for attempt in range(3):
        data, output_dir = write_file_for_microphone(attempt, unique_filename, output_directory)
        with open(f"{output_dir}Voicerecognition.pkl", "wb") as pkl:
            pickle.dump(data, pkl)

def check_and_get_paths(username: str, base_dir: str) -> Tuple[list, bool]:
    user_folder = os.path.join(base_dir, username)

    if os.path.exists(user_folder) and os.path.isdir(user_folder):
        items = os.listdir(user_folder)
        item_paths = [os.path.join(user_folder, item) for item in items]
        return item_paths, True
    else:
        return [], False

def process_new_input_microphone(username: str) -> Tuple[str, str, str, str]:
    regis_directory = "registered_voice/"
    unique_filename = f"{username}.wav"
    regis_directory_with_file = f"registered_voice/{username}/"
    output_directory = f"authentication_folder/{username}/"

    os.makedirs(output_directory, exist_ok=True)
    full_output_path = os.path.join(output_directory, unique_filename)

    item_paths, username_status = check_and_get_paths(username, regis_directory)

    if username_status:
        microphone_integration(full_output_path)
    else:
        print("Username not valid.")
        return process_new_input_microphone(username)

    input_data = read_file(full_output_path)
    
    return username, input_data, regis_directory_with_file, full_output_path
