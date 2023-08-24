import pickle
from VoiceAuthentication.read_audio import read_file
from VoiceAuthentication.models import generate_codebook
from collections import defaultdict
import pyaudio
import wave
import uuid
import shortuuid
import os


def microphone_integration(full_output_path):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 40000
    CHUNK = 1024
    RECORD_SECONDS = 2
    WAVE_OUTPUT_FILENAME = full_output_path
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    #print ("recording...")
    frames = []
     
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    #print ("finished recording")
 
 
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()



def write_file_for_microphone(attempt, unique_filename, output_directory):
    f_name = f"{attempt + 1}_{unique_filename}"
    full_output_path = os.path.join(output_directory, f_name)
    microphone_integration(full_output_path)
    Ip=full_output_path
    Input2=read_file(Ip)
    codes, codebook_abs_weights, codebook_rel_weights = generate_codebook(Input2, size_codebook=10, epsilon=0.00001)
    dictionary=defaultdict()

    try:
        with open(f"registered_voice/{unique_filename[:-4]}/Voicerecognition.pkl","rb") as pkl:
            #print("tryZEROTHITERATION")
            G=pickle.load(pkl)
            #print("TRYYYYYYYYYYYYY")
            #print(G,"\n\n\n")
            #print(type(G))
            G[f_name]=codes
            #print("FINAL TRYYYYYYYYYYYYYYY")
            return G, output_directory
    except:
        with open(f"registered_voice/{unique_filename[:-4]}/Voicerecognition.pkl","wb") as pkl:
            dictionary={}
            #print("EXCEPTTTTTTT")
            dictionary[f_name]=codes
            return dictionary, output_directory
#            pickle.dump(dictionary,pkl)


def file_call_microphone(username):
    #try:
    file_name = username
    #unique_id = str(shortuuid.uuid())
    #unique_filename = f"{file_name}_{unique_id}.wav"
    unique_filename  = f"{file_name}.wav"
    output_directory = f"registered_voice/{file_name}/"
    os.makedirs(output_directory, exist_ok=True)
    for attempt in range(3):
        G1, output_directory = write_file_for_microphone(attempt, unique_filename, output_directory)
        with open(f"{output_directory}Voicerecognition.pkl","wb") as pkl3:
            pickle.dump(G1,pkl3)
    
    #except:
    #    print("Exception occured.")


def check_and_get_paths(username, base_dir):
    user_folder = os.path.join(base_dir, username)

    if os.path.exists(user_folder) and os.path.isdir(user_folder):
        username_status = True
        items = os.listdir(user_folder)
        item_paths = [os.path.join(user_folder, item) for item in items]
        return item_paths, username_status
    else:
        item_paths = []
        username_status = False
        return item_paths, username_status


def process_new_input_microphone(username):
    Ip1=username
    file_name = Ip1
    regis_directory = f"registered_voice/"

    unique_filename = f"{file_name}.wav"
    regis_directory_with_file = f"registered_voice/{unique_filename[:-4]}/"
    output_directory = f"authentication_folder/{unique_filename[:-4]}/"
    os.makedirs(output_directory, exist_ok=True)
    full_output_path = os.path.join(output_directory, unique_filename[:-4])

    item_paths, username_status = check_and_get_paths(Ip1, regis_directory)
    if username_status:
        print("processing voice")
        microphone_integration(full_output_path)

    else:
        print("Username not valid.")
        process_new_input_microphone()



    Ip0=full_output_path
    Ip2=read_file(Ip0)
    
    return Ip1,Ip2,regis_directory_with_file, Ip0
