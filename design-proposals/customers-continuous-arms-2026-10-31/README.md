# Revisión de brazos continuos y proporciones

Nueva revisión de los 24 cuerpos. Se conservan los rostros y peinados aprobados, el vestuario y las diferentes poses. Referencias sin integrar al juego.

## Cambios

- Brazo y antebrazo forman una única silueta antes de dibujar su contorno. Se elimina el borde transversal que producía el extremo de cada tramo en el codo.
- El diámetro disminuye de forma continua hacia la muñeca; ya no aumenta de golpe al comenzar el antebrazo.
- Los brazos desnudos incluyen la mano en la misma silueta. No llevan un anillo de contorno en la muñeca.
- Se eliminan las rayas transversales de los puños. La manga termina con el cambio de material a piel.
- Las manos de reposo, agarre, brazos cruzados y manos juntas siguen la dirección del antebrazo. Los gestos de saludo, cintura y barbilla conservan su silueta específica.
- Se ajustan codos con proporciones extremas sin mover los puntos donde se sujetan bolsos, teléfonos, goggles y audífonos.
- Cris tiene un torso y hombros algo más estrechos para que sus brazos y manos juntas quepan en la altura disponible.

## Revisión de los 24

Todos se revisaron ampliados en las dos láminas. Se puso especial atención en las uniones de mangas de Nico, Ren, Alex, Vale, Sam, Noa, Teo, Mai, Jules, Moren, Ari, Ros, Andy, Fer, Pao y Cris; y en la continuidad de piel y manos de Dani, Ivo, Chema y Leo. Los brazos cruzados de Mar, Ivo y Ros se revisaron con su orden de superposición. Beto, Sol y Luz también recibieron correcciones en los brazos que reposan junto al cuerpo.

La revisión de proporciones está documentada en [proportion-review.json](proportion-review.json). Sus valores son medidas proyectadas del dibujo, usadas como diagnóstico junto con la inspección visual; no equivalen a medidas anatómicas reales.

## Comprobación

- 24 cabezas idénticas a las aprobadas y rasgos centrales sin tapar.
- 24 sprites distintos, de 64 × 80, en la paleta Endesga 32 y sin transparencia parcial.
- Siluetas conectadas, con margen dentro del lienzo y sin fragmentos flotantes.
- Prueba específica de los 48 brazos aislados: cero píxeles de contorno dentro de su silueta. La comparación con el dibujo anterior reproduce las líneas internas de los extremos de los tramos. Datos en [elbow-continuity-checks.json](elbow-continuity-checks.json).
- Revisión visual de los 24 personajes, ocho comparaciones antes/después y seis poses dentro del escenario.
- Sin cambios en los clientes activos del juego ni en sus generadores de producción.

## Imágenes

- [Personajes 01–12](customers-continuous-arms-01-12.png)
- [Personajes 13–24](customers-continuous-arms-13-24.png)
- [Comparación con la revisión anterior](bodies-before-after.png)
- [Prueba en el escenario](customers-continuous-arms-context.png)
