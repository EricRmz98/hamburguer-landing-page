# Conjunto de preparación centrado · 3 de noviembre de 2026

La basura se redibuja a 42 × 25 píxeles nativos, con proporciones más cuadradas, la misma altura y el mismo ancho que la bandeja de carne. Conserva el borde ligeramente elevado y la sombra de contacto, sin un mueble metálico adicional.

Basura y carne comparten la coordenada superior. Ambas flanquean la plancha con huecos iguales: 4 píxeles en horizontal y 3 en vertical. El conjunto inferior y la plancha están centrados exactamente en el escenario y alineados con el centro del plato y de los ingredientes: x=160 en horizontal, x=90 en vertical. La fila del pan ya no sobresale del conjunto inferior. Los tres quemadores y sus áreas de toque se desplazan juntos.

La única matriz que cambia es la basura. Fondo, metal de la barra, alimentos, clientes, botes, plato, plancha y perillas conservan sus dibujos y la paleta Endesga64. Las posiciones usan celdas enteras; no hay reescalado de sprites.

161 pruebas y compilación correctas. `composicion/browser-checks.json` verifica alturas, centrado, márgenes iguales, pan contenido y tres quemadores activos en ambas vistas. `composicion-final.png` reúne capturas reales y `antes-despues.png` permite comparar. No se revisó en teléfono físico.
