# Sprites como texto

Los sprites del [minijuego](PLAN.md) no son imágenes: son **definiciones de texto**. Cada una declara su tamaño en pixeles, qué color representa cada letra y una matriz de caracteres con el dibujo. La IA (el agente que trabaja en el proyecto) los escribe directamente en el código. Al arrancar, el motor los convierte una sola vez en imágenes y los muestra con un solo elemento HTML por sprite.

Estado: **inventario completo en el juego (F4)**. 20 sprites en `src/game/sprites/` (`ingredients.ts`, `utensils.ts`, `people.ts`, `ui.ts`, `tiles.ts`), registrados en `index.ts`, válidos y conformes a la guía de estilo. Este enfoque sustituye al flujo anterior basado en generar imágenes con IA y normalizarlas, que queda solo como importación opcional.

## Por qué texto

- **Es pixel art real desde el principio**: no hay pixeles falsos, antialias ni colores fuera de la paleta que corregir.
- **Cuesta pocos tokens**: una carne de 32 × 6 son 192 caracteres, y una corrección cambia una línea en vez de regenerar la imagen. Como estimación, todo el inventario del juego ronda los 20 000 caracteres.
- **Consistencia garantizada**: las letras solo pueden apuntar a colores de la paleta global, así que ningún sprite se sale del estilo.
- **Variantes casi gratis**: la misma matriz con otra paleta da otro sprite. La carne cruda, perfecta y quemada, los tres botes y los clientes con distinta ropa salen de una sola definición cada uno.
- **Versionable**: cada cambio de un sprite se ve como un diff legible en Git.
- **Sin descargas**: los sprites viajan dentro del JavaScript del juego, comprimidos con el resto, sin peticiones de imágenes aparte.

## Formato

### Estilo y paleta (decididos)

- **Perspectiva**: **frontal elevada 3/4** (cámara a 32° de altura, girada 12° para que se vea el costado derecho). Se eligió tras comparar la vista lateral original (se veía plana), la 3/4 y la isométrica 2:1 (más profundidad, pero obligaba a reacomodar el escenario en diagonal). Los clientes, el humo y la interfaz se quedan de frente, como es habitual en este estilo.
- **Estilo**: pixel art **16-bit con sombreado plano (flat shading) y contorno selectivo (sel-out)**. Cada material lleva 3 tonos (sombra, base y luz) más un brillo puntual de 1 o 2 pixeles; luz desde arriba a la izquierda; contorno del tono oscuro del propio material, nunca negro; sin dithering en los sprites. Referencia: los íconos de comida de *Stardew Valley*.
- **Paleta**: [Endesga 32](https://lospec.com/palette-list/endesga-32), de **ENDESGA** (creada originalmente para *NYKRA*). Se usan exactamente sus 32 colores, sin agregar otros. La ficha de Lospec no indica licencia; se da crédito al autor en los créditos del sitio.

### Paleta global

Los 32 colores tienen nombre propio en español. Las letras de los sprites apuntan a esos nombres; el hex vive solo en `palette.ts`.

```ts
// src/game/sprites/palette.ts — Endesga 32 (ENDESGA), en el orden de Lospec
export const PALETTE = {
  oxido: '#be4a2f',
  tostado: '#d77643',
  crema: '#ead4aa',
  durazno: '#e4a672',
  canela: '#b86f50',
  cafe: '#733e39',
  'cafe-oscuro': '#3e2731',
  'rojo-oscuro': '#a22633',
  rojo: '#e43b44',
  naranja: '#f77622',
  ambar: '#feae34',
  amarillo: '#fee761',
  'verde-claro': '#63c74d',
  verde: '#3e8948',
  'verde-oscuro': '#265c42',
  'verde-noche': '#193c3e',
  'azul-oscuro': '#124e89',
  azul: '#0099db',
  cian: '#2ce8f5',
  blanco: '#ffffff',
  'gris-claro': '#c0cbdc',
  gris: '#8b9bb4',
  'gris-azul': '#5a6988',
  pizarra: '#3a4466',
  noche: '#262b44',
  negro: '#181425',
  alerta: '#ff0044',
  ciruela: '#68386c',
  magenta: '#b55088',
  rosa: '#f6757a',
  'piel-clara': '#e8b796',
  piel: '#c28569',
} as const;
```

Rampas por material (contorno → sombra → base → luz). Viven en código como `RAMPS` (`palette.ts`): cada sprite declara sus `materials` y la revisión de estilo avisa si usa colores de fuera.

| Material | Contorno | Sombra | Base | Luz / brillo |
| --- | --- | --- | --- | --- |
| Pan | `cafe` | `canela` | `durazno` | `crema` |
| Carne perfecta | `negro` | `cafe-oscuro` | `cafe` | `canela` / `piel` |
| Carne cocinándose | `cafe-oscuro` | `cafe` | `canela` | `piel` / `piel-clara` |
| Carne cruda | `ciruela` | `magenta` | `rosa` | `piel-clara` / `blanco` |
| Carne quemada | `negro` | `noche` | `pizarra` | `gris-azul` |
| Queso | `oxido` | `naranja` | `ambar` | `amarillo` |
| Lechuga | `verde-noche` | `verde-oscuro` | `verde` | `verde-claro` |
| Tomate | `rojo-oscuro` | `rojo-oscuro` | `rojo` | `rosa` |
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
- Las piezas grandes se arman con **módulos repetibles**: la plancha es un extremo, cuatro lugares iguales y otro extremo. Así no se escribe una matriz enorme.

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
- **Un elemento por sprite, no por pixel**: en el DOM, cada pieza es un `<button>` o un `<div>` cuyo fondo es el atlas, recortado con `background-position` (`atlasStyle`) y escalado a un múltiplo entero con `image-rendering: pixelated`. Las animaciones mueven el recorte de un cuadro a otro.
- **Por qué PNG y no SVG**: el navegador escala una imagen rasterizada casi gratis y GSAP la mueve en la tarjeta de video. Un SVG serían cientos de rectángulos por sprite, puede dejar líneas finas entre pixeles a escalas no enteras y cuesta más animarlo. El SVG solo se usa en el respaldo sin JavaScript.
- **Coste medido con el set ancla**: las definiciones pesan unos 1 KB comprimidas (frente a unos 4,5 KB que pesarían las imágenes ya hechas) y el atlas de 230 × 39 px, con 11 entradas en 9 lugares, pesa unos 2,3 KB y se genera en unos pocos milisegundos, una sola vez.
- **Respaldo sin JavaScript**: la imagen fija de la sección se genera durante la compilación de Astro con los mismos datos, como SVG con un rectángulo por cada tramo horizontal del mismo color. No hay un asset aparte que mantener.

## Herramientas

| Herramienta | Uso |
| --- | --- |
| `validate.ts` · `validateSprite` | **Errores**: ancho de filas, tamaño declarado, letras sin color, colores o materiales que no existen, cuadros de distinto tamaño, parches fuera de rango y tiles faltantes. |
| `validate.ts` · `lintSprite` | **Guía de estilo**: colores fuera de las rampas de los materiales declarados (`materials`), letras declaradas sin usar y dirección de la luz (dentro de cada material, los tonos claros deben quedar arriba a la izquierda de los oscuros; los colores que comparten dos materiales del sprite se excluyen de esta comparación). Las pruebas fallan si un sprite registrado no la cumple. |
| Página de revisión | `/sprites` en el servidor de `pnpm dev` (`src/dev/sprites.astro`, inyectada solo en desarrollo desde `astro.config.mjs`; no entra en la compilación). Muestra cada sprite y variante a ×1, ×3 y ×6 sobre la pared y la barra, desde el atlas, con animaciones en bucle, errores y avisos de estilo, una pila de prueba, el atlas completo y la paleta. Al editar el texto se recarga. |
| Ida y vuelta con Aseprite | Cada variante tiene un botón **PNG** que descarga la tira a escala 1. En la sección **Importar PNG** de `/sprites` se suelta un PNG y `convert.ts` lo pasa a texto: ajusta cada color al más cercano de Endesga 32 (y avisa cuántos pixeles cambió), separa los cuadros según el ancho indicado y, si el id ya existe, conserva sus letras. Sin dependencias: el navegador lee el PNG. La definición resultante se copia a `src/game/sprites/`. |

## Guía de estilo

Estas reglas aplican tanto a quien escribe los sprites como al agente que los genere:

- **Estilo**: 16-bit con flat shading y sel-out, paleta Endesga 32 (ver «Estilo y paleta»).
- **Vista**: frontal elevada 3/4 para todo lo de cocina: cada objeto muestra su cara de arriba (luz), su frente (base) y su costado derecho (sombra). En la pila, cada capa tapa la cara de arriba de la anterior y asoma por la orilla. La carne de la plancha es el mismo sprite que en la hamburguesa.
- **Luz** desde arriba a la izquierda: el tono claro va en los bordes superior e izquierdo y el oscuro abajo.
- **Contorno selectivo** de 1 px, en el tono más oscuro de la rampa de cada material (no negro puro). Del lado de la luz puede aclararse un tono.
- **Rampas**: 3 tonos por material (sombra, base y luz) más un brillo puntual, sin dithering, salvo para texturas puntuales (ajonjolí, grietas). Los brillos son uno o dos pixeles.
- **Proporciones**: los ingredientes se alinean a 32 px de ancho para que la pila quede limpia. El queso y la lechuga pueden sobresalir 1 px por lado.
- **Legibilidad**: cada estado importante se distingue por forma además de color (carne quemada agrietada, cliente enojado con cejas y boca distintas).
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
| `bote` | 14 × 35 | 2 cuadros (normal y apretado, con gota); `catsup`, `mostaza` y `mayonesa` |
| `plato` | 31 × 18 | Plato con borde (radio 15, apenas más ancho que el pan de 24 para que asome la orilla); su ancla es el centro de la superficie donde se apoya la pila |
| `charola` | 42 × 27 | Bandeja gastronorm más ancha y rectangular (38 × 22) con carne molida cruda, sin forma: un montón con grumos que sobresale al centro, con hebras, surcos y algo de grasa. La forma de medallón aparece hasta que la carne llega a la plancha. Lleva su etiqueta «Carne» |
| `plancha` · `plancha_v` | 156 × 35 · 134 × 35 | Plancha de restaurante: placa de acero curtido por el uso (donde van las carnes, la grasa requemada la deja casi negra; alrededor, un halo más claro con tramado y, entre lugares y en las orillas, acero limpio con vetas de brillo), salpicadera, rieles, canal de grasa y panel frontal con una perilla bajo cada lugar. Hay una por disposición porque cambia el ancho. Un lugar apagado oscurece solo la zona de la placa (filas 6 a 24 del sprite), no la salpicadera ni el panel |
| `bandeja_pan` · `_queso` · `_lechuga` · `_tomate` · `_cebolla` | 36 × 25–28 | Bandejas gastronorm de acero (esquinas redondeadas, orilla ancha, costados que se angostan y veta de brillo) llenas hasta arriba. Lechuga, tomate y cebolla usan **los mismos sprites del plato**: `gen34.py` genera la bandeja vacía, pega encima los sprites `lechuga`, `tomate` o `cebolla` (tabla `FILL`: sprite y desfase desde el centro de la orilla, de atrás hacia adelante) y vuelve a pintar el frente de la bandeja para que tape la parte de abajo de las piezas (tres hojas; dos rodajas). Pan y queso van en **pilas ordenadas** modeladas en 3D a la misma escala: tres bollos con el domo con ajonjolí arriba, y siete rebanadas cuadradas apenas movidas para que se vean todas las orillas. Son las casillas; el frente liso mide 9 filas para que la etiqueta de cinta masking (HTML, 7 filas) quede centrada con margen arriba y abajo. Cada cinta tiene su propia inclinación y un pequeño desfase |
| `basura` | 32 × 14 | Hueco cuadrado en la barra, al ras, con aro de acero y bolsa negra doblada sobre la orilla (un bote parado sobre la barra se veía raro). Con carne quemada el bote no cambia de color: por CSS se le pone un contorno pixelado alrededor de todo el hueco, sin degradados: `drop-shadow` sin desenfoque desplazados exactamente 1 pixel del juego, que alterna a saltos entre contorno rojo y contorno doble con rojo oscuro (fijo con movimiento reducido) |
| `cliente` · `clienta` | 48 × 80 | Hombre y mujer de la cintura para arriba (pelo largo, pestañas y aretes en la mujer), con proporciones reales. 3 cuadros (esperando, feliz, enojado) y 4 looks cada uno (`azul`, `rojo`, `verde`, `morado`; `roja`, `amarilla`, `verde`, `morada`). La cabeza queda por encima de la hamburguesa y la barra tapa la cintura. `CUSTOMERS` alterna los 8 aspectos |
| `humo` | 8 × 8 | 4 cuadros; `blanco` (carne por quemarse) y `negro` (quemada) |
| `flecha` | 9 × 8 | Flecha del tutorial |
| `corazon` | 7 × 6 | `lleno` y `vacio` (vidas) |
| `azulejo` · `madera` | 20 × 20 | Tiles que se repiten en la pared y en la barra |

Los sprites de cocina se generaron con `scripts/sprites/` (ver su README): cada objeto se modela con vóxeles y se proyecta con la cámara 3/4; el sombreado sale de las caras (arriba = luz, frente = base, derecha y contacto = sombra), con contorno selectivo, texturas por material (costra de la carne, venas de la lechuga, semillas del tomate, ajonjolí con sombra) y limpieza de escalones. Cada sprite trae un **ancla** (`anchors.ts`): la posición de su base, con la que la vista apila los ingredientes sobre el centro del plato; `INGREDIENTS.height` es el grosor en pantalla de cada capa. 

Los clientes, por su tamaño y detalle, se generaron con `people_gen.py`, que traza las formas (cabeza, cuello, torso, pelo), les pone contorno y sombrea cada material con luz desde la izquierda; el resultado es texto en el formato de siempre y se edita igual. Una primera versión de 32 px de ancho con el torso alargado se veía como un poste: lo que da proporciones naturales es el ancho (cabeza de unos 22 px y hombros de 44).

Las casillas son bandejas de metal con su ingrediente y una etiqueta de cinta masking. **Todo el texto del juego usa [Pixelify Sans](https://fonts.google.com/specimen/Pixelify+Sans)** (Google Fonts, pesos 400–700). Es pixelada pero sin cuadrícula estricta, así que se escala libre y el texto va a «medio pixel» del juego: tamaño 6 × escala (trazo de 0.6 pixeles del juego, mayúsculas de 3.8, interlineado de 6.5) y títulos al doble en negrita. El texto normal va en 500 y las cintas en 600. Se descartaron Bytesized (demasiado chica) y Tiny5: las fuentes de cuadrícula estricta tienen que ir a 1 pixel de la fuente = 1 del juego y quedan enormes y anchas. La comanda, el globo de texto y los indicadores se hacen con HTML y CSS en colores de Endesga 32. Las piezas rectangulares (plancha y bandejas) se generan sin el giro de cámara de 12° para que queden alineadas con la cuadrícula del juego.

## Pendientes

- Los fondos usan tiles repetidos por CSS (azulejo y madera); los mapas de tiles (`defineTilemap`) quedan para cuando el fondo tenga elementos y animaciones.
- Confirmar con los primeros clientes si su calidad como texto es suficiente o si conviene el importador.
- Ajustar el tamaño de tile si 20 px no encaja bien con las piezas del escenario.
