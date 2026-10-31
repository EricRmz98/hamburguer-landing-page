# Generadores de sprites

Los sprites del juego son texto (`src/game/sprites/`), pero los más complejos se generaron con estos
scripts de Python (solo biblioteca estándar). Sirven para regenerarlos o crear nuevos con el mismo estilo:
vista frontal elevada 3/4, paleta Endesga 32, luz desde la izquierda.

| Script | Qué hace |
| --- | --- |
| `r34.py` | Renderizador de vóxeles 3/4 (cámara a 32° de altura y girada 12°): sombreado por cara, sombra de contacto, contorno selectivo, texturas y limpieza de escalones. |
| `gen34.py` | Modelos 3D de la cocina (panes, carne, queso, lechuga, tomate, cebolla, salsa, plato, bote, charola con carne molida, basura, plancha y bandejas) y sus materiales; genera un JSON con filas, colores y anclas. Lo redondo usa la cámara girada 12°; plancha y bandejas, 0° para alinearse con la cuadrícula. Las bandejas de lechuga, tomate y cebolla se componen con los mismos sprites del plato (tabla `FILL`); pan y queso son pilas modeladas. |
| `write34.py` | Escribe `ingredients.ts`, `utensils.ts` y `anchors.ts` a partir de ese JSON, con las variantes de cada sprite. Los sprites nuevos se registran a mano en `src/game/sprites/index.ts`. |
| `people_gen.py` · `write_people.py` | Clientes (hombre y mujer) con sus expresiones y looks; escribe `people.ts`. |

Desde la raíz del proyecto:

```bash
python3 scripts/sprites/gen34.py /tmp/cocina34.json
python3 scripts/sprites/write34.py /tmp/cocina34.json
python3 scripts/sprites/write_people.py
pnpm test
```

`pnpm test` valida todos los sprites y revisa la guía de estilo. Revisar el resultado en `/sprites` con `pnpm dev`.
Los sprites generados se pueden retocar a mano después, pero volver a generar sobrescribe esos retoques.
