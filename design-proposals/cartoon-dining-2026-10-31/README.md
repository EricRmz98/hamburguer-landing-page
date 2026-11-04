# Revisión cartoon

Tercera tanda, conservando las anteriores. Reinterpreta las seis parejas con muebles robustos, esquinas redondeadas pixeladas, contornos por material, planos de luz y sombra, mesas con canto grueso, asientos acolchados, macetas con hojas agrupadas y marcos de puertas con volumen. Se redujo la densidad de las juntas del suelo para disminuir la apariencia de dibujo arquitectónico.

- `interiors-six-options.png`: seis interiores limpios a escala ×3.
- `bars-six-pairs.png`: seis parejas con los objetos finales y sus posiciones originales.
- Archivos `*-1x.png`: 18 imágenes lógicas independientes.
- `generate.py`: generador aislado con Pillow; consume `source-sprites.json`, copia exacta de las matrices resueltas del proyecto. No regenera ni modifica los sprites finales.

Se revisaron visualmente ambas láminas y se verificó que todos los píxeles de las escenas pertenecen a Endesga 32. Las formas nuevas se trazan en cuadrícula lógica sin suavizado; solo el texto exterior de presentación usa suavizado.

No hay integración, cambios en producción, commits ni publicación. Siguen pendientes pruebas con comanda/globo reales, todos los clientes, formato vertical y animación. Las puertas centrales quedan parcialmente detrás del cliente. La revisión mejora el lenguaje de formas y volumen; la aprobación de compatibilidad estética queda abierta al usuario.

Reproducir desde la raíz con un entorno Python que tenga Pillow:

```sh
python3 design-proposals/cartoon-dining-2026-10-31/generate.py
```
