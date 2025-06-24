document.addEventListener('DOMContentLoaded', () => {
    // --- Prvky na stránce, které ne vždy existují ---
    const answerForm = document.getElementById('answer-form');

    // Pokud formulář neexistuje, jsme na stránce 'lekce.html' a není co dělat.
    if (!answerForm) {
        return;
    }

    // === VÝBĚR PRVKŮ Z HTML (pouze pro tréninkovou stránku) ===
    const phraseQuestionElement = document.getElementById('phrase-question');
    const maskedAnswerElement = document.getElementById('masked-answer');
    const answerInput = document.getElementById('answer-input');
    const phraseIdInput = document.getElementById('phrase-id-input');
    const feedbackContainer = document.getElementById('feedback-container');
    const audioPlayer = document.getElementById('audio-player');
    const infoPanel = document.getElementById('info-panel-wrapper');
    const infoPanelTitle = document.getElementById('info-panel-title');
    const infoPanelContent = document.getElementById('info-panel-content');
    const showTranslationCheckbox = document.getElementById('setting-show-translation');
    const questionHelpIcon = document.getElementById('question-help-icon');

    let startTime;
    let currentPhraseData = {};

    // === HLAVNÍ FUNKCE ===

    async function handleFormSubmit(event) {
        event.preventDefault(); 
        const timeElapsed = startTime ? (new Date() - startTime) / 1000 : -1;
        const dataToSend = {
            user_answer: answerInput.value,
            phrase_id: phraseIdInput.value,
            time_elapsed: timeElapsed
        };

        try {
            const response = await fetch('/check_answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToSend)
            });

            if (!response.ok) throw new Error(`Chyba serveru: ${response.status}`);
            const result = await response.json();

            // Zobrazení HTML feedbacku (oprava chyby s [])
            feedbackContainer.innerHTML = result.feedback_html;

            // Zobrazení překladu ODPOVĚDI
            if (showTranslationCheckbox.checked && result.translation_answer) {
                showInfoPanel("Český význam odpovědi", result.translation_answer);
            }

            playAudio(currentPhraseData.answer_audio_url);
            
            setTimeout(() => {
                updateUIForNextPhrase(result.next_phrase, result.next_masked_answer);
            }, 3000);

        } catch (error) {
            console.error('Došlo k chybě:', error);
            feedbackContainer.textContent = 'Chyba komunikace se serverem.';
        }
    }
    
    function updateUIForNextPhrase(nextPhrase, nextMaskedAnswer) {
        hideInfoPanel();

        if (!nextPhrase) {
            const container = document.getElementById('main-container');
            if(container) {
                container.innerHTML = '<h2>Gratuluji! Všechny fráze v této lekci jsou naučené!</h2>';
            }
            return;
        }

        currentPhraseData = nextPhrase;
        
        phraseQuestionElement.textContent = currentPhraseData.Otázka_EN;
        maskedAnswerElement.innerHTML = nextMaskedAnswer;
        phraseIdInput.value = currentPhraseData.ID_páru;
        
        feedbackContainer.innerHTML = '';
        answerInput.value = '';
        answerInput.focus();

        playAudio(currentPhraseData.question_audio_url);
    }

    function showInfoPanel(title, content) {
        if(infoPanel) {
            infoPanelTitle.textContent = title;
            infoPanelContent.textContent = content;
            infoPanel.classList.remove('hidden');
        }
    }

    function hideInfoPanel() {
        if(infoPanel) {
            infoPanel.classList.add('hidden');
            infoPanelContent.textContent = '';
        }
    }
    
    function playAudio(audioUrl) {
        if (audioUrl && audioPlayer) {
            audioPlayer.src = audioUrl;
            audioPlayer.play().catch(e => console.error("Chyba přehrávání audia:", e));
        }
    }

    function setupSettings() {
        const savedSetting = localStorage.getItem('showTranslation');
        if (savedSetting === 'true') {
            showTranslationCheckbox.checked = true;
        }
        showTranslationCheckbox.addEventListener('change', () => {
            localStorage.setItem('showTranslation', showTranslationCheckbox.checked);
        });
    }

    // === SPUŠTĚNÍ APLIKACE A PŘIPOJENÍ UDÁLOSTÍ ===
    setupSettings();
    answerForm.addEventListener('submit', handleFormSubmit);

    if (audioPlayer) {
        audioPlayer.onplay = () => { startTime = new Date(); };
    }
    
    if (questionHelpIcon) {
        questionHelpIcon.addEventListener('click', () => {
            const helpText = currentPhraseData.Nápověda_CZ_Otazka || 'Překlad není k dispozici.';
            showInfoPanel("Nápověda k otázce", helpText);
        });
    }
    
    const initialDataElement = document.getElementById('initial-phrase-data');
    if (initialDataElement && initialDataElement.textContent) {
        try {
            currentPhraseData = JSON.parse(initialDataElement.textContent);
            if (currentPhraseData && currentPhraseData.question_audio_url) {
                playAudio(currentPhraseData.question_audio_url);
            }
        } catch(e) {
            console.error("Chyba při parsování úvodních dat fráze:", e);
        }
    }
});