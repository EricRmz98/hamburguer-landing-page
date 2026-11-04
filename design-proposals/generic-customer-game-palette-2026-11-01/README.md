# Modelo seleccionado adaptado a la paleta y cuadrícula del juego

La fuente es `approved-source.png`, copia de la última imagen generada que el usuario señaló como mucho mejor. Se conserva su anatomía y pose. La adaptación consiste en eliminar transparencia residual fuera del cuerpo, reducir uniformemente su tamaño y convertir su iluminación cálida a la rampa blanca/gris del juego. No se regenera ni se redibuja la silueta.

## Compatibilidad comprobada

- Cuerpo completo: 64 × 118 píxeles; figura de 110 píxeles de alto más márgenes.
- Recorte para la barra: 64 × 80 píxeles, exactamente el tamaño nativo de los clientes actuales.
- Ancla de cintura en la fila 76: con la escala vigente de 1.5, coincide con la barra en horizontal (`8 + 76 × 1.5 = 122`) y vertical (`86 + 76 × 1.5 = 200`).
- Cuatro colores existentes de Endesga 32: `blanco`, `gris-claro`, `gris`, `gris-azul`.
- Alfa binario; sin suavizado al ampliar.
- Definiciones de texto cargables mediante `defineSprite` y el importador oficial `imageToSprite`.
- `validateSprite` y `lintSprite` pasan sin excepciones.
- La rasterización y la copia en el atlas junto a todos los sprites activos conservan exactamente los píxeles del PNG convertido.

## Archivos

- `palette-review.png`: sprite completo y prueba horizontal con la disposición y escala actuales.
- `context-horizontal.png`, `context-vertical.png`: composiciones del entorno en ambas orientaciones.
- `customer-full-1x.png`, `customer-full-6x.png`: modelo completo.
- `customer-counter-1x.png`, `customer-counter-6x.png`: recorte para la barra.
- `customer-full.ts`, `customer-counter.ts`: definiciones nativas listas para importar; todavía fuera del registro activo.
- `customer-full.json`, `customer-counter.json`: las mismas definiciones en JSON.
- `engine-checks.json`, `import-metadata.json`: validaciones y datos de la conversión.

`prepare.py` prepara la cuadrícula y reduce los tonos a la rampa neutral de la paleta; `convert.mjs` utiliza el importador del proyecto y verifica el motor; `render.py` reproduce las composiciones con los sprites y layouts actuales. `palette.json` refleja `src/game/sprites/palette.ts`.

Esta es una adaptación de referencia lista como base de cliente, con un cuadro y sin rostro ni reacciones dibujadas. No se reemplazó el elenco de 24 clientes ni se modificó el juego activo. La integración posterior consistirá en registrar la definición y asignarla al cliente; la cuadrícula y las posiciones actuales son compatibles.
