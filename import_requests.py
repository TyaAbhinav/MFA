import requests
from itertools import permutations
from collections import defaultdict
from app import Question

base_url = "http://127.0.0.1:5000"
username_to_test = "tabhi2506"

def get_random_questions():
    try:
        headers = {"Accept": "application/json"}
        response = requests.post(f"{base_url}/login", data={"username": username_to_test}, headers=headers)
        response.raise_for_status()  # Will raise an exception for 4xx and 5xx responses
        return [q['text'] for q in response.json()['random_questions']]
    except Exception as e:
        print(f"Failed to get questions. Error: {e}")
        return []

# 1. Frequency Test
frequency = defaultdict(int)
for _ in range(1000):
    questions_asked = get_random_questions()
    for question in questions_asked:
        frequency[question] += 1

for question, freq in frequency.items():
    print(f"Question: {question}, Frequency: {freq}")

# 2. Runs Test
prev_set = set()
runs = 0
for _ in range(1000):
    current_set = set(get_random_questions())
    if prev_set != current_set:
        runs += 1
    prev_set = current_set

print(f"Number of runs: {runs}")

# 3. Permutation Test
try:
    response = requests.get(f"{base_url}/get_all_questions")
    all_possible_questions = response.json()['questions']

    perms = list(permutations(all_possible_questions, 3))
    perm_freq = defaultdict(int)
    for _ in range(1000):
        questions_asked = tuple(get_random_questions())
        perm_freq[questions_asked] += 1

    for p, freq in perm_freq.items():
        print(f"Permutation: {p}, Frequency: {freq}")

except Exception as e:
    print(f"Failed to get questions. Error: {e}")


