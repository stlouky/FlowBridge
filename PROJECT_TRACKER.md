Project FlowBridge: Project Tracker

Poslední aktualizace: 24. 6. 2025, 14:15 (CEST)

Tento dokument slouží jako centrální bod pro sledování postupu, technologií a klíčových rozhodnutí v rámci projektu FlowBridge. Jeho účelem je umožnit komukoliv (včetně AI asistenta v novém chatu) rychle pochopit stav projektu a plynule navázat na předchozí práci.
1. Vize Projektu (The "Why")

Cílem je vytvořit dvoufázový učební systém pro anglickou konverzaci:

    Fáze 1 (Aplikace FlowBridge): Vytvořit personalizovanou desktopovou webovou aplikaci pro intenzivní trénink a automatizaci anglických konverzačních frází.

    Fáze 2 (Konverzace s AI): Využít naučené fráze v reálné, dynamické hlasové konverzaci s externí konverzační AI.

2. Klíčové Koncepty Aplikace (The "What")

    Strukturované lekce: Fráze jsou organizovány do lekcí, počínaje výchozí sadou "Jádro pro přežití" pro okamžité použití.

    Chytré generování obsahu: Nové lekce lze vytvářet pomocí "Inspirátoru Frází", který na základě požadavku uživatele a AI analýzy četnosti generuje relevantní obsah.

    Adaptivní obtížnost: Používá "Index Naučení" (0.0-10.0), který dynamicky hodnotí správnost a rychlost odpovědi.

    Audio-first přístup: Uživatel slyší otázku a po vyhodnocení i správnou odpověď.

    Kontrola duplicit: Při importu nových frází systém kontroluje přesné i podobné duplicity, aby se zabránilo redundanci.

    Volitelná nápověda: Po vyhodnocení odpovědi se může volitelně zobrazit český význam fráze.

3. Technologický Stack (The "How")

    Backend: Python 3, Flask

    Frontend: HTML5, CSS3, Vanilla JavaScript

    Ukládání dat: Samostatné CSV soubory pro každou lekci.

    Generování zvuku: gTTS

    Architektura: App Factory, Blueprints, Servisní vrstva.

    Prostředí: Fedora Linux, virtuální prostředí myenv, Git, GitHub.

4. Dosavadní Postup (Completed Milestones)

    [22.6.2025] Definována vize, název a technologický stack.

    [22.6.2025] Vytvořena profesionální adresářová struktura.

    [23.6.2025] Implementován pokročilý výpočet 'Indexu Naučení'.

    [24.6.2025] Finálně odladěn a stabilizován základní tréninkový cyklus (audio, ovládání klávesnicí, zobrazení feedbacku).

5. Aktuální Stav a Další Krok (Current Status & Next Step)

    Aktuální stav: Základní tréninkový engine aplikace je plně funkční a stabilní.

    Další okamžitý krok: Implementace kompletní správy obsahu dle nové definice. To zahrnuje:

        Vytvoření výchozí sady lekcí "Jádro pro přežití" (6 předpřipravených CSV souborů).

        Implementace rozhraní pro správu lekcí (CRUD): Zobrazení seznamu lekcí, výběr aktivní lekce pro trénink, vytváření a mazání lekcí.

        Implementace "Inspirátoru Frází": Stránka s rozhraním pro generování nových lekcí pomocí AI, včetně kontroly duplicit a zobrazení náhledu.

        Integrace českého významu: Doplnění datového modelu a zobrazení volitelné nápovědy v tréninkovém rozhraní.

6. Klíčová Rozhodnutí (Key Decisions Log)

    Desktop-first: Aplikace je primárně cílena na desktop.

    Příprava dat "dopředu": Pro maximální odezvu se data (včetně audio URL) připravují na serveru a posílají najednou.

    Defaultní obsah: Aplikace obsahuje výchozí sadu 6 lekcí ("Jádro pro přežití") pro okamžité použití a snadný start.

    Chytré generování obsahu: Nové lekce lze generovat pomocí AI ("Inspirátor Frází") na základě požadavků na četnost a funkci.

    Kontrola duplicit: Implementován mechanismus pro kontrolu přesných i podobných duplicit při importu nových frází.

    Lekce jako soubory: Každá lekce je uložena jako samostatný, snadno spravovatelný CSV soubor.