# Proporción de los clientes respecto al plato

Los clientes aprobados se muestran 50 % más grandes en el juego: 96 × 120 sobre su matriz original de 64 × 80. Se mantiene la proporción de ancho y alto y la cintura en el borde de la barra. La cocina conserva su tamaño. El indicador de paciencia se desplaza por encima de las cabezas.

La vista adapta la escala del recorte del atlas al rectángulo de cliente de cada disposición. Las matrices aprobadas, las expresiones y las poses no cambian. Se conserva `image-rendering: pixelated`.

- `desktop.png`: nueva composición horizontal con Vale.
- `mobile.png`: la misma pose de saludo en la vista vertical, simulada a 390 × 844.

También se revisó la composición a 1024 × 768 con Sam y la pose de Nico en el tutorial. Las 160 pruebas y la compilación pasaron. El control de diseño verifica escala uniforme, centrado, cintura anclada a la barra y separación del indicador de paciencia. No se probó en un teléfono físico.
