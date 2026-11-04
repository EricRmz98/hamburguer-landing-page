# Adaptación de los 12 nuevos clientes a la cuadrícula del minijuego

**Versión anterior:** su escala del 150 % no comparte el mismo tamaño de píxel que el entorno. La corrección nativa de 96 × 120 está en `../customers-native-96x120-2026-11-03/` y es la que ahora carga `/clientes-prueba`.

Los diseños de partida son los PNG seleccionados de `customers-new-cast-12-2026-11-01`. Esta adaptación los convierte a matrices nativas de 64 × 80, con transparencia binaria y únicamente colores existentes de Endesga 32. Las imágenes grandes se conservan como referencia; los nuevos sprites no son ilustraciones grandes disimuladas con CSS.

## Encuadre y acabado

Cada personaje tiene un punto de cintura marcado en la referencia. Se usa una sola escala para ambos ejes, encuadrando la parte visible detrás de la barra y conservando proporciones. Se deja margen superior mínimo de cinco píxeles. Algunas figuras quedan ligeramente más bajas por su silueta más ancha, conservando la variedad del diseño.

La cintura corresponde a la fila 76. Con los layouts actuales y escala del 150 %, esto coincide exactamente con el borde de la barra: horizontal `8 + 76 × 1.5 = 122`; vertical `86 + 76 × 1.5 = 200`. Los clientes ocupan 96 × 120 en ambas orientaciones.

La reducción agrupa colores cercanos, limita cada personaje a un máximo de 16 colores de la paleta global y preserva los pequeños brillos blancos. Las zonas cálidas de las caras se reducen a una rampa de piel para eliminar manchas naranjas; el bomber oliva de Sasha se conserva en la familia verde. Se limpian píxeles aislados de tono parecido, manteniendo contrastes de ojos, accesorios y contornos. No se aplica dithering. Todas las ampliaciones para revisar usan vecino más cercano.

## Entregables

- `12-clientes-cuadricula.png`: los doce sprites nativos ampliados para revisión.
- `clientes-01-06-detalle.png`, `clientes-07-12-detalle.png`: detalle en dos láminas.
- `clientes-tamano-juego.png`: los doce a 96 × 120.
- `prueba-en-entorno.png`: seis ejemplos con la cocina y la barra actuales.
- `prueba-vertical.png`: ejemplo en la composición vertical.
- `individuales/`: doce PNG transparentes de 64 × 80.
- `ampliados/`: doce vistas a seis veces el tamaño nativo.
- `plantilla-64x80-transparente.png`: cuadrícula de cuatro columnas y tres filas; celdas de 64 × 80.
- Archivos `.ts` por personaje y `customers.ts`: definiciones nativas importables y lista del elenco.
- `sprite-definitions.json`: las mismas matrices en JSON.
- `12-clientes-adaptados.zip`: PNG, matrices, definición conjunta y lámina.

## Comprobación

`convert.mjs` utiliza `imageToSprite`, `defineSprite`, `validateSprite`, `rasterize` y `buildAtlas` del proyecto. Los doce módulos TypeScript se importaron directamente. Las matrices usan únicamente colores existentes y se rasterizan exactamente como los PNG; la copia al atlas junto a los sprites activos conserva todos los píxeles. Se comprueban los anclajes y tamaños en ambos layouts.

El análisis del centroide de luz global produce avisos por cabello oscuro sobre prendas claras. Como en los clientes activos, se declara una excepción justificada de esa única comprobación: la luz de las distintas piezas se revisa visualmente y se conservan los demás controles. Los avisos originales quedan registrados en `engine-checks.json`; no se falsean recoloreando la ropa para satisfacer un promedio global.

Se inspeccionaron visualmente las doce figuras ampliadas, la hoja al tamaño de juego y las pruebas con el entorno. `prepare.py`, `convert.mjs` y `render.py` reproducen la adaptación, las validaciones y las láminas. `manifest.json` registra recortes, escala, posición, cintura y colores por personaje.

Esta entrega prepara el cuadro de espera de cada personaje para revisar la adaptación. No dibuja expresiones adicionales ni sustituye todavía el elenco activo. Ningún archivo de producción fue modificado en esta fase.
