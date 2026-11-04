# Prueba de cliente genérico

Un único personaje de prueba inspirado en las figuras blancas y redondeadas de la imagen del usuario: cabeza ovalada sin rostro ni orejas, cuello corto, hombros continuos y brazos relajados sin separación entre brazo y antebrazo. No tiene peinado, ropa, accesorios ni rasgos de identidad.

Se dibuja directamente sobre la cuadrícula de píxeles con cuatro colores de Endesga 32 y alfa binario. El volumen se resuelve con bloques de luz y sombra, siguiendo la iluminación superior izquierda de los utensilios. El sprite nativo mide 80 × 112; se presenta sin ampliación adicional respecto a los objetos del escenario. Su cintura queda en la fila 108, apoyada en la barra. El ancho del torso con brazos se compara con el plato real de 31 píxeles.

## Archivos

- `prototype-review.png`: personaje ampliado y composición horizontal con la hamburguesa.
- `generic-customer-1x.png`: sprite nativo con fondo transparente.
- `generic-customer-6x.png`: ampliación sin suavizado para inspección.
- `prototype-horizontal.png`, `prototype-vertical.png`: composiciones usando el escenario y los objetos activos del juego.
- `prototype-empty-plate.png`: comparación de tamaño con el plato vacío.
- `sprite.json`: matriz de texto y paleta, preparada para una posible integración posterior.
- `scene-source.json`: instantánea de los sprites actuales, posiciones y anclas utilizados para revisar las proporciones.

`generate.py` produce estas referencias sin escribir archivos de producción. Se revisaron la cabeza, la continuidad de hombros y brazos, el recorte en la cintura y la proporción con el plato en ambas disposiciones. Las comprobaciones de paleta, transparencia, silueta conectada y relación de tamaño están en `checks.json`. El juego conserva sus clientes actuales.
