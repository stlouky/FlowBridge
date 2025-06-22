import csv
import os
import random
import difflib
from gtts import gTTS
from flask import current_app

def load_phrases():
    """Načte všechny fráze z CSV souboru a vrátí je jako seznam slovníků."""
    file_path = os.path.join(current_app.root_path, '..', 'fraze.csv')
    phrases = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Důležité: Převedeme index na float pro matematické operace
                row['Index_Naučení'] = float(row['Index_Naučení'])
                phrases.append(row)
    except (FileNotFoundError, IOError) as e:
        print(f"CHYBA při čtení souboru {file_path}: {e}")
        return []
    return phrases

# --- NOVÁ FUNKCE ---
def save_phrases(phrases):
    """Uloží kompletní seznam frází (s aktualizovanými indexy) zpět do CSV."""
    file_path = os.path.join(current_app.root_path, '..', 'fraze.csv')
    fieldnames = ['ID_páru', 'Otázka_EN', 'Odpověď_EN', 'Nápověda_CZ', 'Index_Naučení']
    
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for phrase in phrases:
                # Vytvoříme si dočasnou kopii řádku pro bezpečný zápis
                row_to_write = phrase.copy()
                
                # Převedeme číselný index na hezky formátovaný text POUZE v této kopii
                row_to_write['Index_Naučení'] = f"{row_to_write['Index_Naučení']:.2f}"
                
                # Zapíšeme upravenou kopii, původní data v paměti zůstanou nedotčena
                writer.writerow(row_to_write)

    except IOError as e:
        print(f"CHYBA při zápisu do souboru {file_path}: {e}")
        
# --- NOVÁ FUNKCE ---
def generate_audio_file_if_not_exists(phrase_id, text):
    """
    Zkontroluje, jestli existuje audio soubor. Pokud ne, vygeneruje ho pomocí gTTS.
    """
    # Sestavíme cestu k audio souboru ve složce 'audio'
    # app.root_path je cesta ke složce 'app', takže musíme o úroveň výš
    audio_folder = os.path.join(current_app.root_path, '..', 'audio')
    audio_path = os.path.join(audio_folder, f"{phrase_id}.mp3")

    # Pokud soubor ještě neexistuje, vytvoříme ho
    if not os.path.exists(audio_path):
        try:
            print(f"Generuji audio pro frázi ID: {phrase_id}...")
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(audio_path)
            print(f"Audio uloženo: {audio_path}")
        except Exception as e:
            print(f"CHYBA při generování gTTS zvuku: {e}")
    
    return audio_path

# --- NOVÁ FUNKCE ---
def get_next_phrase(phrases):
    """
    Vybere další frázi k procvičení.
    Preferuje fráze s nejnižším Indexem Naučení.
    """
    # Odfiltrujeme fráze, které jsou již "naučené" (index >= 10)
    unlearned_phrases = [p for p in phrases if p.get('Index_Naučení', 0.0) < 10.0]
    
    if not unlearned_phrases:
        return None # Všechny fráze jsou naučené

    # Seřadíme je od nejnižšího indexu po nejvyšší
    unlearned_phrases.sort(key=lambda p: p.get('Index_Naučení', 0.0))
    
    # Vezmeme např. 5 nejslabších frází a z nich vybereme náhodně jednu,
    # aby se neopakovala stále dokola ta úplně nejslabší.
    lowest_five = unlearned_phrases[:5]
    return random.choice(lowest_five)

# --- NÁSLEDUJÍCÍ FUNKCE JIŽ ZNÁME, ZŮSTÁVAJÍ BEZE ZMĚNY ---

def mask_word(text, learning_index):
    # ... beze změny ...
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

def compare_answers(user_answer, correct_answer):
    # ... beze změny ...
    user_words = user_answer.split()
    correct_words = correct_answer.split()
    matcher = difflib.SequenceMatcher(None, user_words, correct_words)
    diff_result = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            diff_result.append({'tag': 'correct', 'text': ' '.join(user_words[i1:i2])})
        elif tag == 'replace':
            diff_result.append({'tag': 'incorrect', 'text': ' '.join(user_words[i1:i2])})
            missing_text = ' '.join(correct_words[j1:j2])
            diff_result.append({'tag': 'missing', 'text': f'[{missing_text}]'})
        elif tag == 'delete':
            diff_result.append({'tag': 'incorrect', 'text': ' '.join(user_words[i1:i2])})
        elif tag == 'insert':
            missing_text = ' '.join(correct_words[j1:j2])
            diff_result.append({'tag': 'missing', 'text': f'[{missing_text}]'})
    result_with_spaces = []
    for item in diff_result:
        result_with_spaces.append(item)
        result_with_spaces.append({'tag': 'space', 'text': ' '})
    return result_with_spaces[:-1]