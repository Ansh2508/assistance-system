---
name: velth-linkedin-caption
description: Schreibt den Begleittext (Caption) für einen velth LinkedIn Carousel Post auf der Unternehmensseite, plus Erstkommentar mit Quellen. Lädt außerdem die Regeln für Upload und Buffer Draft. Immer laden, wenn ein Carousel Post getextet, überarbeitet oder als Draft eingeplant wird.
---

# velth Carousel Caption

Der Text hat eine Aufgabe: Daumen anhalten, Neugier erzeugen, ins Carousel schicken. Nicht erklären, was drin steht. Das Carousel erklärt sich selbst.

## Harte Regeln (nicht verhandelbar)

**Keine Bindestriche und keine Gedankenstriche. Überhaupt keine.**
Kein `-`, kein `–`, kein `—`. Sie werden im LinkedIn Rendering langgezogen und sehen kaputt aus. Das gilt auch innerhalb von Wörtern.
- „audit-ready" → „prüfbereit"
- „KI-generiert" → „von KI erstellt"
- „E-Mail" → „Mail" oder „per Mail"
- „Be- und Entladen" → „Be und Entladen"
- „2-4 Stunden" → „2 bis 4 Stunden"
- Zusammensetzungen ausschreiben oder umformulieren, notfalls trennen: „GBU Pflicht" statt „GBU-Pflicht"

**Sprache:** Ausschließlich Deutsch auf der Unternehmensseite. Nie zwei Sprachen in einem Post. Sie Form.

**Länge:** 90 bis 150 Wörter. Erste Zeile maximal 12 Wörter, damit sie vor dem „mehr anzeigen" komplett steht.

**Pflichtbestandteile, in dieser Reihenfolge:**
1. Hook: eine Zeile, konkret, am besten mit Zahl oder Widerspruch. Keine Frage als Hook.
2. Zwei bis vier kurze Absätze mit dem eigentlichen Inhalt. Jeder Absatz ein Gedanke, Leerzeile dazwischen.
3. CTA: eine Zeile, konkret, kein „Was denkst du?"
4. `velth.io` als eigene Zeile.
5. Maximal 3 Hashtags, fachlich, keine Mode Tags.

**Externe Links** (Gesetze, Quellen, DGUV Dokumente) gehören in den Erstkommentar, nie in den Post. LinkedIn drosselt Beiträge mit Fremdlinks.

**Erstkommentar** immer mitliefern: Paragraphen und Normen im Volltext, Quelle mit Jahr. Kein Marketing.

## Verbotene Formulierungen (klingen nach KI)

Nicht verwenden: „In der heutigen Zeit", „Es ist wichtig zu beachten", „Fazit", „Lass uns", „Tauche ein", „revolutionär", „ganzheitlich", „nahtlos", „Game Changer", „Deep Dive", „🚀 bei Aufzählungen", „Zusammenfassend", rhetorische Dreierketten („schneller, besser, einfacher"), Emojis als Listenpunkte.

Kein Emoji Feuerwerk. Maximal eines, wenn es trägt. Meist keines.

## Ton

Wie ein erfahrener SiFa, der Klartext redet: nüchtern, konkret, respektvoll gegenüber dem Betrieb. Nie belehrend, nie alarmistisch. Der Betrieb ist nicht schlampig, ihm fehlt Zeit und Werkzeug.

Zahlen immer mit Jahr und Quelle im Kommentar. Nie eine Zahl ohne Anker.

## Fakten Regeln

Nur Zahlen aus dem velth Kanon (`velth_legal_reference.md`). Insbesondere:
- 754.660 meldepflichtige Arbeitsunfälle, 345 tödliche (DGUV 2024 final)
- Jeder dritte Betrieb ohne GBU (GDA Betriebsbefragung 2023/24)
- Mindestbesichtigungsquote 5 Prozent, über 100.000 Prüfungen im Jahr, vorher 0,84 Prozent (2022). Nie 175.000.
- §25 ArbSchG: Regelsatz 5.000 Euro, Maximum 30.000 Euro bei Anordnungsverstoß. Nie „30.000 pro fehlende GBU".
- SiFa betreut im Schnitt 14 Betriebe (BAuA F2388). Nie „20 bis 60".
- Pilotstand: „eine kleine Gruppe von Pilotbetrieben". Nie Zahlen erfinden.

Wenn eine Zahl nicht im Kanon steht: nicht verwenden oder vorher verifizieren.

## Struktur Vorlage

```
[Hook: eine Zeile, konkret, Zahl oder Widerspruch]

[Absatz: warum das so ist, ohne Vorwurf]

[Absatz: was daraus folgt, die praktische Konsequenz]

[Optional: der überraschende Punkt, den kaum jemand kennt]

[CTA: eine Zeile]

velth.io

#Fachtag1 #Fachtag2 #Arbeitsschutz
```

## CTA Baukasten (rotieren, nicht wiederholen)

- „Das ganze Thema in sieben Slides oben im Beitrag."
- „Wie Sie das in Minuten dokumentieren, zeigen wir auf velth.io."
- „Prüfen Sie es einmal an Ihrem eigenen Betrieb."
- „Betriebe testen velth kostenlos, SiFas fragen einen Pilotzugang an."

## Selbstprüfung vor der Abgabe

Diese Liste durchgehen, keine Ausnahme:

1. Enthält der Text irgendwo `-`, `–` oder `—`? → entfernen
2. Erste Zeile unter 12 Wörtern?
3. Wortzahl zwischen 90 und 150?
4. Genau ein `velth.io`, als eigene Zeile?
5. Maximal 3 Hashtags?
6. Kein externer Link im Post?
7. Jede Zahl im Kanon belegt und im Erstkommentar mit Jahr benannt?
8. Keine verbotene Formulierung, kein Emoji Wildwuchs?
9. Nur Deutsch?
10. CTA vorhanden und konkret?

## Upload und Draft Regeln

- **Nur die finale Carousel Version** wird hochgeladen und als Draft angelegt. Zwischenstände bleiben im Chat.
- Vor dem Upload: Pixel Lint bestanden, Wortband je Slide eingehalten, keine Bindestriche im Deck, keine Adresse außer „München".
- Assets liegen im Google Drive Ordner `velth-linkedin-assets`, Struktur `week_<KW>/<thema>/carousel.pdf` plus `slide_01.png`.
- Buffer Draft immer mit: Kanal velth (`69ce3cb2af47dacb697e92c8`), `saveToDraft: true`, Termin im Fenster Dienstag bis Donnerstag 8 bis 10 Uhr, Asset als LinkedIn Dokument mit Thumbnail.
- Der Draft bleibt Draft. Freigabe erfolgt ausschließlich durch Bruno.
- Erstkommentar Text mit dem Draft im Chat ausgeben, damit er beim Posten direkt eingefügt werden kann.
