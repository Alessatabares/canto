# canto

Coach de canto privado: **análisis de voz** + **mapas de notas por canción** para
practicar con Vocal Pitch Monitor.

Repo **privado** y separado del de idiomas. Las grabaciones de voz **no se suben**
(privacidad + tamaño): solo se versiona el *análisis* (números) y los mapas de canción.

## Estructura

```
canto/
├── perfil.md              # tu mapa vocal (rango, zona verde, regla de tono)
├── tools/
│   └── analizar_voz.py    # analiza una grabación -> rango, tesitura, estabilidad, brillo
├── grabaciones/           # tus audios (NO se versionan; .gitignore)
├── analisis/              # reportes .json/.md de cada grabación (sí se versionan)
└── canciones/             # mapas palabra->nota por canción (sí se versionan)
```

## Setup (una vez)

```bash
cd canto
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# para leer .m4a/.mp3 hace falta ffmpeg; con .wav no:
#   (Windows) instala ffmpeg o exporta a WAV desde Audacity
```

## Flujo de trabajo

1. **Graba** una toma corta (10-20 s) **a capela**, sin pista de fondo, con volumen
   parejo. Guárdala en `grabaciones/` (mejor **.wav**).
   - Más fácil: grabador de Windows o Audacity → exporta WAV → cópialo a `grabaciones/`.
2. **Analiza**:
   ```bash
   python tools/analizar_voz.py grabaciones/mi_toma.wav
   ```
   Escribe `analisis/mi_toma.json` + `.md` e imprime un resumen (rango, tesitura,
   afinación, brillo).
3. **Coach**: me pasas el resumen (o el .md) y te interpreto: tu clasificación
   aproximada, en qué **tono** cantar, qué **canciones/géneros** te caen bien.
4. **Mapa de canción**: eliges canción → te devuelvo el mapa **palabra → nota** en
   tu tono (pico en A4–B4, no en C5) → lo sigues en **Vocal Pitch Monitor**.

## Privacidad

Repo privado. `grabaciones/` está en `.gitignore`: tu voz cruda **nunca** sale a
GitHub; solo el análisis numérico y los mapas.
