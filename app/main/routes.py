# app/main/routes.py

import os
from difflib import SequenceMatcher
from flask import (
    render_template, jsonify, request,
    send_from_directory, current_app, Blueprint
)
from app.services import (
    load_phrases, mask_word, compare_answers,
    save_phrases, get_next_phrase, generate_audio_file_if_not_exists
)

bp = Blueprint('main', __name__)

# --- Konfigurace modelu ---
TARGET_CPS, REACTION_BONUS = 1.67, 2.0
CORRECTNESS_WEIGHT, TIME_WEIGHT = 0.8, 0.2
OLD_INDEX_WEIGHT, SCORE_WEIGHT = 0.7, 0.3

def prepare_phrase_data(phrase_obj):
    """
    Pomocná funkce, která k frázi přidá URL k audiím a zajistí jejich existenci.
    """
    if not phrase_obj:
        return None
    
    # Zajistíme existenci obou audio souborů s konvencí _Q a _A
    generate_audio_file_if_not_exists(f"{phrase_obj['ID_páru']}_Q.mp3", phrase_obj['Otázka_EN'])
    generate_audio_file_if_not_exists(f"{phrase_obj['ID_páru']}_A.mp3", phrase_obj['Odpověď_EN'])
    
    # Přidáme URL přímo do objektu, aby je šablona a JS mohly použít
    phrase_obj['question_audio_url'] = f"/audio/{phrase_obj['ID_páru']}_Q.mp3"
    phrase_obj['answer_audio_url'] = f"/audio/{phrase_obj['ID_páru']}_A.mp3"
    
    return phrase_obj

@bp.route('/')
def index():
    """Načte stránku a připraví první frázi."""
    all_phrases = load_phrases()
    current_phrase = get_next_phrase(all_phrases)
    prepared_phrase = prepare_phrase_data(current_phrase)
    
    masked_answer = ""
    if prepared_phrase:
        masked_answer = mask_word(prepared_phrase['Odpověď_EN'], prepared_phrase['Index_Naučení'])

    return render_template('index.html', phrase=prepared_phrase, masked_answer=masked_answer)

@bp.route('/check_answer', methods=['POST'])
def check_answer_route():
    """Zpracuje odpověď a vrátí další připravenou frázi."""
    data = request.get_json()
    user_answer = data.get('user_answer', '').strip()
    phrase_id = data.get('phrase_id')
    time_elapsed = float(data.get('time_elapsed', -1.0))
    
    all_phrases = load_phrases()
    phrase_to_check = next((p for p in all_phrases if str(p['ID_páru']) == str(phrase_id)), None)

    if not phrase_to_check:
        return jsonify({'error': 'Fráze nenalezena'}), 404

    # --- Blok pro výpočet indexu (beze změny) ---
    correct_answer = phrase_to_check['Odpověď_EN'].strip()
    diff_result = compare_answers(user_answer, correct_answer)
    correctness_ratio = SequenceMatcher(None, user_answer.lower(), correct_answer.lower()).ratio()
    if time_elapsed < 0:
        time_factor = 0.0
    else:
        phrase_len = len(correct_answer)
        max_time = (phrase_len / TARGET_CPS) + REACTION_BONUS
        time_factor = max(0.0, min(1.0, 1 - (time_elapsed / max_time)))
    current_score = (correctness_ratio * CORRECTNESS_WEIGHT) + (time_factor * TIME_WEIGHT)
    old_index = phrase_to_check['Index_Naučení']
    new_index = (old_index * OLD_INDEX_WEIGHT) + (current_score * 10 * SCORE_WEIGHT)
    phrase_to_check['Index_Naučení'] = round(max(0.0, min(10.0, new_index)), 2)
    
    save_phrases(all_phrases)
    
    # Připravíme kompletní data pro PŘÍŠTÍ frázi
    next_phrase_obj = get_next_phrase(all_phrases)
    prepared_next_phrase = prepare_phrase_data(next_phrase_obj)
    
    next_masked_answer = ""
    if prepared_next_phrase:
        next_masked_answer = mask_word(prepared_next_phrase['Odpověď_EN'], prepared_next_phrase['Index_Naučení'])
    
    return jsonify({
        'feedback': {'diff': diff_result},
        # Pošleme kompletní objekt příští fráze i s audio URL
        'next_phrase': prepared_next_phrase, 
        'next_masked_answer': next_masked_answer,
    })

@bp.route('/audio/<filename>')
def get_audio(filename):
    """Servíruje audio soubory."""
    audio_dir = os.path.join(current_app.root_path, '..', 'audio')
    return send_from_directory(audio_dir, filename)

