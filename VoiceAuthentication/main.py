from VoiceAuthentication.microphone import process_new_input_microphone
from VoiceAuthentication.match_file import matching_check_file
from VoiceAuthentication.similarity_score_all import word_similarity

def voice_authentication(user):

    (Inputname,InputMFCC,
        regis_directory_with_file,auth_directory_file_path) = process_new_input_microphone(user)
    match_status=matching_check_file(InputMFCC, regis_directory_with_file)
    #print("checking words")
    #word_match_found = word_similarity(regis_directory_with_file, auth_directory_file_path)
    if match_status:
        print("checking words")
        word_match_found = word_similarity(regis_directory_with_file, auth_directory_file_path)
        if word_match_found:
            print("Login Successful......")
            status = "successful"
            return status
        else:
            print("Login FAILED......")
    else:
        print("try again")
        (Inputname, InputMFCC,
            regis_directory_with_file, auth_directory_file_path) = process_new_input_microphone(user)
        match_status = matching_check_file(InputMFCC, regis_directory_with_file)
        if match_status:
            print("checking words")
            word_match_found = word_similarity(regis_directory_with_file, auth_directory_file_path)
            if word_match_found:
                print("Login Successful......")
                status = "successful"
                return status
            else:
                print("Login FAILED......")
        else:
            print("No more attempts available")
