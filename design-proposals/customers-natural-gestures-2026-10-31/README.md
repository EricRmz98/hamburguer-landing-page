# Clientes: gestos naturales

Revisión de las referencias `customers-collars-gestures-2026-10-31`. Sin integración en el juego.

- Vale y Luz: saludo de 8 × 10 píxeles con contorno incluido, frente a 11 × 14. Dedos agrupados y pulgar lateral; misma escala de mano en ambas.
- Mar, Ivo y Ros: brazos de mayor grosor, codos redondeados y antebrazos ligeramente curvos. Cruce más bajo, casi horizontal, con una mano apoyada y la otra parcialmente oculta. En Ivo, las mangas se ajustan al nuevo grosor del brazo.
- Nico, Jules y Fer: dedos recogidos bajo el lateral de la barbilla; desaparece el índice vertical sobre la mejilla. La otra mano sostiene el codo. La cabeza se dibuja delante de los nudillos para conservar la mandíbula y la barba.
- Jules: pañuelo rojo óxido con pliegue triangular, nudo lateral y dos puntas cortas. Se elimina el bloque amarillo.

Los otros dieciséis clientes coinciden píxel por píxel con la versión anterior. Las veinticuatro cabezas de referencia coinciden con las aprobadas, incluidos los peinados de Jules y Chema.

## Entrega

- `customers-natural-gestures-01-12.png` y `customers-natural-gestures-13-24.png`: elenco completo.
- `gestures-closeup.png`: ampliaciones de las ocho poses intervenidas.
- `bodies-before-after.png`: comparación con la referencia inmediatamente anterior.
- `customers-natural-gestures-context.png`: seis composiciones con el escenario.
- `customer-NN-1x.png`: veinticuatro sprites nativos de 64 × 80 con transparencia.

## Revisión

Inspección visual de los dos paneles del elenco, detalles ampliados y composición en el escenario. El generador comprueba paleta Endesga32, alfa binario, márgenes, siluetas conectadas, conservación de las cabezas y de los dieciséis personajes ajenos a esta corrección. Comprueba también el contacto de las manos con la barbilla/brazo y la ausencia de líneas interiores añadidas en los codos de los cuarenta y ocho brazos. Estas comprobaciones apoyan la revisión visual; no constituyen una garantía automática de anatomía.

Resultados en `checks.json`, `gesture-contact-checks.json` y `wave-size-checks.json`. Los archivos de clientes utilizados por el juego y sus generadores permanecen sin cambios.
