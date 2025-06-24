import os
import csv
import random
from gtts import gTTS
from difflib import SequenceMatcher
from flask import current_app

LESSONS_DIR = 'app/data/lessons'

def get_all_lessons():
    full_path = os.path.join(current_app.root_path, '..', LESSONS_DIR)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        return []
    lesson_files = [f for f in os.listdir(full_path) if f.endswith('.csv')]
    return sorted([os.path.splitext(f)[0] for f in lesson_files])

def get_lesson_path(lesson_name):
    return os.path.join(current_app.root_path, '..', LESSONS_DIR, f"{lesson_name}.csv")

def load_phrases(lesson_name):
    file_path = get_lesson_path(lesson_name)
    phrases = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['Index_Naučení'] = float(row.get('Index_Naučení', 0.0))
                phrases.append(row)
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"CHYBA při čtení souboru lekce {file_path}: {e}")
        return []
    return phrases

def save_phrases(lesson_name, phrases):
    file_path = get_lesson_path(lesson_name)
    if not phrases:
        return 
    
    fieldnames = phrases[0].keys()
    
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for phrase in phrases:
                row_to_write = phrase.copy()
                row_to_write['Index_Naučení'] = f"{row_to_write['Index_Naučení']:.2f}"
                writer.writerow(row_to_write)
    except IOError as e:
        print(f"CHYBA při zápisu do souboru lekce {file_path}: {e}")

def get_next_phrase(phrases):
    unlearned_phrases = [p for p in phrases if p.get('Index_Naučení', 0.0) < 10.0]
    if not unlearned_phrases:
        return None
    unlearned_phrases.sort(key=lambda p: p.get('Index_Naučení', 0.0))
    lowest_five = unlearned_phrases[:5]
    return random.choice(lowest_five)

def generate_audio_file_if_not_exists(filename, text_to_speak, audio_dir='audio'):
    if not filename.endswith('.mp3'):
        filename += '.mp3'
    full_audio_dir = os.path.join(current_app.root_path, '..', audio_dir)
    audio_path = os.path.join(full_audio_dir, filename)
    
    if os.path.exists(audio_path):
        return
    try:
        os.makedirs(full_audio_dir, exist_ok=True)
        tts = gTTS(text=text_to_speak, lang='en')
        tts.save(audio_path)
    except Exception as e:
        print(f"Error generating audio file {filename}: {e}")

def mask_word(text, learning_index):
    level = int(float(learning_index))
    letters_only = [char for char in text if char != ' ']
    text_len = len(letters_only)
    if level <= 0 or text_len == 0:
        return text
    num_to_hide = min(level, text_len)
    indices_in_letters_list_to_hide = random.sample(range(text_len), num_to_hide)
    masked_list = list(text)
    letter_idx = 0
    for i, char in enumerate(text):
        if char == ' ':
            continue
        if letter_idx in indices_in_letters_list_to_hide:
            masked_list[i] = '_'
        letter_idx += 1
    return "".join(masked_list)

def compare_answers(user_input, correct_answer):
    matcher = SequenceMatcher(None, user_input.lower(), correct_answer.lower())
    html_parts = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            html_parts.append(f"<span>{correct_answer[j1:j2]}</span>")
        elif tag == 'replace':
            html_parts.append(f"<del>{user_input[i1:i2]}</del>")
            html_parts.append(f"<ins>{correct_answer[j1:j2]}</ins>")
        elif tag == 'delete':
            html_parts.append(f"<del>{user_input[i1:i2]}</del>")
        elif tag == 'insert':
            html_parts.append(f"<ins>{correct_answer[j1:j2]}</ins>")
    return "".join(html_parts)