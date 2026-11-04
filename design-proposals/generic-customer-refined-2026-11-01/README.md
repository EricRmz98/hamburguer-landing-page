# Revisión sutil de proporciones del cliente genérico

Parte de la silueta trazada desde la referencia del usuario. Conserva el torso angosto, la cabeza ovalada sin rostro y la pose con un brazo colgando y el otro en la cintura.

Cambios respecto al calco anterior:

- Distancia entre hombros y cadera tres píxeles menor (aproximadamente un 5 %). La longitud de las piernas se conserva.
- Borde exterior del codo doblado suavizado hacia dentro menos de un píxel antes de discretizar.
- Ruido de la fotografía suavizado en contornos y sombras para mejorar la unión del cuello y las muñecas.
- Óvalo de la cabeza regularizado aproximadamente un píxel; su sombra queda en una franja lateral continua para evitar marcas que parezcan faciales.

El resultado mide 80 × 144 y usa tres colores de Endesga 32 con alfa binario. Se conserva como matriz de texto en `sprite.json`. La cadera se alinea con la barra en la fila 92 y los objetos de cocina mantienen su tamaño.

`refinement-comparison.png` muestra anterior, refinado y entorno horizontal. `reference-comparison.png` conserva la foto del usuario para comparar. También se incluyen las composiciones horizontal y vertical, el sprite transparente a escala nativa y ampliado, una composición con plato vacío y las comprobaciones de paleta, silueta conectada y tamaño en `checks.json`.

Se inspeccionaron visualmente el cuerpo completo y ambas composiciones. `generate.py` reproduce exclusivamente esta referencia. El juego activo y las propuestas anteriores permanecen sin cambios.
