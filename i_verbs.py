if __name__ == "__main__":
    # Ask the user for the filename
    filename = input("Please enter the filename for the verbs list (default is 'verbs.txt'): ").strip()
    if not filename:
        filename = "verbs.txt"

    try:
        verbs = load_verbs(filename)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        exit(1)

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
