# Espacio de trabajo, plato y botes · 3 de noviembre de 2026

Aplicado a la página de revisión y al minijuego principal.

- Barra móvil: de 80 a 100 filas, escena de 180 × 300. La encimera tiene 36 filas nativas, con espacio delante y a los lados del plato. Los ingredientes y la plancha bajan juntos.
- Plato: de 31 × 18 a 38 × 22; se redibuja desde el modelo de radio 19, sin reescalar. La hamburguesa se centra por su nueva ancla 19/11.
- Horizontal: escena de 320 × 212, barra de 320 × 90 y encimera de 28 filas para acomodar el mismo plato; la basura se coloca en la encimera entre comanda y plato.
- Basura: abertura de 44 × 18 con profundidad, aro de acero y bolsa oscura. Su boca recibe una carne completa. Con el espacio extra ya se usa el mismo sprite en móvil y escritorio.
- Salsas: botes sin etiquetas, con hombros curvos, tapa estriada, boquilla y bandas de sombra y brillo. Conservan 14 × 35, el cuadro apretado y las áreas de toque.

La pared, los clientes y todos los alimentos conservan sus matrices; todo sigue en Endesga64 con escala entera común. `checks.json` y `composicion/browser-checks.json` verifican tamaños y separación visual. `composicion-final.png` reúne capturas reales de ambas disposiciones; `antes-despues.png` muestra el cambio respecto a la revisión intermedia de los botes. `cocina-detalle.png` amplía los sprites de producción sin suavizado.

161 pruebas y compilación correctas. Comprobación de ambos formatos y de una partida real móvil a 390 × 844: escenario 360 × 600 a 2×, pan, carne en la plancha y pausa. Sin errores nuevos de consola después de recargar. No se revisó en teléfono físico.
