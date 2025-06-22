import csv
import os
import random  # <-- Nový import
from flask import current_app

def load_phrases():
    """Načte všechny fráze z CSV souboru a vrátí je jako seznam slovníků."""
    file_path = os.path.join(current_app.root_path, '..', 'fraze.csv')
    phrases = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                phrases.append(row)
    except FileNotFoundError:
        print(f"CHYBA: Soubor {file_path} nebyl nalezen.")
        return []
    return phrases

# --- NOVÁ FUNKCE ZAČÍNÁ ZDE ---
def mask_word(text, learning_index):
    """
    Zamaskuje text na základě Indexu Naučení.
    Počet skrytých písmen = celá část indexu.
    """
    level = int(float(learning_index))
    
    # Ignorujeme mezery, aby se nemaskovaly a nepočítaly do délky
    letters_only = [char for char in text if char != ' ']
    text_len = len(letters_only)
    
    # Pokud je level 0 nebo je text příliš krátký, nevracíme nic skrytého
    if level <= 0 or text_len == 0:
        return text

    # Určíme, kolik písmen skrýt, ale maximálně všechna
    num_to_hide = min(level, text_len)
    
    # Náhodně vybereme indexy písmen (ne mezer!), které skryjeme
    indices_in_letters_list_to_hide = random.sample(range(text_len), num_to_hide)
    
    # Převedeme text na seznam, abychom mohli měnit znaky
    masked_list = list(text)
    letter_idx = 0
    for i, char in enumerate(text):
        if char == ' ':
            continue
        if letter_idx in indices_in_letters_list_to_hide:
            masked_list[i] = '_'
        letter_idx += 1
        
    return "".join(masked_list)