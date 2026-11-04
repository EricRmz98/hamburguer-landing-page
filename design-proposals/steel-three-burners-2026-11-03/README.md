# Metal, basura y plancha · 3 de noviembre de 2026

Aplicado en el minijuego y en `/clientes-prueba`.

- Acero: reflejos continuos, tonos neutros y fríos, cepillado alargado y sombra bajo el canto, siempre en Endesga64 y sin suavizar la cuadrícula.
- Basura: a la izquierda de la plancha y del lado de preparación, sin mueble metálico adicional. El sprite 44 × 20 tiene un labio de acero elevado y una pequeña sombra de contacto.
- Plancha: tres quemadores, 118 × 35 en horizontal y 90 × 35 en vertical. Perillas circulares de 7 × 7, con luz de borde y marca indicadora. Los indicadores de cocción y las carnes se colocan encima para mantener los controles visibles.
- Disponibilidad: capacidad máxima de tres y tres lugares activos desde el inicio en todos los niveles. Las recetas siguen aumentando su dificultad; el tiempo mínimo de cocción se calcula con esa capacidad.

161 pruebas y compilación correctas. Las pruebas de sesión verifican que caben tres carnes desde el primer cliente, que no se añade una cuarta y que no cambia la capacidad al progresar. Revisión de ambas composiciones y partida móvil real con tres carnes simultáneas y perillas visibles (`tres-carnes-mobile.png`, `runtime-burners.json`). Sin errores nuevos de consola tras recargar. No se revisó en teléfono físico.

`composicion-final.png` reúne capturas reales de ambas vistas; `antes-despues.png` compara con la composición previa. `composicion/browser-checks.json` comprueba tres lugares sin bloquear, basura a la izquierda y escala entera común.
