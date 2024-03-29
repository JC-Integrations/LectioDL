# Virker ikke længere

Grundet jeg ikke har noget login til Lectio mere, og ændringer på deres side, kan jeg ikke længere vedligeholde dette projekt.

# LectioDL
LectioDL eller Lectio Downloader, er et program udviklet til at downloade alle dine dokumenter fra lectio. Evt. inden en eksamen, terminsprøve eller inden du dimitterer. Jeg er på nuværende tidspunkt i slutningen af 3. g, så jeg vil ikke have brug for funktionen mere, men nogle andre kan måske få lidt glæde af det.  
Vær opmærksom på at det kan tage noget tid at hente alt ned. Udover at downloade dokumenterne er der også en lille cooldown mellem forskellige elementer for at undgå at du bliver IP banned på Lectios side. Programmet er 100% sikkert at bruge, selv hvis du skulle blive IP banned plejer det typisk kun at vare 10-15 minutter.

### [Download LectioDL (Windows)](https://github.com/JC-Integrations/LectioDL/releases/download/1.1/LectioDL.exe 'Klik her for at downloade den nyeste version af LectioDL')

## To-do
* GUI for at gøre programmet lettere at bruge.

## Hvis du vil køre scriptet direkte
[Main.py](https://github.com/JC-Integrations/LectioDL/blob/main/main.py) indeholder alt kode som programmet består af. Hvis du vil køre den direkte skal du installere de dependencies der er i [requirements.txt](https://github.com/JC-Integrations/LectioDL/blob/main/requirements.txt). For at køre scriptet kræver det python 3.8 eller højere (de versioner jeg har testet).

## Hvis du selv vil compile koden
Det er forståeligt, hvis man selv vil "compile" koden, og helt klart også bedst at gøre det selv for sikkerhedens skyld. Hvem ved, jeg kunne i princippet have smidt noget kode ind der sender dine login oplysninger til min egen webserver (Det har jeg ikke, men i kan se pointen).

*Jeg ved kun, hvordan man gør dette for Windows og Linux systemer, hvis du har mac og kan finde ud af det, så lav venligst en PR.*

**Du skal have python 3.8 eller højere** (Jeg ved ikke hvor langt ned i python versioner dette script kan klare)  
For at compile selv skal du hente al kode ned på din egen computer. Hvis du har git installeret, kan du bruge følgende kommando:

```
git clone https://github.com/JC-Integrations/LectioDL.git
```

Herefter, hvis du vil compile koden ned til en exe. Så skal du først installere de nødvendige python packages. Det gøres med følgende kommando:
```
pip install -r requirements.txt
```

Nu kan du køre [`compiler.py`](https://github.com/JC-Integrations/LectioDL/blob/main/compiler.py), der laver selve exe filen:
```
python compiler.py
```

Når denne er færdig, har du en fil der hedder `LectioDL.exe`, dette er dokument downloaderen.
