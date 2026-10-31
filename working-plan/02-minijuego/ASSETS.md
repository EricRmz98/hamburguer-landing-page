# Sprites como texto

Los sprites del [minijuego](PLAN.md) no son imágenes: son **definiciones de texto**. Cada una declara su tamaño en pixeles, qué color representa cada letra y una matriz de caracteres con el dibujo. La IA (el agente que trabaja en el proyecto) los escribe directamente en el código. Al arrancar, el motor los convierte una sola vez en imágenes y los muestra con un solo elemento HTML por sprite.

Estado: **planeación**. Las rutas, el formato y las herramientas descritas aquí son la propuesta de implementación de la fase F4, que llega después de fijar la mecánica con bloques. Este enfoque sustituye al flujo anterior basado en generar imágenes con IA y normalizarlas, que queda solo como importación opcional.

## Por qué texto

- **Es pixel art real desde el principio**: no hay pixeles falsos, antialias ni colores fuera de la paleta que corregir.
- **Cuesta pocos tokens**: una carne de 32 × 6 son 192 caracteres, y una corrección cambia una línea en vez de regenerar la imagen. Como estimación, todo el inventario del juego ronda los 20 000 caracteres.
- **Consistencia garantizada**: las letras solo pueden apuntar a colores de la paleta global, así que ningún sprite se sale del estilo.
- **Variantes casi gratis**: la misma matriz con otra paleta da otro sprite. La carne cruda, perfecta y quemada, los tres botes y los clientes con distinta ropa salen de una sola definición cada uno.
- **Versionable**: cada cambio de un sprite se ve como un diff legible en Git.
- **Sin descargas**: los sprites viajan dentro del JavaScript del juego, comprimidos con el resto, sin peticiones de imágenes aparte.

## Formato

### Paleta global

```ts
// src/game/sprites/palette.ts
export const PALETTE = {
  'pan-900': '#5b2c12',
  'pan-600': '#c97a2b',
  'pan-300': '#f2b15a',
  'carne-900': '#2a160e',
  'carne-600': '#7a3b22',
  'carne-400': '#b5643a',
  'cruda-800': '#6e2a2a',
  'cruda-500': '#c4585a',
  'cruda-300': '#e8908a',
  'quemada-900': '#141010',
  'quemada-700': '#302824',
  'quemada-500': '#4e423b',
  // …
} as const;
```

Los colores se organizan en **rampas por material** (pan, carne, queso, lechuga, metal, madera, piel…) de 3 o 4 tonos, oscuro a claro. El hex vive solo aquí. El total ronda entre 32 y 48 colores (valor inicial), que se fijan antes de dibujar el set ancla.

### Definición de un sprite

```ts
// src/game/sprites/ingredients.ts
export const carne = defineSprite({
  id: 'carne',
  size: [32, 6],
  colors: { o: 'carne-900', b: 'carne-600', h: 'carne-400' },
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
    cruda: { o: 'cruda-800', b: 'cruda-500', h: 'cruda-300' },
    quemada: {
      colors: { o: 'quemada-900', b: 'quemada-700', h: 'quemada-500' },
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
definición de texto ──► validación ──► horneado (una vez) ──► caché de URLs ──► <img>/<button> en el DOM
```

- **Horneado**: al arrancar el juego, `bake.ts` dibuja cada sprite, variante y cuadro a escala 1 en un canvas invisible con `putImageData`. Lo convierte en imagen (`toBlob` y una URL de objeto) y la guarda en caché con la clave `id:variante`. Las animaciones se hornean como una tira horizontal para usarla con `steps()`. Los fondos de tiles se hornean como una sola imagen de 320 × 200 o 180 × 280.
- **Un elemento por sprite, no por pixel**: en el DOM, cada pieza es un `<button>` o `<img>` con su imagen, escalada por CSS a un múltiplo entero con `image-rendering: pixelated`. Un elemento por pixel produciría decenas de miles de nodos y haría lento el layout y la animación, sobre todo en móvil. Por la misma razón se descarta el truco de `box-shadow` por pixel.
- **Coste**: hornear sprites tan pequeños es prácticamente instantáneo y ocurre una sola vez, antes de mostrar el juego. Si cambia la paleta de una variante durante la partida, ese resultado también se guarda en caché.
- **Respaldo sin JavaScript**: la imagen fija de la sección se genera durante la compilación de Astro con los mismos datos, como SVG con un rectángulo por cada tramo horizontal del mismo color. No hay un asset aparte que mantener.

## Herramientas

| Herramienta | Uso |
| --- | --- |
| `validate.ts` | Comprueba el ancho de las filas, el tamaño declarado, las letras sin definir, los nombres de color que no existen en la paleta, los cuadros de distinto tamaño, los parches fuera de rango y los tiles faltantes. Corre en las pruebas y en la página de revisión. |
| Página de revisión | Solo para desarrollo, excluida de la compilación. Muestra cada sprite y sus variantes a ×1, ×3 y ×6 sobre el fondo del juego, con las animaciones en bucle, los errores de validación, los fondos de tiles y una pila de prueba de cada receta del catálogo. Con el servidor de desarrollo, editar el texto actualiza la vista. |
| Importador PNG → texto (opcional) | `scripts/sprites/import.mjs` convierte una imagen al formato de texto: reduce a la cuadrícula del tamaño indicado, asigna cada color al más cercano de la paleta y asigna letras. Sirve si algún sprite (por ejemplo, un cliente) sale mejor dibujado en Aseprite o generado con IA. Después de importarlo se edita como cualquier otro. Necesita un lector de PNG como dependencia de desarrollo. |

## Guía de estilo

Estas reglas aplican tanto a quien escribe los sprites como al agente que los genere:

- **Vista**: frontal con una ligera elevación, la misma para todo. Los ingredientes se ven de lado, como en una pila. La carne de la plancha es el mismo sprite que en la hamburguesa, para que el paso de uno a otro sea continuo.
- **Luz** desde arriba a la izquierda: el tono claro va en los bordes superior e izquierdo y el oscuro abajo.
- **Contorno** de 1 px, en el tono más oscuro de la rampa de cada material (no negro puro).
- **Rampas**: de 3 a 4 tonos por material y sin dithering, salvo para texturas puntuales (ajonjolí, grietas). Los brillos son uno o dos pixeles.
- **Proporciones**: los ingredientes se alinean a 32 px de ancho para que la pila quede limpia. El queso y la lechuga pueden sobresalir 1 px por lado.
- **Legibilidad**: cada estado importante se distingue por forma además de color (carne quemada agrietada, cliente enojado con cejas y boca distintas).
- **Personalidad**: apetitosa y algo caricaturesca, con colores saturados pero no neón.

### Instrucciones para el agente que genera sprites

1. Leer esta guía y `palette.ts`. Usar solo nombres de color existentes. Si falta una rampa, proponerla primero en la paleta.
2. Partir del set ancla aprobado (pan base, carne, queso y un bote) como referencia de proporciones y sombreado.
3. Escribir primero la variante base. Las demás se crean con `colors` o `patch`, no con matrices nuevas, salvo que la forma cambie mucho.
4. Usar `mirror` en sprites simétricos y módulos en piezas grandes.
5. Ejecutar la validación y revisar el resultado en la página de revisión antes de darlo por terminado.

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

- Fijar la paleta y dibujar el set ancla antes del resto del inventario.
- Confirmar con los primeros clientes si su calidad como texto es suficiente o si conviene el importador.
- Ajustar el tamaño de tile si 20 px no encaja bien con las piezas del escenario.
