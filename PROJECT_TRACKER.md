Project FlowBridge: Project Tracker

Poslední aktualizace: 24. 6. 2025, 10:25 (CEST)

Tento dokument slouží jako centrální bod pro sledování postupu, technologií a klíčových rozhodnutí v rámci projektu FlowBridge. Jeho účelem je umožnit komukoliv (včetně AI asistenta v novém chatu) rychle pochopit stav projektu a plynule navázat na předchozí práci.
1. Vize Projektu (The "Why")

Cílem je vytvořit dvoufázový učební systém pro anglickou konverzaci:

    Fáze 1 (Aplikace FlowBridge): Vytvořit personalizovanou desktopovou webovou aplikaci pro intenzivní trénink a automatizaci anglických konverzačních frází. Uživatel si zde buduje "arzenál" frází.

    Fáze 2 (Konverzace s AI): Využít naučené fráze v reálné, dynamické hlasové konverzaci s externí konverzační AI (např. Gemini) na mobilním telefonu.

2. Klíčové Koncepty Aplikace (The "What")

    Učení v kontextu: Aplikace pracuje s "konverzačními páry" (Otázka -> Odpověď).

    Adaptivní obtížnost: Používá "Index Naučení" (škála 0.0-10.0), který se dynamicky počítá na základě míry správnosti a rychlosti odpovědi.

    Aktivní zapojení: Uživatelova odpověď je procvičována pomocí "mizejících písmen", jejichž počet se odvíjí od Indexu Naučení.

    Audio-first přístup: Uživatel slyší otázku a po vyhodnocení slyší i správnou odpověď, což uzavírá učební smyčku.

    Caching zvuků: Audio soubory pro otázky i odpovědi se generují on-demand a ukládají lokálně, aby se šetřily API dotazy a aplikace byla rychlá.

    Plynulý pracovní tok (Flow): Aplikace je plně ovladatelná z klávesnice (odeslání odpovědi klávesou Enter).

3. Technologický Stack (The "How")

    Backend: Python 3, Flask

    Frontend: HTML5, CSS3, Vanilla JavaScript (asynchronní komunikace přes JSON)

    Ukládání dat: CSV soubor (fraze.csv)

    Generování zvuku: gTTS

    Architektura: Profesionální struktura (App Factory, Blueprints) s oddělenou servisní vrstvou (app/services).

    Prostředí: Fedora Linux (desktop), rozhraní v lokálním webovém prohlížeči, virtuální prostředí myenv.

    Verzování: Git, GitHub.

4. Dosavadní Postup (Completed Milestones)

    [22.6.2025] Definována vize, název (FlowBridge) a technologický stack.

    [22.6.2025] Vytvořena profesionální adresářová struktura a zprovozněna.

    [22.6.2025] Implementována interaktivní smyčka a audio-first funkcionalita (přehrávání otázek).

    [23.6.2025] Implementován pokročilý výpočet 'Indexu Naučení' (zohledňuje správnost i rychlost).

    [24.6.2025] Implementováno přehrávání audia správné odpovědi po vyhodnocení.

    [24.6.2025] Implementováno odesílání odpovědi klávesou Enter pro lepší ergonomii.

    [24.6.2025] Optimalizována architektura pro robustnější a rychlejší chod (příprava všech dat dopředu).

    [24.6.2025] Finálně odladěna a stabilizována aplikace, opraveny chyby (chybějící moduly, zobrazení feedbacku).

5. Aktuální Stav a Další Krok (Current Status & Next Step)

    Aktuální stav: Základní učební cyklus aplikace je funkčně kompletní a stabilní. Všechny klíčové interakce pro trénink jedné fráze jsou implementovány a odladěny. Aplikace je nyní plně použitelná pro svůj primární účel – efektivní trénink.

    Další okamžitý krok: Implementovat správu frází (CRUD). Cílem je odstranit nutnost manuální editace souboru fraze.csv. Vytvoříme jednoduché webové rozhraní, které uživateli umožní:

        Přidávat nové konverzační páry.

        Zobrazit seznam všech existujících frází.

        Upravovat a mazat stávající fráze.

6. Klíčová Rozhodnutí (Key Decisions Log)

    Desktop-first: Aplikace (Fáze 1) běží jako webová aplikace primárně na desktopu.

    Ukládání zvuku (Caching): Všechny generované zvuky se ukládají lokálně.

    Příprava dat "dopředu": Veškerá potřebná data pro další krok (včetně URL k oběma audiím) se připravují na serveru a posílají najednou pro maximální rychlost a robustnost na straně klienta.

    Servisní vrstva: Projekt využívá oddělenou servisní vrstvu (app/services) pro zapouzdření datové a obchodní logiky.