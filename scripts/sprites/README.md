# Generadores de sprites

Los sprites del juego son texto (`src/game/sprites/`), pero los más complejos se generaron con estos
scripts de Python (biblioteca estándar salvo el generador de entorno, que usa Pillow). Sirven para regenerarlos o crear nuevos con el mismo estilo:
vista frontal elevada 3/4, paleta Endesga 64, luz desde la izquierda.

| Script | Qué hace |
| --- | --- |
| `r34.py` | Renderizador de vóxeles 3/4 (cámara a 32° de altura y girada 12°): sombreado por cara, sombra de contacto, contorno selectivo, texturas y limpieza de escalones. |
| `gen34.py` | Modelos 3D de la cocina (panes, carne, queso, lechuga, tomate, cebolla, salsa, plato, bote, charola con carne molida, basura, plancha y bandejas) y sus materiales; genera un JSON con filas, colores y anclas. Lo redondo usa la cámara girada 12°; plancha y bandejas, 0° para alinearse con la cuadrícula. Las bandejas de lechuga, tomate y cebolla se componen con los mismos sprites del plato (tabla `FILL`); pan y queso son pilas modeladas. |
| `write34.py` | Escribe `ingredients.ts`, `utensils.ts` y `anchors.ts` a partir de ese JSON, con las variantes de cada sprite. Los sprites nuevos se registran a mano en `src/game/sprites/index.ts`. |
| `customers-native.json` · `customers_gen.py` · `write_people.py` | Los 12 clientes nativos aprobados, con sus poses y orientaciones alternadas; escribe `people.ts`. |
| `people_gen.py` | Generador histórico de los clientes anteriores. Se conserva como dependencia de las propuestas archivadas; ya no escribe los clientes del juego. |

Desde la raíz del proyecto:

```bash
python3 scripts/sprites/gen34.py /tmp/cocina34.json
python3 scripts/sprites/write34.py /tmp/cocina34.json
python3 scripts/sprites/write_people.py
pnpm test
```

`pnpm test` valida todos los sprites y revisa la guía de estilo. Revisar el resultado en `/sprites` con `pnpm dev`.
Los sprites generados se pueden retocar a mano después, pero volver a generar sobrescribe esos retoques.

## Clientes aprobados

La fuente de producción es `customers-native.json`, independiente de `design-proposals/` y de Pillow. Contiene los doce retratos de 96 × 120, sus matrices, paletas por personaje, nombres, estilos, orientaciones y firmas SHA-256 del dibujo en Endesga 64. Se conserva un cuadro de espera por personaje; no se inventaron expresiones adicionales sobre las caras aprobadas. `write_people.py` regenera el módulo de producción desde esa fuente.

En el atlas aparecen como `cliente:lia`, `cliente:bruno`, etc. `CUSTOMERS` contiene los doce y `CUSTOMER_PROFILES` sus nombres, estilos y orientación. Se muestran a escala nativa (96 × 120), igual que el entorno; toda la escena crece con una escala entera común. La cintura está en la fila 114. Inés conserva su escala reducida al 85 %, y los perfiles alternan seis a izquierda/seis a derecha. La excepción del centroide de luz es explícita por los múltiples materiales; se mantienen las comprobaciones de paleta y formato.

`customers-approved.json` conserva el elenco anterior de 24 personajes como archivo histórico. `import_approved_native.mjs` es la importación inicial de la última propuesta aprobada: convierte exclusivamente los colores desde los PNG/matrices de revisión, sin cambiar celdas, proporciones ni alfa; no es necesario ejecutarlo para regenerar el juego.

## Paleta común

`src/game/sprites/palette.ts` contiene exactamente los 64 colores de [Endesga 64, de ENDESGA](https://lospec.com/palette-list/endesga-64), en su orden oficial. `endesga-64.json` conserva la descarga oficial que usan las pruebas para verificar la paleta. Las rampas distinguen pan tostado, carne, verduras, cerámica, acero y esmalte rojo. Los colores de la comanda se leen de la misma fuente.

El acabado sigue los clientes: contornos selectivos, sombras en grupos de píxeles, variación de material sin ruido general. El pan tiene costra y ajonjolí, la carne marcas de plancha, la lechuga venas, el tomate semillas; esos mismos ingredientes se reutilizan en las bandejas. Los botes tienen contorno 2D redondeado y dos cuadros (normal/apretado) dibujados en celdas nativas. Se conservan las dimensiones y anclas de los ingredientes; los ajustes del plato y la basura se describen abajo.

## Entorno del comedor

`counter_gen.py` dibuja los dos maestros de la barra directamente en la cuadrícula final: cerámica roja con profundidad de vidriado, reflejos agrupados, juntas ortogonales y encimera de acero cepillado. Se ejecuta antes de `environment_gen.py`; no modifica el comedor aprobado. Los maestros PNG siguen siendo editables.

`environment-native/` contiene los cuatro maestros PNG editables en resolución final: `comedor` (320 × 122), `comedor_v` (180 × 200), `barra_roja` (320 × 90) y `barra_roja_v` (180 × 100). Cada celda corresponde a un píxel del juego, con un único color oficial y sin transparencia. `environment_gen.py` comprueba tamaños y colores y los convierte a `src/game/sprites/environment.ts`, sin interpolación ni reescalado.

El diseño sigue la caricatura de proporciones creíbles de los clientes: marcos finos de acero rojo oscuro, cristal, yeso neutro, concreto pulido, barra blanca y asientos tapizados con costuras. La barra del jugador conserva cerámica roja con juntas rectas y canto de acero. Cada orientación tiene composición propia; los maestros y las matrices comparten exactamente la escala del atlas de clientes y cocina.

```sh
python3 scripts/sprites/environment_gen.py  # requiere Pillow
npm test
```

Las referencias, los prompts de generación, la conversión inicial a la cuadrícula y las capturas de los doce clientes en ambas orientaciones se conservan en `design-proposals/endesga64-unified-2026-11-03/`. La regeneración de producción solo necesita los maestros nativos y `palette.ts`, sin depender de esas referencias. La excepción del centroide global de luz es explícita para escenas compuestas; no desactiva la validación de tamaños, colores ni materiales.

## Detalle de cocina · 3 de noviembre

`gen34.py` aplica texturas por material sin cambiar siluetas ni anclas: miga porosa y costra tostada, sellado de carne, pliegues suaves del queso, nervaduras y pliegues de lechuga, cámaras de pulpa y semillas de tomate, anillos de cebolla y reflejos de salsa espesa. Los mismos materiales se reutilizan en las bandejas, con coordenadas locales para que la luz sea coherente. Los frentes de acero tienen bandas de reflexión y un lado en sombra; las planchas usan tres zonas de cocción desde el inicio.

La revisión `design-proposals/kitchen-detail-2026-11-03/` incluye comparación visual, cocina ampliada y comprobaciones de dimensiones, siluetas, anclas y fondo sin cambios. Las rampas amplían únicamente los tonos oficiales Endesga64 que necesita cada material.

## Plato, salsas y espacio de trabajo

Los botes son 16 × 42, con ancla 8/38 y sin etiquetas: vista frontal elevada con hombro superior ovalado, tapa ovalada baja y boquilla fina alargada, reflejo curvo, base redondeada y sombra corta sobre la encimera. Los dos cuadros nativos (normal/apretado) comparten apoyo y boquilla. Sus zonas de interacción se ajustan al nuevo tamaño en ambas orientaciones y mantienen dos celdas de separación. La basura es una abertura de 42 × 25, con un labio ligeramente elevado, con boca capaz de recibir una carne completa; usa el mismo sprite nativo en ambas orientaciones. El plato pasa a 38 × 22 (radio 19, ancla 19/11), con mayor margen alrededor del pan.

La escena horizontal mide 320 × 212 y la vertical 180 × 300. La pared y el cliente conservan sus posiciones; la barra crece hacia abajo a 320 × 90 y 180 × 100. `counter_gen.py` dibuja la superficie de trabajo a 28 y 36 filas nativas respectivamente. Las bandejas, la plancha y sus áreas de interacción se desplazan juntas, y plato y salsas tienen margen en la encimera; la basura está a la izquierda de la plancha, del lado de preparación. Se conserva una sola escala entera del atlas. Revisión del espacio en `design-proposals/mobile-worktop-2026-11-03/`; composición final con los salseros aprobados en `design-proposals/sauce-dispensers-2026-11-03/`.

## Acero, tres quemadores y borde elevado

`counter_gen.py` dibuja reflejos continuos de acero cepillado, con bandas de luz y variación alargada del grano cuantizadas directamente a Endesga64. No hay un módulo metálico adicional alrededor de la basura: solo su aro elevado y su sombra de contacto.

Las planchas nativas miden 118 × 35 (horizontal) y 90 × 35 (vertical), con tres controles circulares de 7 × 7 dibujados en celdas nativas. La cara frontal se sombrea bajo el borde de acero. Las carnes y los indicadores se sitúan encima de los controles para no ocultarlos. `DEFAULT_CONFIG` tiene capacidad máxima de tres, y todos sus niveles mantienen los tres lugares disponibles desde el primer cliente, incluido el modo infinito. La progresión de recetas y paciencia se conserva.

Capturas y comprobación de tres carnes simultáneas en `design-proposals/steel-three-burners-2026-11-03/`.

## Balance del conjunto de preparación

La basura mide 42 × 25, igual que la charola de carne, y ambas se apoyan a la misma altura. La plancha se centra en x=160 (horizontal) y x=90 (vertical), en el mismo eje del plato y del riel de ingredientes. Los huecos laterales son iguales: 4 y 3 píxeles respectivamente. El conjunto inferior también está centrado y cubre los límites de la fila del pan. Solo se redibuja la basura; las demás matrices se conservan. Verificación visual en `design-proposals/balanced-prep-2026-11-03/`.

`native_waste` añade facetas y pliegues a la bolsa interior sobre la rampa `plastico-negro`, con tonos existentes en Endesga64. Se conservan todas las posiciones, dimensiones y siluetas. Esa revisión se conserva en `design-proposals/bright-steel-liner-2026-11-03/`.

El acabado vigente de la barra toma como referencia la placa inferior de la puerta y el frontal de la plancha: base gris azulada, reflejos estrechos en gris claro y plata y cantos sombreados. El cepillado solo modula las zonas de reflejo. Se conserva el resto de las matrices, incluida la bolsa interior. Comparación y capturas en `design-proposals/matched-steel-2026-11-03/`.
