# Fase 2: revisión de los 24 cuerpos

Referencias corregidas, pendientes de aprobación. No se han aplicado a los clientes activos del juego. Los rostros y peinados provienen de la última versión aprobada, incluido el pelo simétrico de Jules y Chema.

Se conserva la variedad de alturas, anchuras y poses. Se elimina el sombreado automático grande de los brazos y torsos; el volumen se expresa con silueta, superposición y contornos. Los cuellos son más cortos y las manos se conectan a mangas que se estrechan hacia la muñeca.

## Revisión individual

| Cliente | Problema observado | Corrección |
| --- | --- | --- |
| 01 Nico | Manga levantada muy abultada y sombra grande en el costado. | Codo más recogido, antebrazo fino, índice bajo la barbilla y camisa con paneles más simples. |
| 02 Ren | La manga de cintura se mezclaba con una sombra grande de la chaqueta. | Brazo definido por contorno, manga que se estrecha hacia la muñeca y palma apoyada en la cintura. |
| 03 Alex | Manga voluminosa, mano poco diferenciada y una diagonal dominante sobre el torso. | Móvil a la altura del hombro, dedos sobre sus bordes y chaqueta con cremallera y detalles de bolsillos. |
| 04 Dani | Brazos y manos se leían como piezas rectangulares oscuras. | Camiseta y brazos en color plano; codos y palmas ajustados a la pose de ambas manos en cintura. |
| 05 Beto | Sombra ancha sobre la sudadera y mano poco clara dentro del bolsillo. | Sudadera plana, bolsillo delimitado y mano parcialmente tapada por su abertura. |
| 06 Vale | Mangas hinchadas y saludo de silueta poco clara. | Mangas de ancho controlado, muñeca estrecha y saludo con cuatro dedos y pulgar. |
| 07 Mar | Cruce de brazos voluminoso y puños difíciles de distinguir. | Codos más bajos, antebrazos diagonales, dos manos diferenciadas y cuadros limitados a los paneles de la camisa. |
| 08 Sol | Cárdigan, brazo y correa se confundían en una masa de color. | Paneles del cárdigan más simples, correa sujeta cerca del hombro y bolso unido a sus dos tirantes. |
| 09 Sam | Manga blanca muy abultada, puño y mano difíciles de separar. | Manga más estrecha, puño definido y mano de cintura visible contra la chaqueta. |
| 10 Ivo | Cruce de brazos ancho y casi horizontal, manos grandes y sombras repetidas en la piel. | Codos más bajos, antebrazos diagonales y piel de color plano, conservando las mangas cortas. |
| 11 Luz | Estrella y brazo competían por espacio en un torso corto. | Estrella más pequeña y centrada en el pecho, brazo y mano de saludo más claros. |
| 12 Noa | Antebrazo demasiado largo para alcanzar los goggles con el codo tan bajo. | Codo elevado junto a la cabeza; brazo y antebrazo se flexionan hacia los goggles. |
| 13 Teo | Manga y mano tapaban gran parte de la correa del tote. | Agarre más alto sobre el tirante real, manga afinada y bolso con contorno sencillo. |
| 14 Mai | Mangas anchas y dos manos que se fundían visualmente. | Antebrazos afinados y muñecas escalonadas con una separación visible entre ambas manos. |
| 15 Jules | La manga de la barbilla formaba un triángulo muy grande y el pañuelo ocupaba mucho pecho. | Codo recogido, antebrazo estrecho, índice bajo la barbilla y pañuelo más corto. |
| 16 Moren | Antebrazo muy largo y codo bajo para tocar los audífonos. | Codo elevado hacia el lateral de la cabeza y mano pequeña sobre el auricular. |
| 17 Chema | Brazos con masas y contornos muy pesados respecto a la camiseta. | Mangas cortas y brazos planos, palmas de cintura claras y franjas de camiseta simplificadas. |
| 18 Ari | Manga del móvil poco proporcionada y diagonal grande en la chaqueta. | Teléfono más alto para equilibrar el brazo, puño estrecho y chaqueta de cierre central. |
| 19 Ros | Piel y chaqueta tenían colores demasiado parecidos y el cruce se perdía. | Chaqueta marrón más clara, puños visibles y codos más bajos para separar los antebrazos. |
| 20 Andy | Mano en cintura y manga se mezclaban con una sombra grande. | Solapas más simples, manga de contorno continuo y palma de cintura diferenciada. |
| 21 Fer | Manga de barbilla muy grande respecto al torso y al cuello. | Codo recogido, antebrazo estrecho, mano bajo la mandíbula y solapas equilibradas. |
| 22 Leo | Mangas, brazo y correa formaban varios bloques superpuestos. | Mangas cortas más claras, mano sobre el tirante y camisa con menos estampado. |
| 23 Pao | La manga y la mano del bolsillo se confundían con la chaqueta. | Manga blanca más estrecha, puño visible y abertura que oculta parte de la mano. |
| 24 Cris | Antebrazos y manos formaban una barra ancha sobre el chaleco. | Mangas afinadas, dos manos escalonadas y chaleco con construcción frontal más simple. |

## Verificación

- Los 24 cuerpos son distintos de la propuesta anterior.
- Las 24 cabezas se compararon píxel por píxel con las aprobadas: idénticas.
- Ningún brazo o accesorio pinta encima de los rasgos centrales del rostro.
- Cada sprite conserva 64 × 80 píxeles, paleta Endesga 32 y transparencia binaria.
- Siluetas dentro del lienzo y conectadas, sin fragmentos flotantes.
- Revisión visual de los 24 personajes ampliados, ocho comparaciones antes/después y seis poses a escala fija en el escenario.
- Sin cambios en los clientes activos ni en los generadores de producción.

Las comprobaciones por personaje están en [checks.json](checks.json). Los dibujos siguen siendo referencias para aprobación visual; no se han integrado al juego.

## Imágenes

- [Personajes 01–12](customers-body-review-01-12.png)
- [Personajes 13–24](customers-body-review-13-24.png)
- [Antes y después](bodies-before-after.png)
- [Prueba en el escenario](customers-body-review-context.png)
