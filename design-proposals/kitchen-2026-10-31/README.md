# Barras y cocinas — propuestas, 31 octubre 2026

Dos láminas PNG: `bars-six-options.png` y `backgrounds-six-options.png`. Cada lámina contiene seis opciones numeradas con nombres, a escala entera ×3. Para comparar una sola variable, las barras comparten F01 y los fondos comparten B01. Las combinaciones entre familias quedan abiertas.

## Opciones

| Barra | Dirección |
| --- | --- |
| B01 Roble de parrilla | Madera cálida en tablones horizontales anchos |
| B02 Acero cepillado | Metal frío, juntas largas y remaches discretos |
| B03 Cerámica azul | Baldosa modular con juntas finas |
| B04 Esmalte verde | Paneles verticales verdes y borde cálido |
| B05 Piedra grafito | Superficie oscura con vetas contenidas |
| B06 Nogal acanalado | Listones verticales con relieve marcado |

| Fondo | Dirección |
| --- | --- |
| F01 Brasserie azul | Azulejo oscuro, campana central y repisas |
| F02 Ladrillo ahumado | Ladrillo cálido y zócalo liso oscuro |
| F03 Despensa verde | Cerámica verde, repisas y ventilación horizontal |
| F04 Cocina de acero | Grandes paneles metálicos y ventilación industrial |
| F05 Ventana al obrador | Pasaplatos profundo con divisiones de madera |
| F06 Diner nocturno | Pared tranquila, franja burdeos y rótulos discretos |

Preferencias iniciales: B01 + F02 para calidez; B05 + F06 para destacar los ingredientes. Las repisas y detalles se concentran arriba; el área de trabajo mantiene contraste con los alimentos.

## Archivos y método

- `*-environment-1x.png`: 12 escenarios limpios de 320 × 200, sin objetos ni interfaz.
- `*-context-1x.png`: 12 escenas con cliente, alimentos, bandejas, plancha, plato y botes originales.
- `source-sprites.json`: copia resuelta de matrices y variantes aprobadas, extraída mediante `resolveSprite` del proyecto; no regenera ni modifica los originales.
- `export.mjs`: exportación reproducible desde las definiciones TypeScript.
- `generate.py`: dibuja fondos y materiales sobre cuadrícula lógica con Pillow y compone las matrices originales; escala con vecino más cercano. Los fondos se trazan como módulos y planos pixelados; no se utiliza generación de imágenes por IA ni se vuelve a ejecutar el generador de vóxeles sobre los objetos finales.

Reproducir desde la raíz con Node 24 y un entorno Python con Pillow:

```sh
node design-proposals/kitchen-2026-10-31/export.mjs
python3 design-proposals/kitchen-2026-10-31/generate.py
```

## Criterios y verificación

Se leyeron Luxury Pages, Luxury Web Design, ASSETS.md, la referencia local The Watch, UI/UX Pro Max y Emil Design Engineering. Todas las skills complementarias exigidas aparecen disponibles en el catálogo de esta sesión; no hicieron falta instalaciones. Se transfieren materialidad, continuidad del protagonista y restricción decorativa de la metodología, sin trasladar la estética del reloj al juego.

Las posiciones corresponden a la disposición horizontal real. Cámara y sombreado originales de los objetos se conservan; los planos de entorno siguen el eje frontal de las piezas rectangulares. Comanda, globo y barra de paciencia son muestras fijas de sus espacios de lectura, no capturas de la interfaz final; no incluyen texto real. No hay HUD en la muestra.

Revisión visual de ambas láminas completada. El generador verifica que todos los píxeles de los PNG lógicos pertenecen a Endesga 32. La tipografía de presentación exterior a las escenas usa suavizado. Ningún archivo de `src/`, sprite final, dependencia o configuración del juego se modificó. No se integró ninguna opción ni se hicieron commits.

Pendiente tras elegir: adaptación vertical de 180 × 280, pruebas en móvil, visibilidad con hamburguesas muy altas, todos los clientes y comandas reales, estados de error y animación, y conversión del entorno elegido a tiles/atlas del juego. No se ejecutó la compilación porque no hay cambios de implementación.
