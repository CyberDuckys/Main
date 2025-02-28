# DebugDucks
Project Distributiecentrum Bart

## Stappen om de app te draaien:

1. **Zorg ervoor dat de volgende software is geïnstalleerd**:
   - Python 3.x
   - pip (Python package manager)

2. **Maak een virtuele omgeving aan in de 'website/' folder en activeer deze**:
   
   - **Op Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - **Op macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   3. **Installeer de vereiste afhankelijkheden**:
     ```bash
     pip install -r requirements.txt
     ```

   4. **Plaats de DB-gegevens in het .env bestand**:  
      De databasegegevens ontvang je in een apart document (appConfig.py) van de host van deze code. Plaats deze gegevens in het `.env` bestand in de hoofdmap van het project. Dit bestand wordt door de applicatie gebruikt om verbinding te maken met de database.

   5. **Run de applicatie**:
     Nu kun je de app starten vanaf `app.py` of in de terminal met het volgende commando:
     ```bash
     python app.py
     ```

## Let op:
- Zorg ervoor dat het `.env` bestand niet wordt gedeeld via versiebeheer! Het moet in je `.gitignore` bestand staan, zodat het niet per ongeluk wordt gepusht naar je Git repository.