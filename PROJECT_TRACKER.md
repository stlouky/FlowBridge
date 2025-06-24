Project FlowBridge: Project Tracker

Poslední aktualizace: 23. 6. 2025, 09:00 (CEST)

Tento dokument slouží jako centrální bod pro sledování postupu, technologií a klíčových rozhodnutí v rámci projektu FlowBridge. Jeho účelem je umožnit komukoliv (včetně AI asistenta v novém chatu) rychle pochopit stav projektu a plynule navázat na předchozí práci.
1. Vize Projektu (The "Why")

Cílem je vytvořit dvoufázový učební systém pro anglickou konverzaci:

    Fáze 1 (Aplikace FlowBridge): Vytvořit personalizovanou desktopovou webovou aplikaci pro intenzivní trénink a automatizaci anglických konverzačních frází. Uživatel si zde buduje "arzenál" frází.
    Fáze 2 (Konverzace s AI): Využít naučené fráze v reálné, dynamické hlasové konverzaci s externí konverzační AI (např. Gemini) na mobilním telefonu.

2. Klíčové Koncepty Aplikace (The "What")

    Učení v kontextu: Aplikace pracuje s "konverzačními páry" (Otázka -> Odpověď).
    Adaptivní obtížnost: Používá "Index Naučení" (škála 0.0-10.0), který se dynamicky počítá na základě míry správnosti a rychlosti odpovědi. Rychlost se hodnotí vůči cílové rychlosti psaní (CPS) a délce fráze.
    Aktivní zapojení: Uživatelova odpověď je procvičována pomocí "mizejících písmen" (mask_word), jejichž počet se odvíjí od Indexu Naučení.
    Audio-first přístup: Uživatel primárně poslouchá otázku a učí se reagovat na mluvené slovo.
    Caching zvuků: Vygenerované zvukové soubory se ukládají lokálně, aby se šetřily API dotazy a aplikace byla rychlá a funkční i offline.

3. Technologický Stack (The "How")

    Backend: Python 3, Flask
    Frontend: HTML5, CSS3, Vanilla JavaScript (komunikace přes JSON)
    Ukládání dat: CSV soubor (fraze.csv)
    Generování zvuku: gTTS (startovní verze, s možností upgradu)
    Architektura: Profesionální struktura (App Factory, Blueprints) s oddělenou servisní vrstvou (app/services) pro datovou a business logiku.
    Prostředí: Fedora Linux (desktop), rozhraní v lokálním webovém prohlížeči, virtuální prostředí myenv
    Verzování: Git, GitHub

4. Dosavadní Postup (Completed Milestones)

    [22.6.2025] Definována vize, název (FlowBridge) a technologický stack.
    [22.6.2025] Vyřešeny obavy ohledně nákladů na TTS (lokální caching).
    [22.6.2025] Vytvořena adresářová struktura (App Factory, Blueprints) a zprovozněna.
    [22.6.2025] Implementována interaktivní smyčka s "chytrou" zpětnou vazbou (diff).
    [22.6.2025] Implementována audio-first funkcionalita s on-demand generováním a ukládáním zvuků.
    [23.6.2025] Implementován pokročilý výpočet 'Indexu Naučení'. Nyní zohledňuje nejen správnost, ale i rychlost odpovědi v poměru 80/20. Časový limit je dynamický a odvíjí se od délky fráze a cílové rychlosti psaní (1.67 ZzS).
    [23.6.2025] Doladěna a implementována komunikace mezi frontendem a backendem na bázi JSON pro plynulejší chod aplikace (SPA-style).
    [23.6.2025] Implementována funkce "mizejících písmen" (mask_word) pro aktivní procvičování.

5. Aktuální Stav a Další Krok (Current Status & Next Step)

    Aktuální stav: Aplikace má plně funkční a pokročilý učební cyklus. Dynamicky vybírá fráze s nejnižším indexem, generuje a cachuje pro ně zvuk, přijímá odpověď, vyhodnocuje ji na základě správnosti i rychlosti, a plynule připravuje další frázi bez nutnosti znovunačtení stránky. Všechny klíčové koncepty z vize jsou nyní implementovány v základní podobě.
    Další okamžitý krok: Implementovat jednoduché uživatelské rozhraní (nová stránka/sekce v aplikaci) pro správu frází – přidávání nových konverzačních párů (Otázka/Odpověď/Nápověda CZ) přímo v aplikaci. Cílem je odstranit nutnost manuální editace fraze.csv.

6. Klíčová Rozhodnutí (Key Decisions Log)

    Desktop-first: Aplikace (Fáze 1) poběží jako webová aplikace primárně na desktopu.
    Ukládání zvuku (Caching): Všechny generované zvuky se ukládají lokálně.
    Profesionální struktura: Projekt využívá strukturu s "Application Factory" a "Blueprints".
    Vylepšená zpětná vazba: Rušivé alert() okno nahrazeno integrovanou zprávou s vizuálním porovnáním ("diff").
    Výpočet 'Indexu Naučení': Je založen na dynamickém časovém limitu (dle délky fráze a CPS) a váženém průměru, nikoliv na pevných přírůstcích/pokutách.
    Komunikace FE/BE: Probíhá asynchronně pomocí JSON, což umožňuje chod aplikace ve stylu Single Page Application (SPA).
    Servisní vrstva: Projekt využívá oddělenou servisní vrstvu (app/services) pro zapouzdření datové a obchodní logiky, což zpřehledňuje kód v routes.py.