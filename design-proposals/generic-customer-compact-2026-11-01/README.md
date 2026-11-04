# Base compacta según la nueva referencia de figuras blancas

La figura de pie con los brazos relajados, segunda desde la izquierda, es la referencia principal por permitir comparar cabeza, torso, brazos y piernas sin el acortamiento aparente de poses sentadas o inclinadas. La imagen del usuario se conserva en `reference.png`; el recorte ampliado que aparece en la lámina no se estira en ninguno de los ejes.

El problema de la propuesta anterior estaba especialmente en la distancia excesiva entre los hombros y la cadera. Esta base reduce esa distancia y adopta una cabeza casi del ancho del torso. La cabeza ocupa 28 × 27 píxeles de relleno frente a 30 de ancho en el torso. El cuerpo completo tiene aproximadamente 4.4 alturas de cabeza contando el contorno. Estas son medidas de la propuesta, no mediciones anatómicas exactas de la fotografía.

Los brazos caen junto al cuerpo y terminan a la altura de la cadera. Se mantienen los laterales rectos en torso y piernas. Las piernas de la pose neutral son paralelas y su ancho total incluido el contorno queda dentro del torso; la pose de comprobación con piernas juntas mide 28 píxeles frente a 32 del torso.

El sprite nativo mide 80 × 136, usa tres colores de Endesga 32 y alfa binario. La cadera se alinea con la barra mediante el ancla de la fila 85. El escenario y los objetos de cocina mantienen su tamaño.

- `prototype-review.png`: recorte de la nueva referencia, base y contexto horizontal.
- `refinement-comparison.png`: propuesta anterior y nueva a la misma escala.
- `generic-customer-1x.png`, `generic-customer-6x.png`: sprite transparente y ampliado.
- `generic-customer-legs-together-1x.png`: pose de comprobación de ancho.
- `prototype-horizontal.png`, `prototype-vertical.png`, `prototype-empty-plate.png`: composiciones en el entorno.
- `sprite.json`: definición como matriz de texto.
- `checks.json`: medidas y validación de paleta, alfa y silueta conectada.

Se revisaron visualmente la comparación con el recorte y las composiciones horizontal y vertical. `generate.py` reproduce exclusivamente esta propuesta. Se conservan las iteraciones anteriores y no se reemplazan los clientes del juego.
