# Comedores y barras — segunda tanda

Dirección solicitada: desde el cocinero hacia el local. Esta carpeta conserva la primera tanda y no altera el juego.

## Láminas

- `interiors-six-options.png`: seis interiores limpios a ×3, sin cliente, comanda ni globo, para valorar acceso, mesas, sillas y suelo.
- `bars-six-pairs.png`: seis barras diferentes, cada una con su interior compatible y todos los sprites finales a ×3.

| Pareja | Interior | Barra | Diferencia |
| --- | --- | --- | --- |
| F01 + B01 | Salón de barrio | Roble horizontal | Acceso central, seis mesas a tres distancias, sillas burdeos |
| F02 + B02 | Diner de esquina | Acero satinado | Entrada derecha, bancos rojos, calle nocturna |
| F03 + B03 | Comedor jardín | Cerámica verde | Acceso izquierdo, recorrido diagonal, plantas, mesas escalonadas |
| F04 + B04 | Local urbano | Baldosa azul | Pasillo central ancho, mesas metálicas, suelo oscuro |
| F05 + B05 | Cantina de madera | Nogal de trabajo | Acceso derecho, bancos verdes, madera cálida |
| F06 + B06 | Hamburguesería nocturna | Piedra grafito | Puerta izquierda, mesas a distintas distancias, acento burdeos |

Las opciones con acceso lateral dejan la puerta más visible detrás del cliente. F01 es la más ordenada y cálida; F03 aporta un recorrido menos simétrico; F06 da más contraste a los alimentos.

## Método y revisión

Se mantiene la metodología y las skills pertinentes ya revisadas: Luxury Pages/Luxury Web Design, ASSETS.md, UI/UX Pro Max y Emil Design Engineering. Las skills complementarias requeridas siguen disponibles. Materialidad y claridad del protagonista son los principios transferidos de la referencia local The Watch.

Los fondos se generan en cuadrícula pixelada con proyección de puntos del suelo, tableros, patas y asientos a distintas distancias. La paleta procede de `palette.ts`. `source-sprites.json` es la exportación exacta de `resolveSprite` de la primera tanda; se compone sin regenerar, recolorear ni editar ingredientes, plancha, plato, bandejas, cliente o salsas. El generador no escribe en `src/`.

Las barras son superficies horizontales de 320 × 78. Juntas de baldosa convergentes, separación de tablones, borde posterior y labio frontal estrecho refuerzan su lectura como plano de trabajo, sin listones de fachada vertical.

Archivos individuales: seis `interior-*-clean-1x.png` de 320 × 122, seis `bar-*-clean-1x.png` de 320 × 78 y seis `pair-*-context-1x.png` de 320 × 200. Composición contextual en las posiciones horizontales originales del juego.

Se inspeccionaron visualmente ambas láminas y se iteraron las juntas del suelo de F03/F04 por bajo contraste y las uniones de tablones. Comprobación automática de todos los píxeles lógicos: pertenecen a Endesga 32. El suavizado se limita a la tipografía exterior de las láminas.

Reproducir con un entorno Python que tenga Pillow:

```sh
python3 design-proposals/dining-room-2026-10-31/generate.py
```

## Límites

Son propuestas estáticas, no assets integrados. No se muestran comanda, globo ni HUD para que se vea el interior. Su composición definitiva necesita ajuste: la interfaz actual taparía parte de las mesas y las puertas laterales; el cliente cubre la parte inferior de las puertas centrales. No se han movido los elementos del juego. Pendiente comprobar interfaz completa, formato vertical de 180 × 280, todos los clientes, hamburguesas muy altas y animación. No hubo cambios en código de producción, dependencias o configuración; no se requiere compilación para estos PNG. Sin commits ni publicación.
