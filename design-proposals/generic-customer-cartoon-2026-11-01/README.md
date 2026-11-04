# Cliente genérico: revisión cartoon frontal

Revisión de la prueba anterior a partir de la segunda referencia frontal del usuario. Conserva la figura blanca sin rostro, orejas, peinado, ropa ni accesorios. El torso se compacta y la altura nativa pasa de 112 a 96 píxeles. El brazo izquierdo de la imagen cae relajado y el derecho se abre con la mano apoyada en la cintura. Las curvas de los brazos son continuas, sin divisiones en los codos.

El sombreado utiliza dos rellenos planos (blanco y gris claro) con un contorno gris azul. No hay degradados ni bandas de brillo cilíndrico. Se mantiene la paleta Endesga 32, alfa binario y ampliación sin suavizado.

La cintura está en la fila 92 y se alinea con el borde de la barra en ambas disposiciones. La figura se coloca a escala nativa respecto al escenario: el ancho con brazos a la altura del codo es de 70 píxeles frente a los 31 del plato. Esa medida incluye los brazos; no describe el ancho del torso.

## Entregables

- `prototype-review.png`: lámina de revisión con el sprite y su composición horizontal.
- `generic-customer-1x.png`: sprite transparente de 80 × 96.
- `generic-customer-6x.png`: ampliación de 480 × 576.
- `prototype-horizontal.png` y `prototype-vertical.png`: contexto con los objetos actuales del juego.
- `prototype-empty-plate.png`: contexto con el plato vacío.
- `sprite.json`: matriz de píxeles, paleta y ancla de cintura.
- `checks.json`: verificaciones de paleta, alfa, conectividad y proporción.
- `scene-source.json`: instantánea de los elementos del escenario utilizada para comparar escala.

`generate.py` reproduce únicamente esta propuesta. Se inspeccionaron visualmente la silueta, los hombros, los codos, la conexión de la mano a la cintura y las composiciones horizontal y vertical. La propuesta anterior se conserva en su carpeta. Esta revisión no modifica los clientes activos ni el código del juego.
