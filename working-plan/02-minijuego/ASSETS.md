# Sprites como texto

Los sprites del [minijuego](PLAN.md) no son imágenes: son **definiciones de texto**. Cada una declara su tamaño en pixeles, qué color representa cada letra y una matriz de caracteres con el dibujo. La IA (el agente que trabaja en el proyecto) los escribe directamente en el código. Al arrancar, el motor los convierte una sola vez en imágenes y los muestra con un solo elemento HTML por sprite.

Estado: **F3 en revisión**. El formato (`src/game/sprites/`), la validación, el horneado, la página de revisión y el set ancla (pan, carne, queso y bote) están implementados; falta aprobar el set ancla antes de dibujar el resto del inventario (F4). Este enfoque sustituye al flujo anterior basado en generar imágenes con IA y normalizarlas, que queda solo como importación opcional.

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

## Inventario inicial

Tamaños en pixeles lógicos dentro del escenario de 320 × 200. Son valores iniciales que se ajustarán al ver el set ancla.

### Ingredientes (vista lateral)

| id | Tamaño | Variantes y técnica |
| --- | --- | --- |
| `pan_base` | 32 × 8 | Simétrico (`mirror`) |
| `pan_medio` | 32 × 6 | Simétrico |
| `pan_tapa` | 32 × 14 | Domo con ajonjolí |
| `carne` | 32 × 6 | `cruda`, `cocinandose`, `perfecta` y `quemada` por paleta. La quemada lleva además un `patch` de grietas |
| `queso` | 34 × 5 | Esquinas que escurren |
| `lechuga` | 34 × 5 | Borde ondulado |
| `tomate` | 30 × 3 | |
| `cebolla` | 30 × 3 | |
| `salsa` | 30 × 3 | `catsup`, `mostaza` y `mayonesa` por paleta |

La receta más alta del catálogo (cuatro carnes con queso) mide unos 75 px. El generador de recetas limita la altura total a 100 px (valor inicial) para que la pila quepa sobre el plato en la disposición horizontal. Los íconos de la comanda son los mismos sprites a escala 1, sin definiciones aparte.

### Utensilios

| id | Tamaño | Variantes y técnica |
| --- | --- | --- |
| `bote` | 16 × 32 | 2 cuadros (normal y apretado); `catsup`, `mayonesa` y `mostaza` por paleta; simétrico |
| `plancha` | 4 lugares de 34 × 32 (30 × 33 en vertical) | Módulos: lugar y marco, en fila. `lugar_apagado` por paleta para los que no se usan. El indicador de cocción se hace con CSS, sin sprite |
| `plato` | 48 × 8 | Simétrico |
| `charola_carne` | 32 × 20 | Reutiliza la carne cruda apilada |
| `basura` | 34 × 26 | 2 cuadros (cerrada y abierta); `alerta` por paleta cuando hay carne quemada |
| `casilla` | 34 × 24 | Fondo de los botones de ingrediente; `activa` y `atenuada` (tutorial) por paleta |

### Clientes

Dos o tres cuerpos base de 32 × 48. Cada uno se multiplica por paleta (piel, pelo, ropa) en varios personajes y lleva expresiones `esperando`, `feliz` y `enojado` como `patch` de las filas de la cara. Son los sprites más difíciles de escribir como texto: si la calidad no convence, se dibujan o generan como imagen y se convierten con el importador.

### Fondos (tiles de 20 × 20)

`pared`, `azulejo`, `azulejo_borde`, `madera`, `mostrador`, `ventana` y `estante`, más los mapas `cocina_horizontal` (16 × 10) y `cocina_vertical` (9 × 14).

### Efectos y UI

| id | Tamaño | Variantes y técnica |
| --- | --- | --- |
| `humo` | 8 × 8 | 4 cuadros; `blanco` y `negro` por paleta |
| `chispa` | 4 × 4 | 3 cuadros |
| `destello` | 8 × 8 | 3 cuadros |
| `flecha` | 12 × 12 | El rebote se hace con GSAP |
| `bocadillo` · `comanda` | 24 × 16 | Se estiran con 9-slice (`border-image`) |
| `corazon` | 8 × 8 | `lleno` y `vacio` por paleta |
| `bocina` | 10 × 10 | `con_sonido` y `sin_sonido` por `patch` |

La barra de paciencia y el marcador se hacen con HTML y CSS, sin sprites.

## Pendientes

- Aprobar el set ancla. Primer ajuste ya hecho: la carne perfecta pasó a café oscuro (`cafe` con contorno `negro`) y la rampa anterior quedó para «cocinándose»; el queso escurre más.
- Confirmar con los primeros clientes si su calidad como texto es suficiente o si conviene el importador.
- Ajustar el tamaño de tile si 20 px no encaja bien con las piezas del escenario.
