# canto

**Coach de canto por sesiones.** Una canción por archivo en `canciones/`.

## Cómo trabajamos

1. **Tú me dices la canción.**
2. Elijo el **tono** (que la nota más alta caiga en **A4–B4, nunca C5**) y armo el mapa en `canciones/<cancion>.md` con el formato de abajo.
3. Practicas con **Vocal Pitch Monitor (VPM)**, me cuentas cómo te fue, y **registramos el avance** en el mismo archivo, sesión por sesión.

## Tu voz (referencia rápida)

- Mezzo/alto medio-grave. **Zona verde cómoda: G3 → A4** · centro **B3/C4**.
- **C5 = zona roja** (la garganta se cierra). Techo útil para picos: **A4–B4**.
- **Constricción:** la garganta se cierra al empujar/subir → **calentar SIEMPRE con SOVT** (trino de labios / popote) y **soltar, no forzar**. Nunca cantar con dolor.
- Afinación: deriva ~30 cents → puntería de tono con VPM (apuntar al centro de la barra).
- **Regla de tono:** transponer cada canción para que su pico quede en **A4–B4, no en C5**.

## Formato de cada canción (plantilla)

Cada `canciones/<cancion>.md` va así:

1. **Encabezado:** título · tono elegido · rango de la estrofa · aviso "el contorno es fiel; los nombres de nota son guía de altura en tu tono → confirmar con la grabación original en VPM".
2. **🔥 CALENTAMIENTO (con VPM)** — arriba, se repite cada sesión. Siempre **SOVT primero**. Suele llevar 6 pasos: 1) SOVT trino/popote (glissando por el rango), 2) ancla en la nota-casa (tónica), 3) salto al pico (en "u" → "a"), 4) escalera de vocales sin cerrar, 5) desensibilizar la "i", 6) messa di voce. Cada paso con su **🔎 VPM:** qué mirar.
3. **📅 SESIONES** — abajo, una por bloque de trabajo: `## Sesión N — fecha · tema`. Cada sesión lleva, **en este orden**:
   - **🎯 Avance / ✅ Logrado** (qué se trabajó / qué ya sale).
   - **🎚️ Dinámica de la estrofa** (el arco p→mf→dim) — **hasta arriba**.
   - **Notas por palabra/frase** — una **tabla por frase** con 3 filas: **flechas arriba** (la de encima de una sílaba = a dónde va esa nota; la del hueco entre palabras = transición a la siguiente) · **sílabas** · **notas**. Una nota por columna, **columna vacía entre palabras**, picos (A4/A3) en negrita. Flechas de texto: ↑ sube mucho · ↗ sube · → se mantiene · ↘ baja · ↓ baja mucho.
   - **Letra** (justo debajo de la tabla).
   - **Recordatorios de técnica** (vocales recomendadas · brillo · intensidad).
   - **Para la próxima** (qué practicar / si subir de tono).

> Las tablas y diagramas se generan con scripts (en el scratchpad) para que las columnas y flechas cuadren; cualquier canción nueva se arma igual.

## Estructura

```
canto/
├── README.md      # esto (workflow + tu voz + formato)
└── canciones/     # un .md por canción: calentamiento + bitácora por sesión
    └── sabor-a-mi.md
```

> Los audios que practiques se quedan en tu equipo (`grabaciones/` está en `.gitignore`); aquí solo viven los mapas y el avance escrito.
