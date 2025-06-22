from flask import render_template
from app.main import bp
from app.services import load_phrases, mask_word # <-- Přidali jsme import mask_word

@bp.route('/')
def index():
    all_phrases = load_phrases()
    current_phrase = all_phrases[0] if all_phrases else None
    
    masked_answer = ""
    if current_phrase:
        # Zavoláme naši novou funkci na správnou odpověď
        masked_answer = mask_word(
            current_phrase['Odpověď_EN'], 
            current_phrase['Index_Naučení']
        )

    # Předáme do šablony původní frázi i novou maskovanou odpověď
    return render_template('index.html', phrase=current_phrase, masked_answer=masked_answer)