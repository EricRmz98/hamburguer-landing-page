# Resurrect 64 · acabado común del minijuego

Aplicado al juego principal y a `/clientes-prueba`. El elenco nativo de doce personajes es la referencia artística: contorno selectivo, sombras agrupadas, detalle por material y la misma escala de píxel en toda la escena.

## Cambios

- Paleta oficial de 64 colores de **Kerrie Lake**, descargada de [Lospec](https://lospec.com/palette-list/resurrect-64). La descarga original está en `resurrect-64.source.json`; su copia de producción está en `scripts/sprites/resurrect-64.json`. `palette.ts` contiene exactamente estos valores, sin colores añadidos.
- Doce clientes de 96 × 120 integrados en producción desde `customers-native.json`. Se conserva cada celda y el alfa de los dibujos aprobados; únicamente cambia el color. Inés conserva su escala del 85 % y los perfiles siguen alternados. Cada variante tiene un retrato de espera; no se crearon expresiones adicionales.
- Comedor, puerta, ventanas, lámparas, asientos y barra en la paleta común. Se mantienen pared continua, barra blanca adosada, sillas giradas hacia el centro, apoyos y sombras de contacto. Costuras, luces de acolchado, esmalte rojo y pequeñas variaciones de pared y concreto. La textura ambiental se redujo después de la revisión visual para evitar que compitiera con los clientes.
- Alimentos con costra, ajonjolí, marcas de plancha, venas y semillas en grupos de píxeles. La misma comida se reutiliza en las bandejas. El plato tiene un borde interior; botes de salsas redibujados en celdas 2D con cuerpo suave, etiqueta y dos cuadros; plancha con manchas agrupadas en lugar de tramado uniforme.
- Comanda, cintas, ayudas, indicadores, botones y estados de la interfaz en Resurrect 64. Los colores de los ingredientes en la comanda se leen de la paleta común.
- Se conserva el encuadre y tamaño de todas las piezas de cocina y sus anclas; `anchors.ts` coincide exactamente con la copia anterior. `GameView` aplica una única escala entera a todo el atlas.

## Revisión y comprobaciones

- 161 pruebas pasan: reglas, paleta oficial exacta, importación sin pérdida de sus 64 colores, formato, materiales, atlas, anclajes y elenco nativo.
- Compilación correcta; las páginas de revisión siguen siendo exclusivas de desarrollo.
- 24 comprobaciones en el navegador (doce por orientación): el fondo del atlas del cliente tiene exactamente la misma escala que el de la pared; cada retrato mide 96 × 120 celdas lógicas.
- Revisión visual de las dos láminas completas de composición, de los doce clientes recoloreados, de los alimentos y de los cuatro estados de carne. Se conservan las excepciones documentadas de análisis de centroide para escenas y retratos con múltiples materiales; los otros controles de estilo continúan activos.
- Juego principal: arranque, colocar pan, poner carne, estado de cocción y pausa/reanudación, en escritorio y móvil simulado de 390 × 844. No se ha revisado en teléfono físico.

## Entregables de revisión

- `composicion-final.png`: composición horizontal y vertical reales.
- `antes-despues.png`: comparación con la versión anterior.
- `composicion/12-clientes-horizontal.jpg` y `12-clientes-vertical.jpg`: todos los clientes con la escena actual.
- `12-clientes-resurrect.png`: retratos en la paleta nueva.
- `cocina-detalle.png`: alimentos, utensilios y estados.
- `comedor.png`, `comedor_v.png`, `barra_roja.png`, `barra_roja_v.png`: entorno limpio, ampliado por vecino más cercano.
- `partida-real-horizontal.png`, `partida-real-vertical.png`: partida del minijuego principal.
- `before/`: copia de las definiciones de producción anteriores a esta renovación.
- `native-assets.json`: exportación de los sprites y variantes reales para revisar; `export.mjs` y `render.py` reproducen las láminas a partir del código y las capturas.

Los generadores de producción y sus instrucciones están en `scripts/sprites/README.md`. No dependen de esta carpeta de revisión para regenerar el juego.
