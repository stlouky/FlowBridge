# app/main/routes.py - FINÁLNÍ OPRAVENÁ VERZE

# Zde jsou všechny potřebné importy z Flasku, včetně chybějícího 'Blueprint'
from flask import render_template, jsonify, request, send_from_directory, current_app, Blueprint
import os
# Zde jsou všechny potřebné importy z našich služeb
from app.services import load_phrases, mask_word, compare_answers, save_phrases, get_next_phrase, generate_audio_file_if_not_exists


# Tuto definici jsme přesunuli sem z app/main/__init__.py, aby byla na jednom místě s routami, které ji používají.
# Je to čistší řešení.
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    all_phrases = load_phrases()
    # Použijeme naši novou chytrou funkci pro výběr první fráze
    current_phrase = get_next_phrase(all_phrases)
    
    masked_answer = ""
    if current_phrase:
        masked_answer = mask_word(
            current_phrase['Odpověď_EN'], 
            current_phrase['Index_Naučení']
        )

    return render_template('index.html', phrase=current_phrase, masked_answer=masked_answer)

@bp.route('/check_answer', methods=['POST'])
def check_answer_route():
    data = request.get_json()
    user_answer = data.get('user_answer', '').strip()
    phrase_id = data.get('phrase_id')

    # 1. Načteme VŠECHNY fráze
    all_phrases = load_phrases()
    phrase_to_check = next((p for p in all_phrases if p['ID_páru'] == phrase_id), None)

    if not phrase_to_check:
        return jsonify({'error': 'Fráze nenalezena'}), 404

    # 2. Zjistíme správnost a vytvoříme "diff" pro zobrazení
    correct_answer = phrase_to_check['Odpověď_EN'].strip()
    is_perfectly_correct = user_answer.lower() == correct_answer.lower()
    diff_result = compare_answers(user_answer, correct_answer)

    # 3. Aktualizujeme Index Naučení
    current_index = phrase_to_check['Index_Naučení']
    if is_perfectly_correct:
        # Za správnou odpověď přičteme 1 bod
        phrase_to_check['Index_Naučení'] = min(current_index + 1, 10.0)
    else:
        # Za špatnou odpověď snížíme index na polovinu, ale ne pod nulu.
        phrase_to_check['Index_Naučení'] = max(current_index / 2, 0.0)

    # 4. Uložíme VŠECHNY fráze (i s naší jednou změnou) zpět do CSV
    save_phrases(all_phrases)

    # 5. Vybereme další frázi pro příští kolo
    next_phrase_obj = get_next_phrase(all_phrases)
    
    next_masked_answer = ""
    if next_phrase_obj:
        next_masked_answer = mask_word(
            next_phrase_obj['Odpověď_EN'],
            next_phrase_obj['Index_Naučení']
        )
    
    # 6. Pošleme vše potřebné zpět do prohlížeče
    return jsonify({
        'feedback': {
            'is_perfectly_correct': is_perfectly_correct,
            'diff': diff_result
        },
        'next_phrase': next_phrase_obj,
        'next_masked_answer': next_masked_answer
    })

@bp.route('/audio/<filename>')
def get_audio(filename):
    """
    Servíruje audio soubor. Pokud neexistuje, pokusí se ho nejprve vygenerovat.
    """
    # Získáme ID fráze z názvu souboru (např. "1.mp3" -> "1")
    phrase_id = os.path.splitext(filename)[0]
    
    # Najdeme text otázky pro dané ID
    phrases = load_phrases()
    phrase_obj = next((p for p in phrases if p['ID_páru'] == phrase_id), None)
    
    if phrase_obj:
        # Zavoláme naši servisní funkci, která zvuk vygeneruje, pokud je potřeba
        generate_audio_file_if_not_exists(phrase_id, phrase_obj['Otázka_EN'])
    
    # Pošleme soubor z našeho adresáře 'audio' do prohlížeče
    audio_dir = os.path.join(current_app.root_path, '..', 'audio')
    return send_from_directory(audio_dir, filename)