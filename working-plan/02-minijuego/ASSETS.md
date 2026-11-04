# Sprites como texto

Los sprites del [minijuego](PLAN.md) no son imágenes: son **definiciones de texto**. Cada una declara su tamaño en pixeles, qué color representa cada letra y una matriz de caracteres con el dibujo. La IA (el agente que trabaja en el proyecto) los escribe directamente en el código. Al arrancar, el motor los convierte una sola vez en imágenes y los muestra con un solo elemento HTML por sprite.

Estado: **inventario completo en el juego (F4)**. 30 definiciones en `src/game/sprites/` (`ingredients.ts`, `utensils.ts`, `people.ts`, `ui.ts`, `tiles.ts`, `environment.ts`), incluidas las 12 variantes nativas de clientes aprobadas, registradas en `index.ts`, válidas y conformes a la guía de estilo. El entorno parte de referencias generadas y reducidas una sola vez a la cuadrícula nativa; sus maestros editables están en `scripts/sprites/environment-native/`. El juego solo consume las matrices de texto verificadas.

## Estado visual aprobado · 3 de noviembre de 2026

Este resumen describe los recursos vigentes; el historial posterior conserva las iteraciones anteriores.

| Recurso | Matriz o criterio vigente |
| --- | --- |
| Paleta | Exactamente 64 colores oficiales Endesga-64 |
| Escala | Un único factor entero para clientes, entorno, cocina e interfaz |
| Clientes | Doce retratos de 96 × 120; seis perfiles por lado; Inés al 85 % incorporado en su matriz |
| Escenario | Horizontal 320 × 212; vertical 180 × 300 |
| Comedor | 320 × 122 y 180 × 200; pared continua, barra blanca y asientos al fondo |
| Barra | 320 × 90 y 180 × 100; cerámica roja, acero gris azulado y reflejos estrechos como la puerta y la plancha |
| Plato | 38 × 22; ancla 19/11 |
| Salseros | 16 × 42; ancla 8/38; cuerpo alargado, tapa baja, boquilla fina, hombro ovalado y sombra de apoyo; dos cuadros |
| Plancha | 118 × 35 y 90 × 35; tres quemadores activos desde el inicio y perillas redondas |
| Basura y charola de carne | 42 × 25, a la misma altura y a ambos lados de la plancha; basura con labio elevado y bolsa interior texturizada |

Plato, riel de ingredientes, plancha y conjunto inferior comparten el centro del escenario. Las zonas de interacción siguen las dimensiones nativas de cada disposición. Las capturas finales están en [salseros alargados](../../design-proposals/sauce-dispensers-2026-11-03/README.md); el [índice de revisiones](../../design-proposals/README.md) enlaza los maestros y el historial. Se comprobaron ambas composiciones, la paleta, las matrices y las reglas del juego: 161 pruebas y compilación correctas. La revisión en teléfono físico sigue pendiente.

## Por qué texto

- **Es pixel art real desde el principio**: no hay pixeles falsos, antialias ni colores fuera de la paleta que corregir.
- **Editable por celdas**: una carne de 32 × 6 son 192 caracteres, y una corrección puntual cambia una línea en vez de regenerar una imagen. Los retratos y escenas completos tienen matrices mayores y se regeneran desde sus fuentes editables.
- **Paleta común**: las letras solo pueden apuntar a colores de la paleta global, así que ningún sprite introduce colores ajenos a esa paleta; la coherencia artística también se revisa visualmente.
- **Variantes casi gratis**: la misma matriz con otra paleta da otro sprite. La carne cruda, perfecta y quemada, los tres botes y los clientes con distinta ropa salen de una sola definición cada uno.
- **Versionable**: cada cambio de un sprite se ve como un diff legible en Git.
- **Sin descargas**: los sprites viajan dentro del JavaScript del juego, comprimidos con el resto, sin peticiones de imágenes aparte.

## Formato

### Estilo y paleta (decididos)

- **Perspectiva**: **frontal elevada 3/4** (cámara a 32° de altura, girada 12° para que se vea el costado derecho). Se eligió tras comparar la vista lateral original (se veía plana), la 3/4 y la isométrica 2:1 (más profundidad, pero obligaba a reacomodar el escenario en diagonal). Los clientes, el humo y la interfaz se quedan de frente, como es habitual en este estilo.
- **Estilo**: caricatura 2D de proporciones creíbles y materiales detallados, con los doce clientes aprobados como referencia. Contorno selectivo, sombras agrupadas y texturas por material (costra, vetas, tela, esmalte), evitando ruido y tramado uniforme. El fondo mantiene menor contraste que los personajes y la comida.
- **Paleta**: [Endesga 64](https://lospec.com/palette-list/endesga-64), de **ENDESGA**. Se usan exactamente sus 64 colores. La fuente original se conserva en `scripts/sprites/endesga-64.json` y las pruebas comparan cada hexadecimal con `palette.ts`.

### Paleta global

Los 64 colores tienen nombre propio en español. Las letras de los sprites apuntan a esos nombres; el hex vive solo en `palette.ts`.

```ts
// Endesga 64, de ENDESGA: https://lospec.com/palette-list/endesga-64
// Los 64 colores oficiales; escenas, clientes e interfaz comparten esta paleta.
export const PALETTE = {
  'alerta': '#ff0040',
  'negro': '#131313',
  'carbon': '#1b1b1b',
  'grafito': '#272727',
  'gris-oscuro': '#3d3d3d',
  'gris-neutro': '#5d5d5d',
  'gris-medio': '#858585',
  'plata': '#b4b4b4',
  'blanco': '#ffffff',
  'gris-claro': '#c7cfdd',
  'gris': '#92a1b9',
  'gris-azul': '#657392',
  'pizarra': '#424c6e',
  'noche': '#2a2f4e',
  'azul-tinta': '#1a1932',
  'tinta': '#0e071b',
  'cafe-negro': '#1c121c',
  'cafe-oscuro': '#391f21',
  'cafe': '#5d2c28',
  'oxido': '#8a4836',
  'canela': '#bf6f4a',
  'piel': '#e69c69',
  'piel-clara': '#f6ca9f',
  'crema': '#f9e6cf',
  'tostado': '#edab50',
  'durazno': '#e07438',
  'naranja-oscuro': '#c64524',
  'tierra': '#8e251d',
  'naranja': '#ff5000',
  'ambar-oscuro': '#ed7614',
  'ambar': '#ffa214',
  'amarillo': '#ffc825',
  'vainilla': '#ffeb57',
  'pistacho': '#d3fc7e',
  'lima': '#99e65f',
  'verde-claro': '#5ac54f',
  'verde': '#33984b',
  'verde-oscuro': '#1e6f50',
  'verde-noche': '#134c4c',
  'petroleo': '#0c2e44',
  'azul-oscuro': '#00396d',
  'azul': '#0069aa',
  'azul-claro': '#0098dc',
  'cian': '#00cdf9',
  'cian-claro': '#0cf1ff',
  'hielo': '#94fdff',
  'rosa-palido': '#fdd2ed',
  'malva': '#f389f5',
  'magenta-neon': '#db3ffd',
  'violeta': '#7a09fa',
  'ultravioleta': '#3003d9',
  'indigo': '#0c0293',
  'azul-profundo': '#03193f',
  'ciruela-oscura': '#3b1443',
  'ciruela': '#622461',
  'magenta': '#93388f',
  'lila': '#ca52c9',
  'rosa-viejo': '#c85086',
  'rosa': '#f68187',
  'coral': '#f5555d',
  'rojo': '#ea323c',
  'rojo-ladrillo': '#c42430',
  'carmesi': '#891e2b',
  'rojo-oscuro': '#571c27',
} as const;
```

Rampas por material (contorno → sombra → base → luz). Viven en código como `RAMPS` (`palette.ts`): cada sprite declara sus `materials` y la revisión de estilo avisa si usa colores de fuera.

| Material | Contorno | Sombra | Base | Luz / brillo |
| --- | --- | --- | --- | --- |
| Pan | `oxido` | `canela` | `piel` | `tostado` / `crema` |
| Carne perfecta | `negro` | `cafe-oscuro` | `cafe` | `canela` / `piel` |
| Carne cocinándose | `cafe-oscuro` | `cafe` | `canela` | `piel` / `piel-clara` |
| Carne cruda | `ciruela` | `magenta` | `rosa` | `piel-clara` / `blanco` |
| Carne quemada | `negro` | `noche` | `pizarra` | `gris-azul` |
| Queso | `canela` | `ambar` | `amarillo` | `vainilla` |
| Lechuga | `verde-noche` | `verde-oscuro` | `lima` | `verde-claro` / `pistacho` |
| Tomate | `rojo-oscuro` | `rojo-oscuro` | `rojo` | `coral`; semillas `tostado` |
| Cebolla | `ciruela` | `magenta` | `piel-clara` | `blanco` |
| Cátsup | `cafe-oscuro` | `rojo-oscuro` | `rojo` | `rosa` |
| Mostaza | `oxido` | `tostado` | `ambar` | `amarillo` |
| Mayonesa | `canela` | `durazno` | `crema` | `blanco` |
| Metal (plancha, tapas) | `negro` | `noche` | `pizarra` | `gris-azul` → `gris` |
| Madera (barra) | `cafe-oscuro` | `cafe` | `canela` | `piel` |
| Pared y fondo | `negro` | `noche` | `pizarra` | `azul-oscuro` |
| Piel (clientes) | `cafe` | `canela` / `piel` | `piel` / `piel-clara` | `crema` |
| Avisos (UI) | — | — | `alerta`, `cian`, `azul` | — |

Algunas rampas comparten colores (pan y madera, tomate y cátsup). Se distinguen por forma, textura y posición, y la base de cada una es distinta.

Con el inventario completo se agregaron rampas para `ceramica` (plato), `acento` (flecha), `corazon`, `contorno`, `pelo-oscuro` y `pelo-claro`, y `ropa-azul`, `ropa-roja`, `ropa-verde` y `ropa-morada` (clientes). La lista completa vive en `RAMPS`.

### Definición de un sprite

```ts
// src/game/sprites/ingredients.ts
export const carne = defineSprite({
  id: 'carne',
  size: [32, 6],
  colors: { o: 'cafe-oscuro', b: 'cafe', h: 'canela' },
  pixels: `
    ....oooooooooooooooooooooooo....
    ..oobbbbbhhbbbbbbbbbbbbbbhbboo..
    .obbbbbbbbbbbbbhbbbbbbbbbbbbbbo.
    .obbbbhbbbbbbbbbbbbbbbbbhbbbbbo.
    ..oobbbbbbbbbbbbbbbbbbbbbbbboo..
    ....oooooooooooooooooooooooo....
  `,
  variants: {
    perfecta: {},
    cruda: { o: 'ciruela', b: 'magenta', h: 'rosa' },
    quemada: {
      colors: { o: 'negro', b: 'noche', h: 'pizarra' },
      patch: { 2: '.obbbbbbobbbbbbbhbbbbbobbbbbbbo.' },
    },
  },
});
```

Reglas del formato:

- `.` es siempre transparente. Las demás letras se declaran en `colors` y apuntan a **nombres** de la paleta global, nunca a hex sueltos.
- `size` es `[ancho, alto]` y sirve de comprobación: cada fila debe medir el ancho y debe haber tantas filas como el alto. La sangría y las líneas vacías al inicio y al final se ignoran.
- `variants` cambia colores (`colors` o directamente las letras), reemplaza filas concretas (`patch`, por índice de fila) o sustituye la matriz completa (`pixels`). El `patch` sirve para diferencias pequeñas de forma: las grietas de la carne quemada o la boca y las cejas de un cliente enojado.
- `frames` en lugar de `pixels` define una animación: una lista de matrices del mismo tamaño (humo, chispas, el bote apretado).
- `mirror: 'x'` permite escribir solo la mitad izquierda de un sprite simétrico (pan, plato, botes). El motor completa la otra mitad, y así cuesta la mitad de tokens.
- Las piezas grandes se arman con **módulos repetibles**: la plancha es un extremo, tres lugares iguales y otro extremo. Así no se escribe una matriz enorme.

### Fondos con tiles

Los fondos no se dibujan pixel por pixel. Se usan tiles de 20 × 20 (valor inicial; 320 × 200 son 16 × 10 tiles, y 180 × 280 son 9 × 14) y un mapa de letras:

```ts
// src/game/sprites/tiles.ts
export const cocinaHorizontal = defineTilemap({
  tileSize: 20,
  tiles: { p: 'pared', a: 'azulejo', b: 'azulejo_borde', m: 'madera', s: 'mostrador' },
  map: `
    pppppppppppppppp
    aaaaaaaaaaaaaaaa
    …
    mmmmmmmmmmmmmmmm
  `,
});
```

Cada tile es un sprite normal de 20 × 20 (pared, azulejo, madera, mostrador, ventana…). Con 8 a 10 tiles se arman los fondos horizontal y vertical.

## Del texto a la pantalla

```text
definiciones de texto ──► validación y estilo ──► atlas (una sola imagen, una vez) ──► un elemento por sprite en el DOM
```

- **Atlas**: al arrancar el juego, `bakeAtlas` (`atlas.ts` + `bake.ts`) dibuja todos los sprites, variantes y cuadros a escala 1 en **un solo canvas**, acomodados en filas, y lo exporta como **PNG** en memoria (`toDataURL`). No hay archivos de imagen en el servidor ni descargas. Las variantes idénticas (por ejemplo, `carne:perfecta` y `carne`) comparten el mismo lugar. Cada sprite queda como una entrada `{ x, y, ancho, alto, cuadros }`.
- **Un elemento por sprite, no por pixel**: en el DOM, cada pieza es un `<button>` o un `<div>` cuyo fondo es el atlas, recortado con `background-position` (`atlasStyle`) y con `image-rendering: pixelated`. La cocina sigue la escala entera del escenario; los clientes se muestran 1.5 veces más grandes para mantener su proporción respecto al plato. Las animaciones mueven el recorte de un cuadro a otro.
- **Por qué PNG y no SVG**: el navegador escala una imagen rasterizada casi gratis y GSAP la mueve en la tarjeta de video. Un SVG serían cientos de rectángulos por sprite, puede dejar líneas finas entre pixeles a escalas no enteras y cuesta más animarlo. El SVG solo se usa en el respaldo sin JavaScript.
- **Coste medido con el set ancla**: las definiciones pesan unos 1 KB comprimidas (frente a unos 4,5 KB que pesarían las imágenes ya hechas) y el atlas de 230 × 39 px, con 11 entradas en 9 lugares, pesa unos 2,3 KB y se genera en unos pocos milisegundos, una sola vez.
- **Respaldo sin JavaScript**: la imagen fija de la sección se genera durante la compilación de Astro con los mismos datos, como SVG con un rectángulo por cada tramo horizontal del mismo color. No hay un asset aparte que mantener.

## Herramientas

| Herramienta | Uso |
| --- | --- |
| `validate.ts` · `validateSprite` | **Errores**: ancho de filas, tamaño declarado, letras sin color, colores o materiales que no existen, cuadros de distinto tamaño, parches fuera de rango y tiles faltantes. |
| `validate.ts` · `lintSprite` | **Guía de estilo**: colores fuera de las rampas de los materiales declarados (`materials`), letras declaradas sin usar y dirección de la luz (dentro de cada material, los tonos claros deben quedar arriba a la izquierda de los oscuros; los colores que comparten dos materiales del sprite se excluyen de esta comparación). Las pruebas fallan si un sprite registrado no la cumple. |
| Página de revisión | `/sprites` en el servidor de `pnpm dev` (`src/dev/sprites.astro`, inyectada solo en desarrollo desde `astro.config.mjs`; no entra en la compilación). Muestra cada sprite y variante a ×1, ×3 y ×6 sobre la pared y la barra, desde el atlas, con animaciones en bucle, errores y avisos de estilo, una pila de prueba, el atlas completo y la paleta. Al editar el texto se recarga. |
| Ida y vuelta con Aseprite | Cada variante tiene un botón **PNG** que descarga la tira a escala 1. En la sección **Importar PNG** de `/sprites` se suelta un PNG y `convert.ts` lo pasa a texto: ajusta cada color al más cercano de Endesga 64 (y avisa cuántos pixeles cambió), separa los cuadros según el ancho indicado y, si el id ya existe, conserva sus letras. Sin dependencias: el navegador lee el PNG. La definición resultante se copia a `src/game/sprites/`. |

## Guía de estilo

Estas reglas aplican tanto a quien escribe los sprites como al agente que los genere:

- **Estilo**: 16-bit con flat shading y sel-out, paleta Endesga 64 (ver «Estilo y paleta»).
- **Vista**: frontal elevada 3/4 para todo lo de cocina: cada objeto muestra su cara de arriba (luz), su frente (base) y su costado derecho (sombra). En la pila, cada capa tapa la cara de arriba de la anterior y asoma por la orilla. La carne de la plancha es el mismo sprite que en la hamburguesa.
- **Luz** desde arriba a la izquierda: el tono claro va en los bordes superior e izquierdo y el oscuro abajo.
- **Contorno selectivo** de 1 px, en el tono más oscuro de la rampa de cada material (no negro puro). Del lado de la luz puede aclararse un tono.
- **Rampas**: Grupos de tonos por material (sombra, base, medios tonos y luz) más un brillo puntual, sin dithering, salvo para texturas puntuales (ajonjolí, grietas). Los brillos son uno o dos pixeles.
- **Proporciones**: los ingredientes mantienen sus anchos nativos (pan 24, carne 27, lechuga 28 px) para que la pila quede limpia. El queso y la lechuga pueden sobresalir 1 px por lado.
- **Legibilidad**: cada estado importante se distingue por forma además de color (carne quemada oscura con humo y aviso de descarte).
- **Personalidad**: apetitosa y algo caricaturesca, con colores saturados pero no neón.

### Instrucciones para el agente que genera sprites

1. Leer esta guía y `palette.ts`. Usar solo nombres de color existentes y declarar `materials` con las rampas de `RAMPS`. Si falta una rampa, proponerla primero ahí.
2. Partir del set ancla aprobado (pan base, carne, queso y un bote) como referencia de proporciones y sombreado.
3. Escribir primero la variante base. Las demás se crean con `colors` o `patch`, no con matrices nuevas, salvo que la forma cambie mucho.
4. Usar `mirror` en sprites simétricos y módulos en piezas grandes.
5. Registrar el sprite en `index.ts`, ejecutar `pnpm test` (valida y revisa el estilo de todos los sprites registrados) y revisar el resultado en `/sprites` antes de darlo por terminado.

## Inventario

Tamaños en pixeles lógicos dentro del escenario de 320 × 200 (sprite completo en 3/4; el grosor de cada capa de la pila está en `INGREDIENTS.height`).

**Escala única.** Todo lo de comer mide lo mismo en el plato, en las bandejas y en la plancha: pan de radio 12 (24 de ancho), carne 12.5 (cruda 13), rodajas 10.5, hoja de lechuga 13, rebanada de queso 20 × 20, salsa 9 y plato 15. Las constantes están en `scripts/sprites/gen34.py` (`BUN_R`, `PATTY_R`…). Los grosores de la pila (`height` en `ingredients.ts`) siguen a los sprites.

| Sprite | Tamaño | Variantes, cuadros y uso |
| --- | --- | --- |
| `pan_base` · `pan_medio` · `pan_tapa` | 24 × 16 · 24 × 15 · 24 × 16 | Miga clara arriba en los panes cortados; domo dorado con ajonjolí en el de arriba, que también es el ícono de la casilla de pan |
| `carne` | 27 × 17 | `cruda`, `cocinandose`, `perfecta` y `quemada`, con costra y brillos |
| `queso` · `lechuga` | 24 × 15 · 28 × 16 | Queso cuadrado con esquinas que escurren; lechuga ondulada con venas |
| `tomate` · `cebolla` | 22 × 13 · 22 × 12 | Tomate con semillas; cebolla con aros |
| `salsa` | 20 × 13 | Mancha con gotas; `catsup`, `mostaza` y `mayonesa` |
| `bote` | 16 × 42 | 2 cuadros (normal y apretado); `catsup`, `mostaza` y `mayonesa`; hombro ovalado, tapa baja y boquilla fina, ancla 8/38 y sombra de apoyo |
| `plato` | 38 × 22 | Plato con borde (radio 19 y mayor margen alrededor del pan de 24); su ancla es el centro de la superficie donde se apoya la pila |
| `charola` | 42 × 27 | Bandeja gastronorm más ancha y rectangular (38 × 22) con carne molida cruda, sin forma: un montón con grumos que sobresale al centro, con hebras, surcos y algo de grasa. La forma de medallón aparece hasta que la carne llega a la plancha. Lleva su etiqueta «Carne» |
| `plancha` · `plancha_v` | 118 × 35 · 90 × 35 | Plancha de restaurante: placa de acero curtido por el uso (donde van las carnes, la grasa requemada la deja casi negra; alrededor, un halo más claro en grupos de tonos y, entre lugares y en las orillas, acero limpio con vetas de brillo), salpicadera, rieles, canal de grasa y panel frontal con una perilla bajo cada lugar. Hay una por disposición porque cambia el ancho. Un lugar apagado oscurece solo la zona de la placa (filas 6 a 24 del sprite), no la salpicadera ni el panel |
| `bandeja_pan` · `_queso` · `_lechuga` · `_tomate` · `_cebolla` | 36 × 25–28 | Bandejas gastronorm de acero (esquinas redondeadas, orilla ancha, costados que se angostan y veta de brillo) llenas hasta arriba. Lechuga, tomate y cebolla usan **los mismos sprites del plato**: `gen34.py` genera la bandeja vacía, pega encima los sprites `lechuga`, `tomate` o `cebolla` (tabla `FILL`: sprite y desfase desde el centro de la orilla, de atrás hacia adelante) y vuelve a pintar el frente de la bandeja para que tape la parte de abajo de las piezas (tres hojas; dos rodajas). Pan y queso van en **pilas ordenadas** modeladas en 3D a la misma escala: tres bollos con el domo con ajonjolí arriba, y siete rebanadas cuadradas apenas movidas para que se vean todas las orillas. Son las casillas; el frente liso mide 9 filas para que la etiqueta de cinta masking (HTML, 7 filas) quede centrada con margen arriba y abajo. Cada cinta tiene su propia inclinación y un pequeño desfase |
| `basura` | 42 × 25 | Abertura a la izquierda de la plancha, con un labio de acero elevado y sombra de contacto y bolsa negra doblada sobre la orilla (un bote parado sobre la barra se veía raro). Con carne quemada el bote no cambia de color: por CSS se le pone un contorno pixelado alrededor de todo el hueco, sin degradados: `drop-shadow` sin desenfoque desplazados exactamente 1 pixel del juego, que alterna a saltos entre contorno rojo y contorno doble con rojo oscuro (fijo con movimiento reducido) |
| `cliente` | 96 × 120 | Doce retratos aprobados en Endesga 64, con nombres, estilos y perfiles alternados; un cuadro de espera por variante. Inés conserva la escala al 85 %. Sin escala adicional respecto al entorno. |
| `humo` | 8 × 8 | 4 cuadros; `blanco` (carne por quemarse) y `negro` (quemada) |
| `flecha` | 9 × 8 | Flecha del tutorial |
| `corazon` | 7 × 6 | `lleno` y `vacio` (vidas) |
| `azulejo` · `madera` | 20 × 20 | Tiles que se repiten en la pared y en la barra |

Los sprites de cocina se generaron con `scripts/sprites/` (ver su README): cada objeto se modela con vóxeles y se proyecta con la cámara 3/4; el sombreado sale de las caras (arriba = luz, frente = base, derecha y contacto = sombra), con contorno selectivo, texturas por material (costra de la carne, venas de la lechuga, semillas del tomate, ajonjolí con sombra) y limpieza de escalones. Cada sprite trae un **ancla** (`anchors.ts`): la posición de su base, con la que la vista apila los ingredientes sobre el centro del plato; `INGREDIENTS.height` es el grosor en pantalla de cada capa. 

Los clientes activos proceden de la tanda nativa aprobada y su revisión de proporciones del 3 de noviembre. La fuente editable y autónoma es `scripts/sprites/customers-native.json`; `customers_gen.py` y `write_people.py` regeneran `people.ts` sin las propuestas ni Pillow. Se preservan las celdas de los dibujos, la menor escala de Inés y las orientaciones alternadas; solo se convierte el color a Endesga 64. La fuente anterior de 24 clientes se conserva en `customers-approved.json`.

Las casillas son bandejas de metal con su ingrediente y una etiqueta de cinta masking. **Todo el texto del juego usa [Pixelify Sans](https://fonts.google.com/specimen/Pixelify+Sans)** (Google Fonts, pesos 400–700). Es pixelada pero sin cuadrícula estricta, así que se escala libre y el texto va a «medio pixel» del juego: tamaño 6 × escala (trazo de 0.6 pixeles del juego, mayúsculas de 3.8, interlineado de 6.5) y títulos al doble en negrita. El texto normal va en 500 y las cintas en 600. Se descartaron Bytesized (demasiado chica) y Tiny5: las fuentes de cuadrícula estricta tienen que ir a 1 pixel de la fuente = 1 del juego y quedan enormes y anchas. La comanda, el globo de texto y los indicadores se hacen con HTML y CSS en colores de Endesga 64. Las piezas rectangulares (plancha y bandejas) se generan sin el giro de cámara de 12° para que queden alineadas con la cuadrícula del juego.

## Renovación aplicada · 3 de noviembre · Endesga 64

Los 12 clientes nativos aprobados son ahora el elenco de producción y la referencia artística del conjunto. Conservan sus celdas, sus proporciones (Inés al 85 %) y los perfiles alternados. Se convierten únicamente sus colores a Endesga 64. Cada variante conserva un retrato de espera; las expresiones adicionales no forman parte de esta tanda.

El comedor se rediseñó a partir del acabado de los clientes: marcos rectangulares finos de acero rojo oscuro, cristal gris, pared de yeso neutro, concreto pulido y tapizado con costuras. La pared sigue continua, con barra blanca adosada, tres sillas en horizontal y dos en vertical. Cada orientación tiene una composición propia. Las referencias generadas se redujeron a 320 × 122 y 180 × 200, se asignó un único color Endesga64 a cada celda sin tramado y se guardaron como maestros PNG nativos. La barra de trabajo conserva azulejos rojos y juntas rectas, con un canto fino de acero. Los alimentos y utensilios conservan sus dimensiones, anclas e interacciones; la carne cruda usa tonos rosados y la mayonesa una rampa clara con sombra coherente. Los botes mantienen dos cuadros nativos.

Cliente y entorno usan exactamente la misma escala entera del atlas, sin ampliación adicional del personaje. Las 161 pruebas y la compilación verifican la paleta oficial, la importación de sus 64 tonos, las matrices, el atlas, las posiciones, las variantes y las reglas del juego. La revisión visual comprende los doce clientes en ambas composiciones y el arranque y la pausa del juego principal. Capturas en `design-proposals/endesga64-unified-2026-11-03/`. Sigue pendiente la revisión en teléfono físico.

## Refinamiento de barra y cocina · 3 de noviembre

La cocina recibe el mismo tratamiento de material que el comedor y los clientes: pan con miga porosa y costra tostada, carne con sellado y brillos de grasa, queso con pliegues leves, lechuga con nervaduras y zonas plegadas, tomate con cámaras de pulpa y semillas, cebolla con anillos fríos y salsas con un reflejo de superficie espesa. Los frentes de acero de bandejas y plancha tienen bandas de reflexión y sombra lateral. `gen34.py` conserva todas las dimensiones, siluetas y anclas; las texturas de las pilas de ingredientes se calculan en coordenadas locales.

La barra del jugador incorpora profundidad de vidriado rojo, reflejos agrupados, juntas rectas y una encimera fina de acero cepillado. `counter_gen.py` genera los dos maestros nativos sin remuestreo; `environment_gen.py` los convierte a texto. Los fondos del comedor y los clientes aprobados se conservan exactamente. Las rampas solo añaden colores de la paleta oficial Endesga64. Revisión en ambas composiciones, 161 pruebas y compilación correctas; comparación y ampliaciones en `design-proposals/kitchen-detail-2026-11-03/`.

## Espacio de trabajo y botes · 3 de noviembre

El plato nativo crece a 38 × 22, con ancla 19/11, sin ampliar el pan ni los demás ingredientes. La escena horizontal pasa a 320 × 212 y la vertical a 180 × 300. Las barras crecen a 320 × 90 y 180 × 100, con encimeras de 28 y 36 filas para dejar margen al plato. Bandejas, plancha y zonas de toque bajan coordinadamente; la pared y los clientes se mantienen. La basura es una abertura de 44 × 18 empotrada en la encimera, con espacio para una carne completa, y ya cabe con su profundidad completa en móvil. Los botes de salsas conservan 14 × 35 y dos cuadros, ahora sin etiquetas, con hombros redondeados, tapa estriada y sombreado cilíndrico.

En la revisión final, la versión compacta de 16 × 33 se sustituyó por salseros alargados de 16 × 42, con ancla 8/38. La tapa se aplana y estrecha y la boquilla pasa a ser fina; el hombro ovalado, los reflejos curvos y la sombra de apoyo conservan el volumen. Se mantienen dos cuadros y las tres variantes Endesga-64. Las zonas de interacción de ambas disposiciones se ajustan al tamaño nativo con dos celdas de separación y la misma posición de apoyo. Revisión final en `design-proposals/sauce-dispensers-2026-11-03/`; la versión compacta queda como historial en `design-proposals/sauces-volume-2026-11-03/`.

Comprobado en ambas composiciones y en una partida móvil a 390 × 844, con escala común de 2×. No se solapan el plato, la basura ni las bandejas. 161 pruebas y compilación correctas; sin errores nuevos de consola tras recargar. La revisión está en `design-proposals/mobile-worktop-2026-11-03/`.

## Acero y plancha de tres quemadores · 3 de noviembre

La encimera refleja la luz en bandas continuas con cepillado fino; todos los tonos siguen siendo Endesga64. La basura está del lado del cocinero, a la izquierda de la plancha, sin bloque metálico añadido. Su labio de acero sobresale ligeramente y proyecta una sombra corta. Las planchas se reducen a tres quemadores (118 × 35 y 90 × 35), con perillas redondas de 7 × 7 e indicador claro. Las carnes y barras de cocción quedan por encima de los controles.

Los tres lugares están activos desde el primer cliente y se mantienen durante todos los niveles; no hay desbloqueos progresivos. Comprobado con tres carnes simultáneas en una partida móvil y con pruebas de configuración y sesión. 161 pruebas y compilación correctas. Capturas y auditoría en `design-proposals/steel-three-burners-2026-11-03/`.

## Balance de la zona de preparación · 3 de noviembre

La basura pasa a 42 × 25, más cuadrada y con el mismo tamaño y altura que la charola de carne. Las dos flanquean la plancha con margen igual. Plancha, conjunto inferior, plato y fila de ingredientes comparten un eje central (160 en horizontal, 90 en vertical). La fila del pan queda contenida dentro del ancho del conjunto inferior. El borde elevado se mantiene y los tres quemadores conservan su tamaño, perillas y disponibilidad. 161 pruebas y compilación correctas; comprobaciones de posiciones reales en navegador en `design-proposals/balanced-prep-2026-11-03/`.

El acabado final añade facetas y pliegues grises a la bolsa negra del interior. La encimera adopta la base gris azulada de la placa inferior de la puerta y el frontal de la plancha, con reflejos estrechos y cantos sombreados. Todos los tonos pertenecen a Endesga-64. Revisión del metal en `design-proposals/matched-steel-2026-11-03/` y de la bolsa en `design-proposals/bright-steel-liner-2026-11-03/`.

## Historial anterior · no describe el estado vigente

La siguiente información documenta iteraciones previas. La dirección vigente es Endesga64 y los doce clientes nativos descritos arriba.


- El comedor y la barra usan cuatro sprites completos en el atlas (`environment.ts`): `comedor` 320 × 122, `comedor_v` 180 × 200, `barra_roja` 320 × 78 y `barra_roja_v` 180 × 80. Comedor industrial cartoon rojo/blanco, pared cercana con barra adosada y sillas vistas de espaldas, concreto pulido y barra de azulejo rojo con juntas rectas. La vista vertical tiene composición propia. `scripts/sprites/environment_gen.py` genera estas matrices sin tocar objetos finales. Los tiles antiguos se conservan como referencias de desarrollo; ya no se usan como fondo del juego.
- El elenco de 24 clientes quedó aprobado e integrado como matrices de texto. Las comprobaciones conservan el dibujo de espera píxel por píxel y limitan las reacciones a la cara. Verificación en escritorio y móvil simulado de 390 × 844; 160 pruebas y compilación correctas. Capturas en `design-proposals/applied-customers/`.
- Ajustar el tamaño de tile si 20 px no encaja bien con las piezas del escenario.

### Entorno aplicado

El atlas conserva los mismos sprites finales de cocina y clientes. La vista coloca primero el comedor, después cliente y barra, y encima los controles; comedor y barra son decorativos, no capturan puntero ni foco. Se quitaron los bordes y sombras CSS de la barra antigua para no desplazar ni duplicar la geometría dibujada. La cocina mantiene su escala nativa. Los clientes de 64 × 80 se presentan en un rectángulo de 96 × 120 (150 %) para que el torso sea mayor que el plato, conservando la cintura (fila 76) en el borde de la barra. El indicador de paciencia se mueve sobre las cabezas en ambas orientaciones. Comprobado en escritorio, móvil simulado de 390 × 844 y tamaño intermedio de 1024 × 768. Capturas en `design-proposals/customer-composition-2026-11-01/`.

Validación: sprites, paleta y cobertura opaca de ambos escenarios mediante pruebas; revisión en navegador de escritorio y móvil simulado, incluyendo una orden completa del tutorial. Falta revisión táctil en teléfono físico. La comanda y las ayudas ocultan parte del comedor según el estado, sin alterar las posiciones de los controles existentes.

### Simplificación del comedor

Se redujo el escenario horizontal de ocho mesas a dos conjuntos separados (dos bancos, dos mesas y cuatro sillas). El vertical también conserva solo dos conjuntos completos. Se mantiene la altura común de asiento, tablero y respaldo, y las sillas opuestas a cada banco. Las caras laterales visibles se eligen según el lado del local; se añadieron paneles de cojín y se redujeron costuras, accesorios y marcas del concreto para mejorar la lectura. El centro queda libre detrás del cliente. Revisión en navegador con interfaz real en escritorio y móvil simulado; 159 pruebas y compilación correctas.

### Fondo frontal de barra a pared (dirección vigente)

Se retiró todo el mobiliario anterior en perspectiva: mesas, bancos y sillas laterales. La pared se aproxima al jugador (su base baja de 62 a 91 píxeles en horizontal y de 116 a 140 en vertical), reduciendo el suelo visible. Una barra continua bajo las ventanas tiene tres sillas de espaldas en horizontal y dos en vertical; todas miran hacia la pared. Sus respaldos, patas y reposapiés usan proporciones y alineaciones comunes. Se conservan las ventanas, lámparas, puerta de vidrio con marco rojo y concreto pulido; la puerta tiene altura ajustada a la pared más próxima. La barra de preparación del jugador y los sprites finales no cambian. Esta dirección sustituye las distribuciones de comedor descritas en las dos secciones anteriores.

Ajuste final de intimidad: la base de la pared baja a 97 px en horizontal y 152 px en vertical, con ventanas, puerta, barra y sillas desplazadas de forma coordinada. La barra adosada ahora tiene superficie blanca y canto gris claro; la barra roja de preparación se conserva. Pruebas (159) y compilación correctas; revisión visual en navegador de escritorio.

Último ajuste: pared continua de borde a borde, sin caras ni franjas grises laterales. Base de pared a 102 px en horizontal y 160 px en vertical. Barra blanca con superficie superior y canto lateral en tres cuartos; sillas mirando hacia la pared con giro suave, asiento con profundidad y cuatro patas proyectadas en posiciones distintas. Se mantienen las tres sillas horizontales y dos verticales, sin añadir mobiliario. Revisión en navegador de escritorio/móvil simulado; 159 pruebas y compilación correctas.

Ajuste de las sillas: se recuperó la silueta anterior del respaldo acolchado (esquinas redondeadas, costura inferior y brillos originales), manteniendo la profundidad del asiento, el canto lateral y las cuatro patas del giro en tres cuartos. El resto del fondo se conserva. 159 pruebas y compilación correctas; revisión visual en el juego.

Perspectiva central: los extremos de profundidad de la barra convergen hacia el centro del escenario. Las dos sillas de la izquierda giran hacia la derecha y la derecha hacia la izquierda, manteniendo el modelo acolchado. La sombra de cada silla se centra en el promedio de los cuatro puntos proyectados de contacto, con sombra puntual bajo cada pata; no se usa una elipse fija desplazada. Los apoyos de la barra llegan al suelo, tienen pie visible y sombra de contacto. Mismo criterio en vertical (una silla a cada lado). Revisión visual de ambos formatos, 159 pruebas y compilación correctas.
