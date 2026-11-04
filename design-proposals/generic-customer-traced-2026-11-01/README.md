# Cliente genérico trazado desde la referencia

Esta propuesta sustituye la interpretación de anatomía por una extracción directa de la silueta de la fotografía proporcionada por el usuario. La figura blanca se separa del fondo rojo por su color neutro y se conserva el componente conectado que contiene su torso. Se mantienen el contorno exterior y el espacio entre el brazo doblado y el torso.

La transformación es uniforme (0.27 en ambos ejes). No se ensanchan hombros, pecho, cabeza ni extremidades. El resultado se discretiza en una cuadrícula de 80 × 148 píxeles con alfa binario. Las sombras originales se reducen a blanco y gris claro de Endesga 32, con un contorno gris azul de un píxel. Esa discretización y el contorno son las diferencias inevitables respecto al contorno fotográfico.

La propuesta incluye el cuerpo completo para comparar directamente las proporciones. En las composiciones del juego se recorta en la cadera, fila 95, y se alinea con la barra. El brazo colgante termina justo encima de ella.

- `reference-comparison.png`: fotografía original, sprite completo y contexto horizontal.
- `prototype-review.png`: revisión del sprite, contexto y comparación con el plato.
- `generic-customer-1x.png` y `generic-customer-6x.png`: sprite transparente y ampliado.
- `prototype-horizontal.png` y `prototype-vertical.png`: composiciones con la cocina actual.
- `prototype-empty-plate.png`: contexto con plato vacío.
- `sprite.json`: matriz de texto, paleta y ancla de cadera.
- `checks.json`: verificación de paleta, alfa, conectividad y proporción con el plato.
- `reference.png`: imagen del usuario utilizada como fuente reproducible.
- `scene-source.json`: instantánea de los objetos y posiciones del escenario.

`generate.py` reproduce solo esta propuesta. Las versiones previas permanecen en sus carpetas. No se modifica el juego activo.
