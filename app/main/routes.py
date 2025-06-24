import os
from difflib import SequenceMatcher 

import json
from flask import (
    render_template, jsonify, request,
    send_from_directory, current_app, Blueprint,
    session, redirect, url_for
)
from app.services import (
    get_all_lessons, load_phrases, save_phrases, get_next_phrase,
    mask_word, compare_answers, generate_audio_file_if_not_exists,
    SequenceMatcher
)

bp = Blueprint('main', __name__)

TARGET_CPS, REACTION_BONUS = 1.67, 2.0
CORRECTNESS_WEIGHT, TIME_WEIGHT = 0.8, 0.2
OLD_INDEX_WEIGHT, SCORE_WEIGHT = 0.7, 0.3

def prepare_phrase_data(phrase_obj):
    if not phrase_obj:
        return None
    
    generate_audio_file_if_not_exists(f"{phrase_obj['ID_páru']}_Q.mp3", phrase_obj['Otázka_EN'])
    generate_audio_file_if_not_exists(f"{phrase_obj['ID_páru']}_A.mp3", phrase_obj['Odpověď_EN'])
    
    phrase_obj['question_audio_url'] = f"/audio/{phrase_obj['ID_páru']}_Q.mp3"
    phrase_obj['answer_audio_url'] = f"/audio/{phrase_obj['ID_páru']}_A.mp3"
    
    return phrase_obj

@bp.route('/')
def index():
    active_lesson = session.get('active_lesson')
    if not active_lesson:
        return redirect(url_for('main.manage_lessons'))

    phrases = load_phrases(active_lesson)
    current_phrase = get_next_phrase(phrases)
    
    if not current_phrase:
         return render_template('index.html', phrase=None, lesson_name=active_lesson.replace('_', ' '))

    prepared_phrase = prepare_phrase_data(current_phrase)

    masked_answer = ""
    if prepared_phrase:
        masked_answer = mask_word(prepared_phrase['Odpověď_EN'], prepared_phrase['Index_Naučení'])

    return render_template(
        'index.html', 
        phrase=prepared_phrase, 
        masked_answer=masked_answer, 
        lesson_name=active_lesson.replace('_', ' '),
        initial_phrase_data=json.dumps(prepared_phrase)
    )

@bp.route('/lekce')
def manage_lessons():
    lessons = get_all_lessons()
    return render_template('lekce.html', lessons=lessons, active_lesson=session.get('active_lesson'))

@bp.route('/vybrat-lekci/<lesson_name>')
def select_lesson(lesson_name):
    session['active_lesson'] = lesson_name
    return redirect(url_for('main.index'))

@bp.route('/check_answer', methods=['POST'])
def check_answer_route():
    active_lesson = session.get('active_lesson')
    if not active_lesson:
        return jsonify({'error': 'Není vybrána žádná aktivní lekce.'}), 400
    
    data = request.get_json()
    user_answer = data.get('user_answer', '').strip()
    phrase_id = data.get('phrase_id')
    time_elapsed = float(data.get('time_elapsed', -1.0))
    
    all_phrases = load_phrases(active_lesson)
    phrase_to_check = next((p for p in all_phrases if str(p['ID_páru']) == str(phrase_id)), None)

    if not phrase_to_check:
        return jsonify({'error': 'Fráze nenalezena v aktuální lekci.'}), 404

    correct_answer = phrase_to_check['Odpověď_EN'].strip()
    diff_result_html = compare_answers(user_answer, correct_answer)
    
    correctness_ratio = SequenceMatcher(None, user_answer.lower(), correct_answer.lower()).ratio()
    if time_elapsed < 0:
        time_factor = 0.0
    else:
        max_time = (len(correct_answer) / TARGET_CPS) + REACTION_BONUS
        time_factor = max(0.0, min(1.0, 1 - (time_elapsed / max_time)))
    current_score = (correctness_ratio * CORRECTNESS_WEIGHT) + (time_factor * TIME_WEIGHT)
    old_index = phrase_to_check['Index_Naučení']
    new_index = (old_index * OLD_INDEX_WEIGHT) + (current_score * 10 * SCORE_WEIGHT)
    phrase_to_check['Index_Naučení'] = round(max(0.0, min(10.0, new_index)), 2)
    
    save_phrases(active_lesson, all_phrases)
    
    next_phrase_obj = get_next_phrase(all_phrases)
    prepared_next_phrase = prepare_phrase_data(next_phrase_obj)
    
    next_masked_answer = ""
    if prepared_next_phrase:
        next_masked_answer = mask_word(prepared_next_phrase['Odpověď_EN'], prepared_next_phrase['Index_Naučení'])
    
    return jsonify({
        'feedback_html': diff_result_html,
        'next_phrase': prepared_next_phrase, 
        'next_masked_answer': next_masked_answer,
        'translation_answer': phrase_to_check.get('Nápověda_CZ_Odpoved', 'Překlad není k dispozici.')
    })

@bp.route('/audio/<filename>')
def get_audio(filename):
    audio_dir = os.path.join(current_app.root_path, '..', 'audio')
    return send_from_directory(audio_dir, filename)