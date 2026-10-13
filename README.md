# Lediga jobb i Gästrikland

Statisk sida (GitHub Pages) med lediga jobb från Platsbanken i Sandviken, Gävle, Ockelbo och Hofors.
`index.html` läser `jobs.json`. "Markera som sökt" sparas i webbläsarens localStorage.

## Daglig uppdatering
    python3 /workspace/jobb-gastrikland/update.py /path/nya.json

`nya.json` är en JSON-lista med objekt: `id, rubrik, arbetsgivare, ort, kategori, beskrivning, krav, sista_dag, lank`.
Skriptet sätter `first_seen` till dagens datum för nya id:n, uppdaterar befintliga, tar bort utgångna,
sätter `senast_uppdaterad`, committar och pushar. Kör med tom lista (`[]`) för att bara rensa utgångna.
Lägg till `--no-push` för att testa lokalt.

Kategorier: Bygg/snickeri, Fastighet/vaktmästare, Industri, Lager/logistik, Skog/trä, Transport, Övrigt.
