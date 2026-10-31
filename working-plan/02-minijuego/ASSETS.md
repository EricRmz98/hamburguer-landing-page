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
- **Vista**: frontal con una ligera elevación, la misma para todo. Los ingredientes se ven de lado, como en una pila. La carne de la plancha es el mismo sprite que en la hamburguesa, para que el paso de uno a otro sea continuo.
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

Tamaños en pixeles lógicos dentro del escenario de 320 × 200. Ancho y alto de los ingredientes coinciden con los de `INGREDIENTS`, que usa la pila del plato.

| Sprite | Tamaño | Variantes, cuadros y uso |
| --- | --- | --- |
| `pan_base` · `pan_medio` · `pan_tapa` | 32 × 8 · 32 × 6 · 32 × 14 | Pan de arriba en domo con ajonjolí; también es el ícono de la casilla de pan |
| `carne` | 32 × 6 | `cruda`, `cocinandose`, `perfecta` y `quemada` (con grietas) |
| `queso` · `lechuga` | 34 × 5 | Sobresalen 1 px por lado |
| `tomate` · `cebolla` | 30 × 3 | |
| `salsa` | 30 × 3 | `catsup`, `mostaza` y `mayonesa`, con gotas |
| `bote` | 16 × 32 | 2 cuadros (normal y apretado al poner salsa); `catsup`, `mostaza` y `mayonesa` |
| `plato` | 48 × 8 | En espejo |
| `charola` | 38 × 18 | Charola con tres carnes crudas |
| `basura` | 26 × 25 | `alerta` (tapa roja) cuando hay carne quemada |
| `cliente` · `clienta` | 48 × 80 | Hombre y mujer de la cintura para arriba (pelo largo, pestañas y aretes en la mujer), con proporciones reales. 3 cuadros (esperando, feliz, enojado) y 4 looks cada uno (`azul`, `rojo`, `verde`, `morado`; `roja`, `amarilla`, `verde`, `morada`). La cabeza queda por encima de la hamburguesa y la barra tapa la cintura. `CUSTOMERS` alterna los 8 aspectos |
| `humo` | 8 × 8 | 4 cuadros; `blanco` (carne por quemarse) y `negro` (quemada) |
| `flecha` | 9 × 8 | Flecha del tutorial |
| `corazon` | 7 × 6 | `lleno` y `vacio` (vidas) |
| `azulejo` · `madera` | 20 × 20 | Tiles que se repiten en la pared y en la barra |

Los clientes, por su tamaño y detalle, se generaron con un script que traza las formas (cabeza, cuello, torso, pelo), les pone contorno y sombrea cada material con luz desde la izquierda; el resultado es texto en el formato de siempre y se edita igual. Una primera versión de 32 px de ancho con el torso alargado se veía como un poste: lo que da proporciones naturales es el ancho (cabeza de unos 22 px y hombros de 44).

Las casillas de ingredientes muestran un montoncito de 2 a 4 rebanadas apiladas, y la comanda, el globo de texto y los indicadores se hacen con HTML y CSS en colores de Endesga 32.

## Pendientes

- En la disposición vertical la basura queda sobre la pared, junto al cliente, porque la barra no tiene espacio libre; buscarle un lugar en la barra si molesta.
- Los fondos usan tiles repetidos por CSS (azulejo y madera); los mapas de tiles (`defineTilemap`) quedan para cuando el fondo tenga elementos y animaciones.
- Confirmar con los primeros clientes si su calidad como texto es suficiente o si conviene el importador.
- Ajustar el tamaño de tile si 20 px no encaja bien con las piezas del escenario.
