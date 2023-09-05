from microphone import process_new_input_microphone
from match_file import matching_check_file
from similarity_score_all import word_similarity
from typing import Optional

def voice_authentication(user: str) -> Optional[int]:
    def try_authentication(user: str) -> bool:
        """
        A helper function to try voice authentication once.
        """
        (input_name, input_mfcc, regis_directory_with_file, auth_directory_file_path) = process_new_input_microphone(user)
        match_status = matching_check_file(input_mfcc, regis_directory_with_file)
        
        if match_status:
            print("checking words")
            word_match_found = word_similarity(regis_directory_with_file, auth_directory_file_path)
            return word_match_found
        return False
    
    # First attempt
    if try_authentication(user):
        print("Login Successful......")
        return 1

    print("Try again.")

    # Second attempt
    if try_authentication(user):
        print("Login Successful......")
        return 1

    print("No more attempts available.")
    return None  # Returning None to indicate no more attempts


