# Clientes: ajustes de consistencia

Continuación de `customers-natural-gestures-2026-10-31`. Referencias para revisión, sin integración en el juego.

- **Vale:** cresta rosa de silueta más clara, con puntas y un mechón continuo. Se eliminan los dos bloques de las sienes y se despejan las cejas.
- **Vale y Luz:** el brazo levantado tiene una curva continua en el codo. Se conserva el tamaño pequeño del saludo; no se añade una pieza circular en la articulación.
- **Mar, Ivo y Ros:** grosor nominal de brazo reducido de 8 a 7 píxeles, conservando la pose plegada, el arco del antebrazo y la mano parcialmente oculta.
- **Ivo:** ancho de hombros de 40 a 36 píxeles y cintura de 33 a 30. Pecho de la playera más estrecho, mangas cortas separadas del torso y bordes de manga reconocibles. La piel de los brazos queda fuera de la playera.
- **Nico, Ren, Alex, Mar, Sol, Ivo, Noa, Ari, Andy, Fer y Cris:** se eliminan los restos de piel y de contorno de cabeza que sobresalían sobre el pelo en las primeras siete filas. No se modifica el dibujo del pelo de estos once clientes.

Diez sprites completos quedan idénticos a la referencia anterior, incluidos Jules y Chema. Las facciones, gafas y accesorios faciales de los veinticuatro clientes se conservan.

## Imágenes

- `customers-final-polish-01-12.png` y `customers-final-polish-13-24.png`: elenco completo.
- `hair-before-after.png`: comparación de los once peinados limpiados y la cresta de Vale.
- `bodies-before-after.png`: comparación de codos, brazos y playera con la referencia inmediatamente anterior.
- `gestures-closeup.png`: detalles ampliados de poses.
- `customers-final-polish-context.png`: seis composiciones con el escenario, a la misma escala de cliente y cintura.
- `customer-NN-1x.png`: sprites nativos de 64 × 80 con transparencia.

## Revisión

Inspección visual de los paneles completos, comparaciones de pelo y cuerpo, ampliaciones de articulaciones y escenario. El generador verifica paleta, alfa binario, márgenes, siluetas conectadas, conservación de las facciones a partir de la fila 7 de cada cabeza, alcance de los cambios y ausencia de cortes interiores en los cuarenta y ocho brazos. También verifica que los once clientes señalados no tengan piel expuesta sobre el pelo en la zona superior.

Resultados en `checks.json` y `gesture-contact-checks.json`. La revisión visual sigue siendo necesaria para valorar la anatomía; las comprobaciones de píxeles no la sustituyen. Los archivos de clientes en producción permanecen sin cambios.
