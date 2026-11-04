# Clientes cartoon 2D — tercera revisión

24 referencias sin integrar, conservando las poses, estaturas, nombres y estilos de la segunda tanda.

## Dirección

Se retiraron las bandas de luz continuas de brazos y caras, el parche brillante del pecho y los reflejos de las manos. El dibujo usa color base, contorno de un píxel y una sombra gráfica por pieza. El pelo se reduce a dos tonos principales y las solapas dejan de funcionar como facetas brillantes. El objetivo es caricatura 2D, no una figura modelada en 3D.

Nueve siluetas faciales: alargada, cuadrada, corazón, ancha, rombo, estrecha, triangular, mandíbula ancha y redonda. También varían cejas, ojos, nariz y boca. La barba sigue la mandíbula de cada personaje. Los cuellos se ajustan al largo del nuevo rostro. Se conservan las complexiones y gestos de la tanda anterior; no se vuelve al cuerpo rectangular de la primera.

## Entregables

- `customers-cartoon-2d-01-12.png` y `customers-cartoon-2d-13-24.png`: láminas de 12 a escala ×4.
- `customers-cartoon-2d-context.png`: seis casos a escala ×2, con el escenario y objetos finales, sin interfaz.
- `customer-01-1x.png` … `customer-24-1x.png`: imágenes transparentes de 64 × 80.
- `cast.json`: elenco, poses y silueta facial.
- `generate.py`: generador aislado, con Pillow; reutiliza el elenco y módulos de peinado/accesorios de la primera tanda.

## Verificación y alcance

Se inspeccionaron las dos láminas y la prueba de escenario. Se comprobaron 24 imágenes únicas, dimensiones, margen de cabeza/codos y paleta Endesga 32. Se limpiaron píxeles aislados fuera del personaje.

No hay modificaciones en los sprites activos ni en el registro del juego. Pendiente aprobación, expresiones, transiciones, anclas del cliente y de la paciencia según estatura, interfaz real y móvil. La prueba contextual es una composición de referencia; no es una captura del juego con los clientes integrados. No se compiló la aplicación porque esta carpeta no entra en ella.
