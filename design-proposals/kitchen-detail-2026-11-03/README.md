# Detalle de barra e ingredientes · 3 de noviembre de 2026

Aplicado en el juego principal y en `/clientes-prueba`. Refinamiento directo de los generadores y de las celdas nativas, sin generar imágenes de referencia nuevas ni remuestrear sprites.

- Barra: juntas rectas, profundidad del esmalte rojo, reflejos cortos y capa de acero cepillado con sombra bajo el canto. `scripts/sprites/counter_gen.py` reproduce los dos maestros PNG; `environment_gen.py` los convierte a las matrices del atlas.
- Pan: miga con poros agrupados, luz en el domo y costra de borde más tostada.
- Carne: marcas de sellado interrumpidas, relieve y brillos de grasa; se conservan las cuatro fases de cocción.
- Queso: pliegues leves, brillo del borde, poros pequeños y separación entre lonchas en la bandeja.
- Verduras: nervaduras de lechuga con pliegues, cámaras de pulpa y semillas del tomate, anillos de cebolla con sombras frías.
- Salsas: bordes de volumen y reflejo localizado; sus variantes mantienen colores propios.
- Acero: bandas de reflexión, sombra lateral y uniones finas en bandejas y plancha.

`composicion-final.png` muestra las capturas reales horizontal y vertical; `antes-despues.png` compara la misma escena. `cocina-detalle.png` amplía las matrices de producción a 4×, sin suavizado. `checks.json` confirma que los 26 sprites/variantes con cambios conservan dimensiones, siluetas y anclas. Los dos fondos de comedor y todos los clientes aprobados se mantienen iguales. Todo utiliza exclusivamente Endesga64 y escala entera común.

161 pruebas y compilación correctas. Revisión de ambas composiciones con la hamburguesa montada y consola sin errores. No se comprobó en teléfono físico.
