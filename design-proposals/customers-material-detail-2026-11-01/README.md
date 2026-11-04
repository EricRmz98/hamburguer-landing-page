# Prueba de acabado y materiales de los 24 clientes

El usuario señaló que los clientes estaban más planos y simples que los utensilios y la comida del juego. Esta propuesta trabaja sobre las matrices aprobadas de 64 × 80 para acercar el acabado mediante pequeños bloques de luz y sombra, pliegues, costuras y detalles de material. No se utiliza un filtro de ruido ni dithering.

El acabado depende de cada prenda: reflejos interrumpidos y paneles en chaquetas oscuras; ribetes y pequeños detalles de tejido en camisetas deportivas; cuadros más definidos en la camisa grunge; puntadas y desgaste moderado en lona/sarga; bloques de brillo en prendas técnicas; pequeñas líneas de mechones dentro del cabello. El gorro tejido y algunas gorras también reciben detalles específicos.

Se conservan la paleta Endesga 32, las dimensiones, las poses y cada píxel de la silueta. Las regiones de expresión facial y los píxeles de piel base se protegen. Las tres expresiones se reconstruyen con los parches originales; las caras coinciden con las originales en todos los cuadros. La escala continúa siendo 150 % en el juego (96 × 120).

## Para revisar

- `antes-despues.png`: comparación de seis personajes con distintos materiales.
- `clientes-detalle-todos.png`: los 24 con el nuevo acabado.
- `clientes-detalle-01-12.png`, `clientes-detalle-13-24.png`: revisión ampliada en dos hojas.
- `contexto-antes-despues.png`: Nico, Dani y Ari junto a los utensilios y el entorno, antes y propuesta.
- `clientes-escala-juego.png`: los 24 al tamaño del juego.
- PNG individuales numerados: las matrices propuestas a escala nativa.

`source-cast.json` conserva el elenco de partida; `proposal-cast.json` contiene la propuesta editable; `native-sprite.json` guarda la definición completa con las tres expresiones, comprobada con el motor. `checks.json` registra los cambios y la conservación de siluetas, caras y piel base. `engine-checks.json` registra las comprobaciones de formato, paleta y copia al atlas.

`generate.py` reproduce las imágenes y la propuesta. `render-context.py` monta la comparación de contexto usando los mismos sprites y posiciones de la cocina. Se inspeccionaron las hojas ampliadas, la vista al tamaño del juego y la comparación en el entorno.

Esta propuesta es únicamente para revisión. El juego sigue utilizando los clientes aprobados; no se modificaron los archivos de producción ni el elenco original.
