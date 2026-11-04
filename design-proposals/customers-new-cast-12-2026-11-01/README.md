# Propuesta de 12 clientes nuevos

El usuario solicitó una nueva dirección de personajes, más cercana al acabado del fondo, la barra, la comida y los utensilios. Se generaron doce imágenes individuales nuevas con la herramienta integrada `image_gen`. La referencia de arte principal, `style-reference.png`, reproduce los sprites actuales del escenario y la cocina sin clientes; no se modificó el juego para producirla.

Los conceptos comparten contornos oscuros de color, iluminación cálida superior izquierda, sombras por bloques y detalles de tela, cabello, bolsillos, puños, herrajes y accesorios. Las imágenes son referencias de diseño en resolución alta, no matrices de producción de 64 × 80 ni una garantía de paleta Endesga 32 exacta. La conversión de resolución, colores y expresiones queda para una siguiente fase después de elegir la dirección visual.

## Personajes

1. Lía — skater, chaqueta roja y crema, gorra.
2. Bruno — indie, anteojos, sobrecamisa de pana y tote.
3. Zoe — gótica, chaqueta ciruela y cabello rizado.
4. Ciro — afición al fútbol, camiseta verde y crema.
5. Mika — techwear, prenda técnica oscura y mecha turquesa.
6. Alma — arte, chaqueta de lona crema y cabello cobrizo.
7. Rafa — rockabilly, cuero oscuro y pañuelo rojo.
8. Dante — metal, chaleco de mezclilla y cabello recogido.
9. Vega — rave, rompevientos de bloques de color y gafas.
10. Inés — kawaii, cardigan tejido y pasadores de estrella.
11. Gael — surf, camisa azul desgastada y cabello aclarado.
12. Sasha — streetwear, bomber oliva y gorro rojo.

## Archivos

- `clientes-nuevos-12.png`: lámina completa numerada.
- `clientes-nuevos-01-06.png`, `clientes-nuevos-07-12.png`: dos hojas con seis referencias cada una.
- `individuales/`: los doce PNG originales seleccionados, conservando su transparencia generada.
- `12-clientes-referencias.zip`: imágenes individuales, láminas, referencia y prompts.
- `prompts.json`: instrucciones exactas por imagen, método integrado y procedencia de cada resultado. Incluye la corrección de fondo solicitada para Vega.
- `checks.json`: cantidad, dimensiones y transparencia de los archivos entregados.

`assemble.py` solo maqueta las imágenes, con recorte a su contenido visible y reducción uniforme sin suavizado; no redibuja los originales. Se inspeccionaron los resultados individuales durante la generación y la lámina final. Son doce referencias distintas y no sustituyen los 24 clientes activos ni la propuesta de texturas anterior.
