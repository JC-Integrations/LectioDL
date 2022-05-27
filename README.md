# LectioDL
LectioDL er et program udviklet til at downloade alle dine dokumenter fra lectio. Evt. inden en eksamen, terminsprøve eller inden du dimitterer. Lavet af en gymnasie elev der har/havde samme problem. Jeg er på nuværende tidspunkt i slutningen af 3. g, så jeg vil ikke have brug for funktionen mere, men nogle andre kan måske få lidt glæde af det.

## Hvis du selv vil compile koden
Det er forståeligt, hvis man selv vil compile koden, og helt klart også bedst at gøre det selv for sikkerhedens skyld. Hvem ved, jeg kunne i princippet have smidt noget kode ind der sender dine login oplysninger til min egen webserver (Det har jeg ikke, men i kan se pointen).

*Jeg ved kun, hvordan man gør dette for Windows og Linux systemer, hvis du har mac og kan finde ud af det, så lav venligst en PR*

**Du skal have python 3.8 eller højere** (Jeg ved ikke hvor langt ned i python versioner dette script kan klare)
For at compile selv skal du hente al kode ned på din egen computer. Hvis du har git installeret, kan du bruge følgende kommando:

```
git clone https://github.com/JC-Integrations/LectioDL.git
```

Herefter, hvis du vil compile koden ned til en exe. Så skal du først installere de nødvendige python packages. Det gøres med følgende kommando:
```
pip install -r requirements.txt
```

Nu kan du køre `compiler.py`, der laver selve exe filen:
```
python compiler.py
```

Når denne er færdig, har du en fil der hedder `LectioDL.exe`, dette er dokument downloaderen.
