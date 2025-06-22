Project FlowBridge: Project Tracker

Poslední aktualizace: 22. 6. 2025, 22:21 (CEST)

Tento dokument slouží jako centrální bod pro sledování postupu, technologií a klíčových rozhodnutí v rámci projektu FlowBridge. Jeho účelem je umožnit komukoliv (včetně AI asistenta v novém chatu) rychle pochopit stav projektu a plynule navázat na předchozí práci.
1. Vize Projektu (The "Why")

Cílem je vytvořit dvoufázový učební systém pro anglickou konverzaci:

    Fáze 1 (Aplikace FlowBridge): Vytvořit personalizovanou desktopovou webovou aplikaci pro intenzivní trénink a automatizaci anglických konverzačních frází. Uživatel si zde buduje "arzenál" frází.
    Fáze 2 (Konverzace s AI): Využít naučené fráze v reálné, dynamické hlasové konverzaci s externí konverzační AI (např. Gemini) na mobilním telefonu.

2. Klíčové Koncepty Aplikace (The "What")

    Učení v kontextu: Aplikace pracuje s "konverzačními páry" (Otázka -> Odpověď).
    Adaptivní obtížnost: Používá "Index Naučení" (škála 0.0-10.0), který kombinuje správnost a rychlost odpovědi.
    Aktivní zapojení: Uživatelova odpověď je procvičována pomocí "mizejících písmen", jejichž počet se odvíjí od Indexu Naučení.
    Audio-first přístup: Uživatel primárně poslouchá otázku a učí se reagovat na mluvené slovo.
    Caching zvuků: Vygenerované zvukové soubory se ukládají lokálně, aby se šetřily API dotazy a aplikace byla rychlá a funkční i offline.

3. Technologický Stack (The "How")

    Backend: Python 3, Flask
    Frontend: HTML5, CSS3, Vanilla JavaScript
    Ukládání dat: CSV soubor (fraze.csv)
    Generování zvuku: gTTS (startovní verze, s možností upgradu na Google Cloud TTS / ElevenLabs)
    Prostředí: Fedora Linux (desktop), rozhraní v lokálním webovém prohlížeči, virtuální prostředí myenv
    Verzování: Git, GitHub

4. Dosavadní Postup (Completed Milestones)

    [22.6.2025] Definována vize a dvoufázový model učení.
    [22.6.2025] Zvolen název projektu: FlowBridge.
    [22.6.2025] Definována a odsouhlasena sada technologií (Tech Stack).
    [22.6.2025] Vyřešeny obavy ohledně nákladů na TTS služby.
    [22.6.2025] Dohodnut pracovní postup přes GitHub a vytvořen PROJECT_TRACKER.md.
    [22.6.2025] Založen a naklonován GitHub repozitář.
    [22.6.2025] Vytvořena profesionální adresářová struktura a zprovozněna v nové podobě (App Factory, Blueprints).
    [22.6.2025] Implementována interaktivní smyčka s "chytrou" zpětnou vazbou (diff).
    [22.6.2025] Implementována audio-first funkcionalita. Aplikace nyní automaticky přehrává zvuk otázky. Zvukové soubory se generují on-demand (gTTS) a ukládají do mezipaměti (cache).

5. Aktuální Stav a Další Krok (Current Status & Next Step)

    Aktuální stav: Aplikace má plně funkční učební cyklus: dynamické načítání frází, chytré 'diff' porovnání odpovědi a audio přehrávání otázek. Základní aktualizace Indexu Naučení (bez časového faktoru) funguje a ukládá se do CSV.
    Další okamžitý krok: Implementovat započítávání času odpovědi do výpočtu Indexu Naučení pro ještě přesnější a efektivnější učení.

6. Klíčová Rozhodnutí (Key Decisions Log)

    Desktop-first: Aplikace (Fáze 1) poběží jako webová aplikace primárně na desktopu.
    Ukládání zvuku (Caching): Všechny generované zvuky se ukládají lokálně.
    Čeština jako nápověda: V datovém modelu bude existovat volitelná česká nápověda.
    Profesionální struktura: Projekt využívá strukturu s "Application Factory" a "Blueprints".
    Virtuální prostředí: Veškeré závislosti jsou spravovány v myenv.
    Vylepšená zpětná vazba: Rušivé alert() okno nahrazeno integrovanou zprávou s vizuálním porovnáním ("diff").