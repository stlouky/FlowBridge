import csv
import os
import random
import difflib
from gtts import gTTS
import pandas as pd
from difflib import SequenceMatcher 
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
def generate_audio_file_if_not_exists(filename, text_to_speak, audio_dir='audio'):
    """
    Univerzální funkce, která vygeneruje audio soubor, pokud neexistuje.
    Nyní pracuje s celým názvem souboru.
    """
    # Ujistíme se, že název souboru končí na .mp3
    if not filename.endswith('.mp3'):
        filename += '.mp3'
        
    audio_path = os.path.join(audio_dir, filename)
    
    # Pokud soubor již existuje, nic neděláme
    if os.path.exists(audio_path):
        return True, "File already exists."
        
    try:
        # Vytvoříme adresář, pokud neexistuje
        os.makedirs(audio_dir, exist_ok=True)
        
        # Vygenerujeme audio
        tts = gTTS(text=text_to_speak, lang='en')
        tts.save(audio_path)
        return True, f"File {filename} created successfully."
    except Exception as e:
        print(f"Error generating audio file {filename}: {e}")
        return False, str(e)

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

def compare_answers(user_input, correct_answer):
    """
    Porovná dva texty a vrátí výsledek jako JEDEN HTML řetězec.
    Toto je opravená verze, která řeší problém '[object Object]'.
    """
    # Použijeme SequenceMatcher pro nalezení rozdílů
    matcher = SequenceMatcher(None, user_input.lower(), correct_answer.lower())
    
    html_parts = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Správná část, kterou uživatel napsal
            html_parts.append(f"<span class='diff-correct'>{correct_answer[j1:j2]}</span>")
        elif tag == 'replace':
            # Uživatel napsal něco jiného, než měl
            html_parts.append(f"<del class='diff-incorrect'>{user_input[i1:i2]}</del>")
            html_parts.append(f"<ins class='diff-missing'>{correct_answer[j1:j2]}</ins>")
        elif tag == 'delete':
            # Uživatel napsal něco navíc
            html_parts.append(f"<del class='diff-incorrect'>{user_input[i1:i2]}</del>")
        elif tag == 'insert':
            # Uživatel na něco zapomněl
            html_parts.append(f"<ins class='diff-missing'>{correct_answer[j1:j2]}</ins>")
            
    # Spojíme všechny části do jednoho finálního HTML stringu
    return "".join(html_parts)