# Optical Energy Meter - Frontend
Das Frontend des Prototyps besteht aus einer Python-App mit folgendem Funktionsumfang:
- Verwendung des `Kivy-`UI-Frameworks
- Verwendung von m`atplotlib` zur Erstellung des Diagramms
- Laden der Daten aus der MySQL-Datenbank und Darstellung im `Kivy-App`
- Aktualisierung der Daten jede Minute
- Standardmäßig wird die letzte Stunde für einen Stromzähler mit einer Impulsausgabe von 1000 Impulse/kWh angezeigt. Der Benutzer kann diese Einstellungen anpassen, um einen anderen Stromzähler oder einen anderen Zeitraum anzuzeigen.
- Berechnung des Gesamtverbrauchs für den angezeigten Zeitraum

## inbetriebnahme
Dependencies Installieren:
`python -m pip install --upgrade pip setuptools`
`python -m pip install "kivy[base]" kivy_examples`
`python -m pip install mysql-connector-python` 
`python -m pip install matplotlib` 
App Starten
`./main.py` 