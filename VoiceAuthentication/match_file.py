import pickle
from VoiceAuthentication.models import matching

def matching_check_file(InputMFCC, regis_directory_with_file):
    with open(f"{regis_directory_with_file}Voicerecognition.pkl","rb") as pkl4:
        data=pickle.load(pkl4)
        mini=1800
        match_status = False
        for i in data:
            #print(InputMFCC.shape)
            print(i,matching(InputMFCC,data[i]),"FINALMATCHES")
            value=matching(InputMFCC,data[i])
            if value<=mini:
                match_status = True
                break
    return match_status