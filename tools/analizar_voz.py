# -*- coding: utf-8 -*-
"""Analiza una grabación de voz: rango, tesitura, estabilidad de afinación y brillo.

Uso:
    python tools/analizar_voz.py grabaciones/mi_toma.wav

Escribe  analisis/<nombre>.json  +  analisis/<nombre>.md  e imprime un resumen.

Notas:
- Graba A CAPELA (sin pista de fondo) y con volumen parejo. 10-20 s basta.
- .wav no necesita nada extra; .m4a/.mp3 requieren ffmpeg instalado.
- El rango/tesitura/afinación se miden bien. El "brillo" (timbre) es un proxy
  crudo: para género/color fino, mejor el oído de un humano.
"""

import sys
import json
from pathlib import Path

import numpy as np
import librosa
from scipy.signal import medfilt

# Piso en G2 (~98 Hz): bien por debajo de cualquier grave real de voz femenina,
# pero alto como para que pyin no invente subarmónicos (octava abajo falsa).
FMIN = librosa.note_to_hz("G2")   # ~98 Hz
FMAX = librosa.note_to_hz("C6")   # ~1047 Hz


def _nota(hz):
    return librosa.hz_to_note(float(hz), unicode=False)


def analizar(path):
    y, sr = librosa.load(path, sr=22050, mono=True)
    f0, _, _ = librosa.pyin(y, fmin=FMIN, fmax=FMAX, sr=sr)
    f0v = f0[~np.isnan(f0)]
    if f0v.size < 20:
        raise SystemExit(
            "No detecté voz cantada clara. ¿Grabaste a capela, con volumen y sin "
            "pista de fondo?"
        )

    # Filtro de mediana sobre las notas (en MIDI): mata saltos de octava aislados.
    midiv = medfilt(librosa.hz_to_midi(f0v), kernel_size=5)
    f0v = librosa.midi_to_hz(midiv)

    # Rango robusto (2-98 percentil): ignora picos sueltos en los extremos.
    lo, hi = np.percentile(f0v, 2), np.percentile(f0v, 98)
    median = np.median(f0v)
    t_lo, t_hi = np.percentile(f0v, 10), np.percentile(f0v, 90)  # tesitura cómoda

    # estabilidad: desviación (en cents) respecto a la nota más cercana
    midi = librosa.hz_to_midi(f0v)
    cents = (midi - np.round(midi)) * 100.0
    estabilidad = float(np.std(cents))

    # brillo: centroide espectral medio (proxy crudo de timbre)
    centroide = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))

    return {
        "archivo": Path(path).name,
        "rango": {
            "min": _nota(lo),
            "max": _nota(hi),
            "semitonos": round(12 * np.log2(hi / lo), 1),
        },
        "centro": _nota(median),
        "tesitura_comoda": {"min": _nota(t_lo), "max": _nota(t_hi)},
        "afinacion_desviacion_cents": round(estabilidad, 1),
        "brillo_centroide_hz": round(centroide, 0),
    }


def sugerencias(r):
    """Heurísticas orientativas a partir del centro de tesitura."""
    centro_midi = librosa.note_to_midi(r["centro"])
    a3, e4, a4 = librosa.note_to_midi("A3"), librosa.note_to_midi("E4"), librosa.note_to_midi("A4")
    if centro_midi < a3:
        clasif = "contralto / voz grave"
    elif centro_midi < e4:
        clasif = "mezzo / alto (medio-grave)"
    elif centro_midi < a4:
        clasif = "mezzo-soprano / medio"
    else:
        clasif = "soprano / voz aguda"

    afin = r["afinacion_desviacion_cents"]
    if afin < 25:
        nota_afin = "muy estable (afinas centrado)"
    elif afin < 45:
        nota_afin = "estable con derivas leves"
    else:
        nota_afin = "inestable: trabajar puntería de tono (graba y compara con VPM)"

    return {
        "clasificacion_aprox": clasif,
        "regla_tono": "Transpón cada canción para que su nota MÁS ALTA caiga en A4–B4 "
                      "(no en C5, tu zona roja).",
        "afinacion": nota_afin,
        "genero_orientativo": "ORIENTATIVO (timbre por máquina es crudo): una tesitura "
                              "medio-grave suele caer bien en balada/bolero, pop medio, "
                              "indie/folk, soul/R&B de pecho. Lo confirmamos con tu oído.",
    }


def to_md(r, s):
    return f"""# Análisis · {r['archivo']}

- **Rango:** {r['rango']['min']} → {r['rango']['max']}  ({r['rango']['semitonos']} semitonos)
- **Centro de tesitura:** {r['centro']}
- **Tesitura cómoda (donde de verdad cantas):** {r['tesitura_comoda']['min']} → {r['tesitura_comoda']['max']}
- **Afinación (desviación):** {r['afinacion_desviacion_cents']} cents — {s['afinacion']}
- **Brillo (centroide):** {r['brillo_centroide_hz']} Hz

## Coach
- **Clasificación aprox.:** {s['clasificacion_aprox']}
- **Regla de tono:** {s['regla_tono']}
- **Género (orientativo):** {s['genero_orientativo']}
"""


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python tools/analizar_voz.py grabaciones/mi_toma.wav")
    path = sys.argv[1]
    r = analizar(path)
    s = sugerencias(r)

    out = Path(__file__).resolve().parent.parent / "analisis"
    out.mkdir(exist_ok=True)
    stem = Path(path).stem
    (out / f"{stem}.json").write_text(json.dumps({**r, "coach": s}, indent=2, ensure_ascii=False))
    (out / f"{stem}.md").write_text(to_md(r, s), encoding="utf-8")

    print(to_md(r, s))
    print(f"-> analisis/{stem}.json  +  analisis/{stem}.md")


if __name__ == "__main__":
    main()
