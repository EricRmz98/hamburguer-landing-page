# Cliente genérico con torso y extremidades más rectos

Revisión solicitada para eliminar el contorno abultado de las piernas y enderezar el torso y los brazos. Conserva la pose de la referencia del usuario y la cabeza ovalada de la propuesta anterior.

La construcción se realiza directamente con máscaras geométricas y se exporta como matriz de texto. El torso tiene laterales verticales paralelos: 30 píxeles de relleno y 32 contando el contorno. Los brazos siguen segmentos rectos sin separaciones transversales en codos. Las piernas se dibujan con bordes paralelos de grosor uniforme y extremos suavizados, sin ensanchar pantorrillas ni pies. La unión a la cadera mantiene el ancho del torso.

Se incluye una segunda pose exclusivamente de comprobación con las piernas juntas. Su ancho máximo entre las filas 106 y 135, incluido el contorno, es de 26 píxeles, inferior a los 32 del torso. Esta comparación no cuenta el espacio entre las piernas de la pose abierta.

Se conserva la cuadrícula de 80 × 144, el ancla de cadera en la fila 92, la paleta Endesga 32 de tres colores y el alfa binario. Las composiciones mantienen las escalas originales de la cocina y los utensilios.

- `refinement-comparison.png`: anterior, nuevo, entorno y comprobación de piernas juntas.
- `reference-comparison.png`: referencia del usuario, nuevo sprite y entorno.
- `generic-customer-1x.png` y `generic-customer-6x.png`: sprite transparente y ampliado.
- `generic-customer-legs-together-1x.png`: pose para comprobar el ancho.
- `prototype-horizontal.png`, `prototype-vertical.png`, `prototype-empty-plate.png`: contexto en el juego.
- `sprite.json`: matriz de texto del sprite propuesto.
- `checks.json`: comprobaciones de paleta, alfa, silueta conectada y proporciones.

Se inspeccionaron visualmente ambas poses y la composición. `generate.py` reproduce únicamente esta propuesta; conserva las referencias previas y no cambia el juego activo.
