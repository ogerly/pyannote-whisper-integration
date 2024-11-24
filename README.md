# PyAnnote & Whisper Integration - README

![image](https://github.com/user-attachments/assets/8053607d-5d7b-410c-b85d-f0360936339d)



## Einleitung

Dieses Projekt kombiniert die Leistungsfähigkeit von **PyAnnote** zur Sprecherdiarisierung und **Whisper** zur Audio-Transkription. Es wurde eine Webanwendung entwickelt, mit der Benutzer Audiodateien hochladen, analysieren und die Ergebnisse (z.B. Sprecherzuordnungen und Transkripte) visuell anzeigen lassen können. Die Anwendung ist mit Flask als Backend und einer einfachen HTML-Frontend-Benutzeroberfläche realisiert.

## Funktionalitäten

- **Audiodateien hochladen**: Benutzer können MP3- oder WAV-Dateien hochladen, die dann automatisch in das WAV-Format umgewandelt werden, falls sie im MP3-Format vorliegen.
- **Audioanalyse starten**: Nachdem die Datei hochgeladen wurde, kann der Benutzer die Analyse starten. Dabei werden die verschiedenen Sprecher in der Datei identifiziert und die jeweiligen gesprochenen Segmente transkribiert.
- **Sprecherzuordnung bearbeiten**: Benutzer können den Sprecherbezeichnungen manuell Namen zuordnen, um eine bessere Lesbarkeit zu ermöglichen.
- **Audiowiedergabe der gesamten Datei oder einzelner Segmente**: Nach der Analyse können Benutzer die gesamte hochgeladene Audiodatei oder spezifische Sprechersegmente direkt im Browser abspielen.

## Voraussetzungen

- **Python 3.10 oder höher**
- **ffmpeg** (für die Umwandlung von MP3 in WAV)
- **Flask** und weitere Python-Bibliotheken:
  - **PyAnnote** zur Sprecherdiarisierung
  - **Whisper** für die Transkription
  - **dotenv** zum Laden von Umgebungsvariablen
  - **pydub** für die Audiokonvertierung
  - **Wavesurfer.js** für die visuelle Darstellung der Audiowellenform im Browser

## Installation und Ausführung

1. **Repository klonen**:

   ```bash
   git clone https://github.com/dein-benutzername/pyannote-whisper-integration.git
   cd pyannote-whisper-integration
   ```

2. **Python-Umgebung einrichten und Abhängigkeiten installieren**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **.env-Datei erstellen**: Erstellen Sie eine `.env`-Datei mit den notwendigen API-Schlüsseln für Hugging Face und ggf. OpenAI:

   ```
   HUGGINGFACE_API_KEY=dein_huggingface_api_schluessel
   OPENAI_API_KEY=dein_openai_api_schluessel
   ```

4. **ffmpeg installieren** (falls noch nicht installiert):

   ```bash
   sudo apt-get install ffmpeg
   ```

5. **Anwendung starten**:

   ```bash
   flask run
   ```

   Die Anwendung wird lokal unter `http://127.0.0.1:5000` ausgeführt.

## Nutzung

- **Audio hochladen**: Klicken Sie auf "Datei auswählen", wählen Sie eine MP3- oder WAV-Datei aus und klicken Sie auf "Datei hochladen".
- **Analyse starten**: Nach erfolgreichem Upload klicken Sie auf "Starte Analyse", um den Diarisierungs- und Transkriptionsprozess zu starten.
- **Sprecher benennen**: Nach der Analyse werden alle Segmente und ihre jeweiligen Sprecher angezeigt. Hier können Sie die Standardbezeichnungen (SPEAKER\_01, SPEAKER\_02, etc.) durch eigene Namen ersetzen.
- **Audio anhören**: Nutzen Sie die Schaltfläche "Play/Pause", um die gesamte Datei abzuspielen, oder klicken Sie auf "Anhören" in den Segmenten, um spezifische Teile der Aufnahme zu hören.

## Aufbau der Anwendung

### Backend (Flask)

Das Backend ist mit Flask implementiert und enthält alle API-Endpunkte für das Hochladen, die Analyse und die Rückgabe der Ergebnisse. Es gibt drei Hauptendpunkte:

- `/upload`: Hier wird die Audiodatei vom Benutzer hochgeladen und ggf. in WAV konvertiert.
- `/analyze`: Startet die Sprecherdiarisierung und Transkription mit PyAnnote und Whisper.
- `/get_audio`: Zum Zurückgeben der Audiodatei, damit sie im Frontend abgespielt werden kann.

### Frontend (HTML + JavaScript)

Das Frontend ist eine einfache HTML-Seite, die mit CSS (Bulma-Framework) gestaltet wurde. JavaScript steuert die Benutzerinteraktion und nutzt Wavesurfer.js, um eine Audiowiedergabe und visuelle Darstellung der Audiowellenform zu ermöglichen.

- **Wavesurfer.js**: Wird verwendet, um eine intuitive Audiowiedergabe zu bieten und bestimmte Bereiche der Audiodatei (Sprechersegmente) abspielen zu können.

### Kommunikation zwischen Frontend und Backend

Die Kommunikation erfolgt hauptsächlich über zwei Hauptmethoden:

- **Fetch-API**: Zum Hochladen der Datei und Anfordern der Analyseergebnisse.
- **Event Listener**: Für Benutzerinteraktionen wie das Klicken auf "Play" oder "Starte Analyse".

## Mindmap zur Prozessübersicht

Eine Mindmap zur Visualisierung der Abläufe kann wie folgt aussehen:

- **Start**
  - **Datei hochladen**
    - Eingabe: MP3/WAV Datei
    - Aktion: Datei wird gespeichert (ggf. Konvertierung)
  - **Analyse starten**
    - Sprecherdiarisierung mit PyAnnote
    - Transkription mit Whisper
  - **Ergebnisse anzeigen**
    - Segmente mit Start-/Endzeiten
    - Zuordnung von Sprechern
    - **Interaktionen**
      - Namen von Sprechern anpassen
      - Segmente anhören mittels Wavesurfer.js

Die Mindmap würde die Beziehungen zwischen diesen Prozessen zeigen, mit **Datei hochladen** als zentralem Punkt, von dem die weiteren Aktionen abzweigen (ähnlich einem Flussdiagramm).

## Erweiterungsmöglichkeiten

- **Automatische Protokollerstellung**: Integration eines NLP-Modells zur Erstellung eines zusammenfassenden Protokolls basierend auf den transkribierten Sprecherbeiträgen.
- **Live-Transkription**: Echtzeit-Sprechererkennung und Transkription, um Live-Meetings zu unterstützen.
- **Bessere Visualisierung**: Integration eines detaillierteren Zeitstrahls zur Visualisierung der Sprecherwechsel.

## Lizenz

Das Projekt steht unter der MIT-Lizenz. Bitte überprüfen Sie die `LICENSE`-Datei für weitere Details.

---

Dies sollte die grundlegenden Informationen enthalten, die notwendig sind, um das Projekt zu verstehen und damit zu arbeiten. Viel Erfolg beim Weiterentwickeln der Anwendung! Wenn noch Fragen bestehen oder mehr Funktionen benötigt werden, kannst du mich gerne kontaktieren.

