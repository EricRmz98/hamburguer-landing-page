# Elenco aprobado integrado

Los 24 clientes de `customers-vale-ivo-contours-2026-10-31/customers-all-24.png` están integrados como variantes de `cliente` en el atlas del juego. Cada uno tiene tres expresiones. El cuadro de espera conserva todos los píxeles aprobados; la satisfacción y el enfado solo modifican rasgos de la cara.

La fuente editable es `scripts/sprites/customers-approved.json`. Se regenera `src/game/sprites/people.ts` con `python3 scripts/sprites/write_people.py`, sin Pillow ni dependencia de las propuestas históricas. La generación conserva un solo cuerpo por personaje y aplica parches faciales para evitar datos repetidos.

Los escenarios usan un espacio de cliente de 64 × 80 centrado, con la misma altura y cuatro filas detrás del borde de la barra. Se conservan las animaciones de llegada, satisfacción y salida del juego.

Verificación: 160 pruebas correctas y compilación correcta. Comprobaciones específicas de los 24 dibujos mediante sus huellas RGBA aprobadas, tres expresiones distintas por personaje, siluetas idénticas entre expresiones y tamaño/alineación en ambas disposiciones. Inspección visual de las reacciones y del juego en escritorio y móvil simulado de 390 × 844; no se probó en un teléfono físico.

- `game-desktop.png`: juego compilado en escritorio, con Ivo.
- `game-mobile.png`: la misma partida con la disposición vertical y la expresión de impaciencia.

Las referencias anteriores se conservan. No se publicó el sitio.
