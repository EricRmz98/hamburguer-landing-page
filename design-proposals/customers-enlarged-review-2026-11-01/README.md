# Plantilla de los 24 clientes actuales ampliados

El usuario decidió conservar los personajes anteriores y solicitó verlos todos después del aumento de tamaño. Esta exportación usa los píxeles del cuadro de espera de las 24 variantes activas de `src/game/sprites/people.ts`, en el orden de `CUSTOMER_PROFILES`. Cada imagen nativa coincide con el hash de la versión aprobada en `scripts/sprites/customers-approved.json`.

La escala vigente del juego es 150 %: el cuadro nativo de 64 × 80 ocupa 96 × 120. La lámina de detalle amplía cuatro veces ese tamaño, equivalente a seis veces la matriz nativa. Se usa vecino más cercano; no se redibujan detalles, no se alteran colores ni se modifican cuerpos o caras.

- `clientes-todos-detalle.png`: los 24 personajes con nombre y número, 6 columnas × 4 filas, listos para revisión ampliada.
- `clientes-01-12.png`, `clientes-13-24.png`: dos hojas de detalle con 12 personajes cada una.
- `clientes-escala-juego.png`: los 24 a 96 × 120 con nombres.
- `clientes-24-plantilla-transparente.png`: cuadrícula sin etiquetas y con fondo transparente; celdas de 96 × 120.
- `clientes-24-ampliados.zip`: los 24 PNG individuales transparentes, plantilla y manifiesto.
- `sprites-96x120/`: esos PNG individuales, nombrados por número y personaje.
- `manifest.json`: correspondencia entre nombres y celdas.
- `checks.json`: validaciones de identidad, escala, alfa y coincidencia con la cuadrícula exportada.
- `runtime-source.json`: instantánea de los píxeles y perfiles activos utilizados por `generate.py`.

El fondo claro de las hojas es únicamente para facilitar la inspección de contornos y playeras claras. No forma parte de los PNG individuales. Esta exportación no modifica el juego ni registra el prototipo genérico.
