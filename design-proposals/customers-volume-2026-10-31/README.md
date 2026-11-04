# Clientes — anatomía, volumen y poses

Segunda tanda de 24 referencias para aprobación. Conserva nombres, estilos y pronombres de la tanda anterior, pero sustituye el torso rectangular y el esquema de brazos pegados. No modifica los clientes activos del juego.

## Cambios visuales

- Lienzo nativo 64 × 80, con cintura común y margen para codos. No se estiran los sprites anteriores.
- Alturas visibles aproximadas de 55 a 72 píxeles. Hombros de 30 a 42 unidades, cintura y rostro independientes.
- Torso construido desde cuello, hombros, pecho y cintura; hombros asimétricos, brazos articulados con codo y muñeca, manos con pulgar orientado hacia cada lado.
- Poses de cintura, ambas manos en cintura, brazos cruzados, mano en barbilla, saludo, móvil, bolsillo, correa, audífonos y manos entrelazadas.
- Sombras por pieza, superficies de luz en hombros y mejillas, pliegues cortos y sombras de contacto. Se mantienen Endesga 32 y el lenguaje cartoon de los objetos finales.
- Cabezas con mejilla y mandíbula variables, nariz sombreada, pequeñas diferencias en ojos y boca; prendas adaptadas al cuerpo y a la pose.

Los peinados y accesorios conservan rasgos de la dirección aprobada; la construcción del cuerpo y rostro ya no usa `people.body()` ni la plantilla rectangular anterior. El generador anterior solo aporta el elenco, paletas y módulos de peinado/accesorios.

## Archivos

- `customers-volume-01-12.png` y `customers-volume-13-24.png`: 24 referencias a escala ×4, con línea de cintura fija para comparar estaturas reales.
- `customers-volume-context.png`: seis personajes sobre el entorno y objetos finales. Lienzo de 64 px centrado en la posición del cliente, sin comanda ni ayudas.
- `customer-01-1x.png` … `customer-24-1x.png`: originales transparentes.
- `cast.json`: pose y parámetros del cuerpo de cada personaje.
- `generate.py`: generador aislado; requiere Pillow y reutiliza los módulos de la tanda anterior y el entorno del proyecto.

## Revisión y límites

Se inspeccionaron las dos láminas y la prueba contextual. Se corrigió el margen de los codos para evitar recortes y se revisó la mano que entra en el bolsillo y la orientación de los pulgares. Comprobaciones: 24 imágenes, todas de 64 × 80; Endesga 32 en cada píxel visible; cabeza y codos con margen dentro del lienzo. Se conserva la tanda anterior para comparar.

No se integraron al juego. Son poses de referencia; las expresiones feliz/enojada y las transiciones quedan para después de aprobar la dirección. Integrarlas requerirá ampliar y centrar el espacio del cliente, definir anclas por personaje y ajustar la barra de paciencia a las estaturas. Las manos bajas pueden quedar tras el mostrador; las muestras contextuales permiten valorar esa oclusión. Pendiente probar interfaz completa y móvil. No se ejecutó la compilación porque no hay cambios de aplicación.
