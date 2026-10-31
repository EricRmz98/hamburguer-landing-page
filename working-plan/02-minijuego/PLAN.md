# Segunda sección: minijuego de hamburguesas

Crear un minijuego de pixel art en la segunda sección de la landing: el visitante prepara hamburguesas para clientes que llegan al mostrador. La primera partida es un tutorial guiado que termina invitando a pedir la hamburguesa real; quien decide seguir jugando entra en un modo infinito, al estilo del dinosaurio de Chrome, donde cada cliente pide una orden distinta y la dificultad sube hasta que el jugador falla.

Estado: **planeación**. No hay código ni sprites. Este documento reúne las decisiones acordadas, la arquitectura propuesta del motor y los valores iniciales que se afinarán al jugar el prototipo. El formato de los sprites (texto con paleta) y sus herramientas se describen en [ASSETS.md](ASSETS.md).

## Decisiones acordadas

- El juego ocupa la **segunda sección** de la landing. El hero todavía no está definido.
- La mecánica central es la **carne en la plancha**. Todo lo demás (panes, queso, verduras, salsas) se coloca con un solo toque.
- Se toca la carne cruda y pasa a la plancha, que tiene un número limitado de lugares. Hay que vigilarla: si se quema, se toca para descartarla. Cuando está bien hecha, se toca y pasa **en automático** a la hamburguesa, pero solo si la hamburguesa ya está lista para recibirla (como mínimo, con el pan abajo).
- La interacción debe ser rápida y ligera: pocos toques por hamburguesa y nada de controles complejos.
- **Tutorial**: la primera partida es una hamburguesa clásica guiada con flechas y textos. Los tiempos se congelan, así que no se puede fallar. Al entregarla, un cliente de pixel art la recibe y aparecen dos opciones: **«Pídela de verdad»** y **«Seguir jugando»**.
- **Modo infinito**: al seguir jugando llega el siguiente cliente con otra orden. A partir de aquí se puede fallar. La partida continúa hasta perder, y se guarda el récord.
- Las órdenes tienen un **orden de ingredientes lógico**: los panes nunca quedan juntos abajo con los ingredientes encima. Hay variantes de doble, triple y cuádruple carne, y de pan intermedio (tres panes en total).
- Los sprites son **definiciones de texto**: tamaño, letras asignadas a colores de una paleta global y una matriz de caracteres. La IA los escribe directamente con pocos tokens, y las variantes salen cambiando la paleta. El motor los convierte una vez en imágenes al arrancar, con **un elemento HTML por sprite, no por pixel**. Los fondos se arman con tiles. Ver [ASSETS.md](ASSETS.md).
- Lleva **efectos de sonido** de estilo 8 bits.
- El motor es **nativo de HTML/CSS** con la lógica en TypeScript y GSAP, sin una librería de juegos (detalle en la sección «Motor»).

## Flujo de una partida

```text
SECCIÓN VISIBLE ─► pantalla de inicio: cliente esperando + «Jugar»
                     │
                     ▼
               TUTORIAL (tiempos congelados, flechas y textos)
                     │  hamburguesa clásica entregada
                     ▼
         «Pídela de verdad»  ·  «Seguir jugando»
                                   │
                                   ▼
                    MODO INFINITO: cliente 1, 2, 3…
                    (la dificultad sube con cada cliente)
                                   │  se acaban las vidas
                                   ▼
         FIN: clientes atendidos · récord · «Jugar otra vez» · «Pídela de verdad»
```

Quien vuelve a la página y ya terminó el tutorial puede saltarlo (propuesta; ver pendientes).

## Mecánicas

### Plancha (mecánica central)

Una charola de carnes crudas, que nunca se acaba, alimenta la plancha. Al tocarla, una carne ocupa el primer lugar libre. Si la plancha está llena, el toque se rechaza con un sonido y una sacudida.

Cada carne avanza por estados según su tiempo en la plancha:

| Estado | Señales visibles y sonoras | Al tocarla |
| --- | --- | --- |
| Cruda → cocinándose | Color rosado que se oscurece, chisporroteo suave | Nada: un pequeño rebote de «todavía no» |
| **Perfecta** | Color dorado, destello y un «ding»; ventana limitada | Pasa a la hamburguesa si el siguiente paso de la orden es carne; si no, se queda y aparece una pista |
| Quemándose (aviso) | Humo gris y parpadeo | Igual que perfecta (todavía sirve) |
| Quemada | Negra, humo denso, «puf» | Se descarta a la basura y libera el lugar |

Una carne quemada **ocupa su lugar** hasta que se descarta: ese es el castigo natural. El estado no depende solo del color (ver accesibilidad).

Valores iniciales propuestos para el primer cliente del modo infinito: 4 s hasta perfecta, 3 s de ventana perfecta, 1,5 s de aviso y después quemada. La dificultad acorta estos tiempos con un límite inferior.

### Armado

La hamburguesa se arma de abajo hacia arriba sobre el plato. La comanda del cliente muestra la receta como una pila de íconos, con el siguiente paso resaltado.

- Tocar el ingrediente que corresponde lo coloca de inmediato, con una caída corta y un sonido.
- Las salsas se aplican desde los botes de arriba, con una animación de apretar.
- Si se toca un ingrediente que no toca, se rechaza (propuesta; ver pendientes): sacudida, zumbido y una pequeña pérdida de paciencia del cliente. Así no hace falta una mecánica para deshacer o tirar hamburguesas.
- Cuando se coloca el pan de arriba, la orden se entrega sola al cliente.

### Clientes

- Hay un cliente en el mostrador. El siguiente puede asomarse en la fila (opcional).
- Cada cliente llega con su comanda y una **barra de paciencia**.
- Si se entrega a tiempo, el cliente se alegra, sube el contador de clientes atendidos y entra el siguiente.
- Si se le acaba la paciencia, se va enojado y el jugador pierde una vida (propuesta: 3 vidas; ver pendientes).
- Las variaciones de cliente (personajes distintos) dan vida sin añadir mecánicas.

### Puntuación y récord

Como en el dinosaurio de Chrome, el marcador principal es un solo número: **clientes atendidos**. Se muestra junto al récord, que se guarda en `localStorage` y se protege con `try/catch`. Si el almacenamiento no está disponible, el juego funciona igual, solo que sin récord.

### Dificultad (valores iniciales propuestos)

| Clientes | Recetas | Lugares en plancha | Paciencia | Velocidad de cocción |
| --- | --- | --- | --- | --- |
| 1–3 | Sencilla o con queso | 2 | 35 s | ×1,0 |
| 4–7 | Doble carne, más verduras y salsas | 2 | 32 s | ×1,1 |
| 8–12 | Triple carne | 3 | 30 s | ×1,2 |
| 13–20 | Cuádruple o pan intermedio | 4 | 28 s | ×1,3 |
| 21+ | Cualquiera | 4 | baja 0,5 s por cliente hasta 18 s | sube hasta ×1,6 |

Al pasar el último nivel solo se ajustan el tiempo y la velocidad, hasta que el juego se vuelve imposible de sostener, como en el dinosaurio de Chrome. La paciencia de cada cliente se calcula en función del tamaño de su receta, de modo que una cuádruple no resulte injusta.

## Recetas

### Gramática

Cada receta es una pila de abajo hacia arriba que cumple esta gramática:

```text
hamburguesa = pan_base  sección  [ pan_medio  sección ]  pan_tapa
sección     = bloque_carne+  verdura*  salsa*
bloque_carne = carne  [ queso ]
```

Reglas de validación:

1. Empieza con `pan_base` y termina con `pan_tapa`. Puede haber como máximo un `pan_medio`, siempre entre dos secciones (tres panes en total).
2. Cada sección tiene al menos una carne. Hay entre 1 y 4 carnes en total.
3. El queso va siempre directamente sobre una carne.
4. Las verduras (lechuga, tomate, pepinillos, cebolla) van después de la última carne de su sección, sin repetirse dentro de ella.
5. Las salsas (cátsup, mostaza, mayonesa) van al final de la sección, justo antes del siguiente pan. Puede haber como máximo dos por sección.
6. La altura total no supera el límite del plato: 100 px lógicos como valor inicial (ver tamaños en [ASSETS.md](ASSETS.md)).

Las recetas aleatorias del modo infinito se construyen **a partir de la gramática**, nunca combinando ingredientes al azar, así que siempre son válidas. El validador se usa en las pruebas y para revisar las recetas escritas a mano.

### Catálogo inicial

| Receta | Pila (abajo → arriba) | Uso |
| --- | --- | --- |
| Clásica | pan_base · carne · queso · lechuga · tomate · cátsup · pan_tapa | Tutorial y clientes iniciales |
| Sencilla | pan_base · carne · cátsup · mostaza · pan_tapa | Clientes iniciales |
| Doble | pan_base · carne · queso · carne · queso · pepinillos · cebolla · mostaza · pan_tapa | Nivel 2 |
| Triple | pan_base · carne · queso · carne · carne · queso · lechuga · cátsup · pan_tapa | Nivel 3 |
| Cuádruple («la torre») | pan_base · 4 × (carne · queso) · pepinillos · mostaza · pan_tapa | Nivel 4 |
| Tres panes | pan_base · carne · queso · lechuga · pan_medio · carne · queso · pepinillos · mayonesa · pan_tapa | Nivel 4 |

Además del catálogo, el generador crea variantes por nivel. Los nombres son provisionales hasta definir la marca.

## Tutorial

Es un guion de pasos. Cada paso resalta un elemento con una flecha y un texto breve, y solo acepta el toque correcto. Los demás elementos quedan atenuados. Los tiempos de cocción avanzan hasta «perfecta» y se congelan ahí, y la paciencia del cliente no corre.

1. Llega el cliente: «¡Una clásica, por favor!». La comanda aparece resaltada.
2. Flecha a la charola de carne: «Pon la carne en la plancha».
3. Flecha al pan de abajo: «Mientras se cocina, prepara el pan».
4. La carne llega a perfecta y se congela. Flecha: «¡Lista! Tócala y pasa al pan».
5. Queso, lechuga, tomate y cátsup, cada uno con su flecha.
6. Pan de arriba, entrega, cliente feliz.
7. Mensaje final con «Pídela de verdad» y «Seguir jugando».

La carne quemada no aparece en el tutorial. En el modo infinito, **la primera vez** que ocurre algo nuevo (primera carne quemada, primera receta con pan intermedio, plancha que crece) aparece una pista contextual breve y el tiempo se pausa un momento. Cada pista se muestra una sola vez por visitante.

## Disposición del escenario

El juego se dibuja en un escenario de resolución lógica fija que se escala por múltiplos enteros, para que el pixel no se deforme. Hay dos disposiciones con las mismas piezas:

**Horizontal, 320 × 180** (escritorio y tableta)

```text
┌──────────────────────────────────────────────────────────┐
│  [♥♥♥]   CLIENTES 12 · RÉCORD 20                [🔊]    │
│            [CÁTSUP] [MAYONESA] [MOSTAZA]                 │
│  CLIENTE      ┌───────┐        ┌──── PLANCHA ────┐       │
│  + comanda    │ plato │        │ [ ] [ ] [ ] [ ] │ [🗑]  │
│  + paciencia  └───────┘        └─────────────────┘       │
│  [pan base][pan medio][pan tapa][queso][lechuga]…[carne] │
└──────────────────────────────────────────────────────────┘
```

**Vertical, 180 × 320** (móvil): el cliente y la comanda arriba, después los botes, el plato y la plancha en el centro, y los ingredientes abajo, en una cuadrícula al alcance del pulgar.

Las coordenadas de cada pieza se definen en un mapa por disposición. La lógica del juego no conoce posiciones.

## Motor

### Por qué HTML/CSS y no una librería de juegos

El juego tiene posiciones fijas, se controla con toques y no necesita física, colisiones ni muchos objetos en movimiento. Un motor propio pequeño sobre el DOM ofrece:

- Botones reales: el teclado, el foco, el tacto y los lectores de pantalla funcionan sin trabajo extra.
- Animaciones con GSAP, que ya está en la plantilla, y ningún bucle de render adicional.
- Escalado responsive con CSS e integración natural con Astro y Lenis.
- Cero dependencias pesadas en la landing.

Alternativas descartadas por ahora: Phaser o PixiJS (demasiado para este alcance, y obligan a rehacer la accesibilidad dentro de un canvas) y Kaplay o LittleJS (ligeros y buenos para pixel art, pero aquí no aportan nada que el DOM no resuelva). Si el juego llegara a necesitar movimiento libre o colisiones, la lógica se conserva y solo cambia la capa de dibujo.

### Arquitectura propuesta

```text
src/components/MiniGame.astro        Marcado de la sección, HUD y montaje
src/game/
  engine/
    clock.ts       Reloj de juego sobre gsap.ticker: pausa, escala de tiempo y congelamiento
    stage.ts       Escenario lógico, escalado entero y cambio de disposición
    store.ts       Estado del juego y eventos (sin framework)
    input.ts       Toques, teclado y atajos con el juego enfocado
    sprite.ts      Elementos de sprite: imagen horneada, variante y cuadro actual
    audio.ts       Efectos con ZzFX, silencio y desbloqueo con el primer toque
  game/
    grill.ts       Lugares, estados de la carne y temporizadores
    assembly.ts    Pila del plato y aceptación del siguiente paso
    recipes.ts     Gramática, generador por nivel, validador y catálogo
    customers.ts   Llegada, paciencia, entrega y vidas
    difficulty.ts  Curva por número de cliente
    tutorial.ts    Guion de pasos, flechas y congelamiento
    hints.ts       Pistas de primera vez
    session.ts     Máquina de estados: inicio → tutorial → oferta → infinito → fin
  layouts/
    landscape.ts   Mapa de piezas 320 × 180
    portrait.ts    Mapa de piezas 180 × 320
  sprites/
    palette.ts     Paleta global por rampas de material
    define.ts      defineSprite / defineTilemap
    ingredients.ts · utensils.ts · customers.ts · effects.ts · ui.ts · tiles.ts
    validate.ts    Validación de las definiciones
    bake.ts        Texto → canvas → imagen en caché, una sola vez
```

No hay carpeta de imágenes: los sprites viajan dentro del JavaScript del juego.

Principios:

- **La lógica está separada del dibujo.** `game/*` no toca el DOM: emite eventos que la capa visual convierte en animaciones. Así la lógica se puede probar con pruebas unitarias y la mecánica se ajusta sin tocar el arte.
- **Un solo reloj de juego.** Se usa `gsap.ticker`, el mismo que mueve Lenis, con tiempo propio que se pausa. El congelamiento del tutorial y las pausas de las pistas viven en `clock.ts`.
- **Se pausa solo** cuando la sección sale de la vista (IntersectionObserver) o la pestaña se oculta (`visibilitychange`).
- **Pixel nítido.** `image-rendering: pixelated`, escala entera calculada según el ancho disponible, sin transformaciones fraccionarias en los sprites (se redondea a pixeles lógicos).
- **Animación de sprites.** Los estados son variantes de la misma definición (cambio de paleta o `patch`), horneadas por adelantado: cambiar de estado es cambiar la imagen del elemento. El movimiento (caída, rebote, apretar, sacudida) se hace con GSAP. Las animaciones cuadro a cuadro (humo, chispas) son tiras horneadas que se usan con `steps()`.
- **El HUD es HTML.** Marcador, vidas, textos del tutorial y botones finales usan una fuente pixel. Propuestas: Silkscreen, Pixelify Sans o Press Start 2P, de Google Fonts.

### Sonido

Los efectos se sintetizan en el navegador con **ZzFX**, una librería diminuta de efectos 8 bits, de modo que no hay que generar ni descargar archivos de audio. Antes de instalarla se verifican su fuente, su licencia y su versión. Si no convence, se hace lo mismo con Web Audio directamente.

| Evento | Sonido |
| --- | --- |
| Colocar ingrediente | «Tic» corto, con un tono por tipo |
| Carne a la plancha | Chisporroteo que se intensifica mientras se cocina |
| Carne perfecta | «Ding» |
| Aviso de quemándose | Pitidos rápidos |
| Carne quemada / descartar | «Puf» / bote de basura |
| Apretar bote | «Squish» |
| Toque rechazado | Zumbido grave |
| Entrega | Fanfarria corta y moneda |
| Cliente enojado | Gruñido descendente |
| Fin de partida / nuevo récord | Melodía corta |

El audio se activa con el toque de «Jugar», un gesto del usuario que los navegadores exigen. El botón de silencio está siempre visible y se recuerda. No hay música en esta etapa.

### Integración en la landing

- Sección 2 de `src/pages/index.astro`. Fuera de la sección, el scroll de Lenis no cambia. Dentro del escenario se usa `touch-action: manipulation` para que los toques rápidos no hagan zoom.
- El juego se carga cuando la sección se acerca a la vista, para no retrasar la carga inicial.
- Si JavaScript falla, la sección muestra una imagen fija de la hamburguesa con «Pídela de verdad». Esa imagen se genera en la compilación como SVG, a partir de las mismas definiciones de texto.
- «Pídela de verdad» apunta al destino de pedidos de la marca, que está pendiente.

### Accesibilidad

- Cada pieza es un `<button>` con nombre accesible («Carne en lugar 2: perfecta»).
- Teclado: Tab recorre las piezas. Con el juego enfocado, hay atajos de número y letra.
- Una región `aria-live` anuncia solo los eventos clave: cliente nuevo, carne perfecta, carne quemada y entrega.
- El estado de la carne se distingue por color, forma y humo, y también por el sonido.
- Con `prefers-reduced-motion` se quitan las sacudidas y partículas, y las caídas se vuelven instantáneas. La mecánica no cambia.

## Fases de trabajo

- [ ] **F0 · Sprites como texto**: formato `defineSprite`/`defineTilemap`, paleta, validación, horneado, página de revisión y set ancla (pan base, carne, queso y bote). Ver [ASSETS.md](ASSETS.md).
- [ ] **F1 · Núcleo del motor**: escenario y escalado, reloj, store, input y elementos de sprite. Los sprites que aún no existan se muestran como bloques de color.
- [ ] **F2 · Plancha jugable**: estados, temporizadores, descarte y prueba de sensación de los tiempos.
- [ ] **F3 · Armado y recetas**: pila, comanda, gramática, generador, validador y pruebas.
- [ ] **F4 · Clientes y modo infinito**: paciencia, vidas, dificultad, fin de partida y récord.
- [ ] **F5 · Tutorial y pistas**: guion, flechas, congelamiento, oferta final y pistas de primera vez.
- [ ] **F6 · Sonido**: efectos, silencio y desbloqueo de audio.
- [ ] **F7 · Inventario completo de sprites**: el resto de ingredientes, utensilios, clientes, efectos, UI y fondos de tiles, revisados en la página de revisión. El importador de PNG se usa solo si algún sprite lo necesita.
- [ ] **F8 · Integración y revisión**: sección 2, respaldo sin JS, disposiciones horizontal y vertical, accesibilidad, rendimiento y compilación.

F2 es la fase crítica: si la plancha no se siente bien con cuadros de color, el arte no la va a salvar. Conviene jugarla y ajustar los tiempos antes de invertir en sprites.

## Criterios de aceptación

- El tutorial no se puede perder y termina en la oferta con las dos opciones.
- En el modo infinito, la carne pasa sola a la hamburguesa solo cuando el siguiente paso es carne. Una carne quemada bloquea su lugar hasta descartarla.
- Todas las recetas generadas pasan el validador y caben en el plato.
- La dificultad sube de forma perceptible y el juego termina tarde o temprano.
- Se juega con mouse, tacto y teclado. Funciona en 320 × 180 escalado en escritorio y en la disposición vertical en móvil.
- Todas las definiciones de sprites pasan la validación. Cada sprite es un solo elemento en el DOM.
- El pixel se ve nítido en todas las escalas. No hay saltos de layout al entrar ni al salir de la sección.
- El juego se pausa fuera de vista y no consume recursos mientras está pausado.
- La compilación de Astro pasa y las pruebas de `recipes`, `grill` y `difficulty` también.

## Pendientes por decidir

Cada punto tiene un valor propuesto, que se usará si no se indica otra cosa:

1. **Lugares en la plancha**: empezar con 2 y llegar a 4 con la dificultad (propuesto), o un número fijo.
2. **Fin de partida**: 3 vidas que se pierden cuando un cliente se va (propuesto), o un solo error, como en el dinosaurio de Chrome.
3. **Ingrediente equivocado**: rechazarlo con penalización de paciencia (propuesto), o permitirlo y que la entrega salga mal.
4. **Carne quemada**: solo bloquea el lugar (propuesto), o además quita una vida.
5. **Saltar el tutorial** para quien ya lo terminó (propuesto: sí).
6. **Fuente pixel** del HUD.
7. **Marca y destino** de «Pídela de verdad» (nombre, URL o app de pedidos).
8. **Ingredientes extra**: tocino, cebolla caramelizada, aguacate u otros que encajen con la marca.
