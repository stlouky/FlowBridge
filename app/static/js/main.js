// app/static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    // === VÝBĚR PRVKŮ Z HTML ===
    const phraseQuestionElement = document.getElementById('phrase-question');
    const maskedAnswerElement = document.getElementById('masked-answer');
    const answerForm = document.getElementById('answer-form');
    const answerInput = document.getElementById('answer-input');
    const phraseIdInput = document.getElementById('phrase-id-input');
    const feedbackContainer = document.getElementById('feedback-container');
    const audioPlayer = document.getElementById('audio-player');

    // === STAVOVÉ PROMĚNNÉ APLIKACE ===
    let startTime; // Pro měření času odpovědi
    // Načteme URL k audiím z Pythonu/Jinja2 (tato data se pošlou s další frází)
    // Inicializujeme je z dat, která jsou v HTML od serveru
    let currentPhraseData = {
        // Zde si uložíme celý objekt fráze, abychom měli všechna data pohromadě
    };

    /**
     * Zpracuje odeslání formuláře (kliknutím nebo klávesou Enter).
     * @param {Event} event - Událost odeslání formuláře.
     */
    async function handleFormSubmit(event) {
        event.preventDefault(); // Zabráníme klasickému odeslání a znovunačtení stránky

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

            // 1. Zobrazíme výsledek (diff)
            feedbackContainer.innerHTML = result.feedback.diff;

            // 2. PŘEHRAJEME ZVUK SPRÁVNÉ ODPOVĚDI
            // URL k audiu odpovědi jsme dostali od serveru už PŘI NAČTENÍ OTÁZKY!
            playAudio(currentPhraseData.answer_audio_url);
            
            // 3. Po chvíli připravíme další frázi
            setTimeout(() => {
                updateUIForNextPhrase(result.next_phrase, result.next_masked_answer);
            }, 2500); // Dáme 2.5s na poslech správné odpovědi

        } catch (error) {
            console.error('Došlo k chybě:', error);
            feedbackContainer.textContent = 'Chyba komunikace se serverem.';
        }
    }
    
    /**
     * Aktualizuje celou stránku pro další frázi.
     * @param {object} nextPhrase - Kompletní objekt další fráze ze serveru.
     * @param {string} nextMaskedAnswer - Nová maskovaná odpověď.
     */
    function updateUIForNextPhrase(nextPhrase, nextMaskedAnswer) {
        if (!nextPhrase) {
            document.querySelector('#main-container').innerHTML = '<h2>Gratuluji! Všechny fráze jsou naučené!</h2>';
            return;
        }

        // Uložíme si kompletní data nové fráze
        currentPhraseData = nextPhrase;
        
        // Aktualizujeme viditelné části stránky
        phraseQuestionElement.textContent = currentPhraseData.Otázka_EN;
        maskedAnswerElement.innerHTML = nextMaskedAnswer;
        phraseIdInput.value = currentPhraseData.ID_páru;
        
        // Vyčistíme starý stav
        feedbackContainer.innerHTML = '';
        answerInput.value = '';
        answerInput.focus();

        // Přehrání zvuku NOVÉ otázky
        playAudio(currentPhraseData.question_audio_url);
    }
    
    /**
     * Univerzální funkce pro přehrání zvuku.
     * @param {string} audioUrl - URL adresa k MP3 souboru.
     */
    function playAudio(audioUrl) {
        if (audioUrl && audioPlayer) {
            audioPlayer.src = audioUrl;
            audioPlayer.play().catch(e => console.error("Chyba přehrávání audia:", e));
        }
    }

    // === SPUŠTĚNÍ APLIKACE ===

    // Připojíme hlavní funkci na událost 'submit' formuláře
    if (answerForm) {
        answerForm.addEventListener('submit', handleFormSubmit);
    }

    // Nastartujeme časovač vždy, když se začne přehrávat jakýkoliv zvuk
    if (audioPlayer) {
        audioPlayer.onplay = () => { startTime = new Date(); };
    }
    
    // Načteme data pro první frázi z HTML, které poslal server
    fetch('/check_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_answer: '', phrase_id: phraseIdInput.value, time_elapsed: -1 })
    }).then(res => res.json()).then(result => {
        currentPhraseData = result.next_phrase;
        playAudio(currentPhraseData.question_audio_url);
    });
});
