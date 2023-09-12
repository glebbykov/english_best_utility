import random
import time

def load_verbs(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    verbs = [line.strip().split() for line in lines]
    return verbs

def display_progress_bar(percent):
    filled_length = int(50 * percent // 100)
    bar = "█" * filled_length + '-' * (50 - filled_length)
    print(f'\rProgress: |{bar}| {percent}% Correct', end='\r')

def update_record_file(time_elapsed):
    with open('records.txt', 'a', encoding='utf-8') as f:
        f.write(f"Time to 100%: {time_elapsed} seconds\n")

def quiz_user(verb_form_pair, errors):
    verb, form = verb_form_pair
    base, past, past_participle, russian_verb = verb
    
    english_form = ""
    if form == "base":
        english_form = base
    elif form == "past":
        english_form = past
    else:
        english_form = past_participle

    print(f"\n{form}\n{russian_verb}")
    user_input = input().strip()
    
    key = (russian_verb, form)
    
    if user_input == english_form:
        print("Correct!")
        return 1
    else:
        print(f"Incorrect!\n{english_form}")
        errors[key] = errors.get(key, 0) + 1
        return -2

if __name__ == "__main__":
    verbs = load_verbs("verbs.txt")
    forms = ["base", "past", "past participle"]
    
    verb_form_pairs = [(verb, form) for verb in verbs for form in forms]
    random.shuffle(verb_form_pairs)
    
    correct_percent = 0
    start_time = time.time()
    
    errors = {}
    total_questions = len(verb_form_pairs)

    print(f"Starting the quiz. Reach 100% to complete.")
    
    for idx, verb_form_pair in enumerate(verb_form_pairs):
        delta = quiz_user(verb_form_pair, errors)
        correct_percent += delta
        correct_percent = max(0, correct_percent)
        display_progress_bar(correct_percent)
        
        if correct_percent >= 100:
            break
    
    time_elapsed = time.time() - start_time
    minutes, seconds = divmod(time_elapsed, 60)
    
    print(f"\nTotal time to reach 100%: {int(minutes)} minutes {int(seconds)} seconds")
    update_record_file(time_elapsed)
    
    print("\nErrors by verb and form:")
    for key, value in errors.items():
        print(f"{key}: {value} errors")