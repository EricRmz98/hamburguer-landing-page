# Endesga64 · estilo común con clientes · 3 de noviembre de 2026

Aplicado al minijuego y a la vista de revisión `/clientes-prueba`. Se mantienen los doce clientes aprobados, las proporciones de Inés al 85 % y los perfiles alternados. Las referencias del nuevo comedor se generaron con la herramienta integrada **imagegen** (sin CLI ni API externa); los prompts completos están en `prompts.txt`.

## Producción

- Paleta oficial Endesga64, de ENDESGA: https://lospec.com/palette-list/endesga-64 . Fuente oficial guardada en `endesga-64.source.json` y `scripts/sprites/endesga-64.json`.
- `referencia-horizontal.png` y `referencia-vertical.png`: referencias artísticas. **No son las imágenes usadas directamente en el juego.**
- `normalize.py`: importación inicial a 320 × 122 y 180 × 200, color oficial único por celda, sin tramado ni alfa. Genera también la barra de cerámica con juntas rectas. El giro de la silla derecha horizontal se corrige mediante espejo de sus celdas y sombra inmediata.
- `scripts/sprites/environment-native/*.png`: los cuatro maestros finales editables. `environment_gen.py` solo comprueba y convierte sus celdas a matrices de texto, sin reescalar.
- Clientes reimportados desde la tanda nativa aprobada, sin remuestreo, para evitar pérdidas acumuladas de color. Ingredientes, utensilios, etiquetas y controles usan Endesga64; las dimensiones, anclas y zonas de interacción se conservan.

## Revisión

`composicion-final.png` reúne capturas reales de horizontal y vertical. `composicion/` contiene las 24 composiciones con sus doce clientes y comprobaciones de escala. `12-clientes-endesga.png` y `cocina-detalle.png` muestran los sprites de producción ampliados exclusivamente con vecino más cercano. `antes-despues.png` compara el comedor anterior con el nuevo. `partida-real.png` verifica que la nueva dirección también está en el juego principal.

161 pruebas y compilación correctas. Consolas del juego y de la vista de revisión sin errores. Arranque, incorporación de pan, carne en la plancha y pausa comprobados en el juego principal. Revisión vertical mediante la composición móvil; no se comprobó en teléfono físico.
