# Mentés – a chat oldal állapota az átépítés előtt

Dátum: 2026-09-16

## Mi van ebben a mappában

- `chat.html` — a `templates/chat.html` pontos másolata az átépítés előtt
- `style.css` — a `static/css/style.css` pontos másolata

## Mire való

Az új, lépésekre bontott munkafelület építése előtt készült. Ha az új
forma nem válik be, ezzel a két fájllal az EDDIGI oldal egy az egyben
visszaáll:

    copy mentes\2026-09-16_atepites_elott\chat.html templates\chat.html
    copy mentes\2026-09-16_atepites_elott\style.css static\css\style.css
    git add templates/chat.html static/css/style.css
    git commit -m "Vissza a regi chat oldalra"
    git push

## Fontos

Ez a mentés a kényelem miatt van. A VALÓDI biztonsági háló a git: minden
korábbi állapot megvan a történetben, akkor is, ha ez a mappa törlődik.
