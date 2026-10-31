# Segunda sección: minijuego de hamburguesas

Crear un minijuego de pixel art en la segunda sección de la landing: el visitante prepara hamburguesas para clientes que llegan al mostrador. La primera partida es un tutorial guiado que termina invitando a pedir la hamburguesa real; quien decide seguir jugando entra en un modo infinito, al estilo del dinosaurio de Chrome, donde cada cliente pide una orden distinta y la dificultad sube hasta que el jugador falla.

Estado: **F1 a F4 listas**. El juego completo ya se dibuja con sprites de pixel art (Endesga 32) en vista 3/4, generados desde texto y horneados en un atlas. Siguen el sonido (F5) y la integración final (F6). Este documento reúne las decisiones acordadas, la arquitectura y los valores iniciales que se afinarán jugando. El formato de los sprites (texto con paleta) y sus herramientas se describen en [ASSETS.md](ASSETS.md).

## Decisiones acordadas

- El juego ocupa la **segunda sección** de la landing. El hero todavía no está definido.
- Cada carne tiene un **indicador de cocción**: amarillo, verde cuando está lista (a la mitad o un poco más) y rojo con parpadeo de señal cuando se está pasando.
- La disposición es una **barra de preparación**, igual en escritorio y móvil: plancha con carnes a la derecha abajo, complementos encima, plato centrado con aderezos a la derecha y comanda a la izquierda. Toda esa zona es la barra, y el cliente está justo del otro lado, recargado en ella (ver «Disposición del escenario»).
- La mecánica central es la **carne en la plancha**. Todo lo demás (panes, queso, verduras, salsas) se coloca con un solo toque.
- Se toca la carne cruda y pasa a la plancha, que tiene un número limitado de lugares. Hay que vigilarla: si se quema, se toca para descartarla. Cuando está bien hecha, se toca y pasa **en automático** a la hamburguesa, pero solo si la hamburguesa ya está lista para recibirla (como mínimo, con el pan abajo).
- La interacción debe ser rápida y ligera: pocos toques por hamburguesa y nada de controles complejos.
- **La dificultad es el tiempo**: cada cliente da menos tiempo para su orden, siempre con la posibilidad de lograrlo. A partir de un tope, el tiempo deja de bajar y todo depende de la habilidad.
- **Tutorial**: la primera partida es una hamburguesa clásica guiada con flechas y textos. Los tiempos se congelan, así que no se puede fallar. Al entregarla, un cliente de pixel art la recibe y aparecen dos opciones: **«Pídela de verdad»** y **«Seguir jugando»**.
- **Modo infinito**: al seguir jugando llega el siguiente cliente con otra orden. A partir de aquí se puede fallar. La partida continúa hasta perder, y se guarda el récord.
- Las órdenes tienen un **orden de ingredientes lógico**: los panes nunca quedan juntos abajo con los ingredientes encima. Hay variantes de doble, triple y cuádruple carne, y de pan intermedio (tres panes en total).
- **Estética**: pixel art 16-bit en **vista frontal elevada 3/4**, con sombreado plano y contorno selectivo, sobre la paleta **Endesga 32** (ver [ASSETS.md](ASSETS.md#estilo-y-paleta-decididos)).
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

Una carne quemada **ocupa su lugar** hasta que se descarta: ese es el castigo natural. Se tira tocándola en la plancha o tocando la **basura**, que tira todas las quemadas de una vez. Cuando hay alguna, la basura se ilumina en rojo con un contorno pixelado que parpadea. El estado no depende solo del color (ver accesibilidad).

**Indicador de cocción.** Cada carne en la plancha lleva una barra que avanza con su cocción. La pista de fondo muestra las tres zonas, para anticipar cuánto falta: amarillo mientras se cocina, verde en la ventana perfecta (empieza a la mitad o un poco más de la barra) y rojo después. En el aviso, la barra parpadea en rojo como una señal; quemada, queda roja fija. Las zonas se calculan con los tiempos de la configuración.

Tiempos: 3 s hasta que está lista y 2 s lista (1,2 s perfecta y 0,8 s de aviso parpadeando); a los 5 s se quema. Así el verde empieza al 60 % de la barra. Estos tiempos no cambian con la dificultad.

### Armado

La hamburguesa se arma de abajo hacia arriba sobre el plato. La comanda del cliente muestra la receta como una pila de íconos, con el siguiente paso resaltado.

- Tocar el ingrediente que corresponde lo coloca de inmediato, con una caída corta y un sonido.
- **Pocos ingredientes**: queso, tres verduras (lechuga, tomate y cebolla) y tres salsas. Los pepinillos se quitaron para simplificar.
- **Hay una sola casilla de pan**: pone el pan que toque según la comanda (abajo, en medio o arriba). Las recetas conservan sus tres tipos de pan; solo se simplifica el toque.
- Las salsas se aplican desde los botes de arriba, con una animación de apretar.
- Si se toca un ingrediente que no toca, se rechaza (propuesta; ver pendientes): sacudida, zumbido y una pequeña pérdida de paciencia del cliente. Así no hace falta una mecánica para deshacer o tirar hamburguesas.
- Cuando se coloca el último pan, la orden se entrega sola al cliente.

### Clientes

- Hay un cliente en el mostrador. El siguiente puede asomarse en la fila (opcional).
- Cada cliente llega con su comanda y una **barra de paciencia**.
- Si se entrega a tiempo, el cliente se alegra, sube el contador de clientes atendidos y entra el siguiente.
- Si se le acaba la paciencia, se va enojado y el jugador pierde una vida (propuesta: 3 vidas; ver pendientes).
- Las variaciones de cliente (personajes distintos) dan vida sin añadir mecánicas.

### Pausa

- Un botón ❚❚ en la esquina superior derecha, visible mientras se juega (también en el tutorial), detiene el tiempo: cocción, paciencia y llegada de clientes. Mientras está en pausa no se aceptan toques.
- La pantalla de pausa ofrece «Continuar» y «Volver a empezar» (reinicia el modo actual).
- `P` o `Esc` pausan y reanudan mientras la sección está a la vista.
- Si el jugador sale de la sección o cambia de pestaña a media partida, el juego queda en pausa. Al volver decide cuándo seguir, en lugar de reanudarse de golpe.

### Puntuación y récord

Como en el dinosaurio de Chrome, el marcador principal es un solo número: **clientes atendidos**. Se muestra junto al récord, que se guarda en `localStorage` y se protege con `try/catch`. Si el almacenamiento no está disponible, el juego funciona igual, solo que sin récord.

### Dificultad

La dificultad es **el tiempo**: cada cliente da menos tiempo que el anterior para su orden. Siempre debe ser posible lograrlo, pero en cierto punto hay que ser muy hábil. Ese tiempo deja de bajar al llegar a un tope, y desde ahí todo depende de la habilidad.

- **Tiempo mínimo de la orden**: lo que tardaría alguien sin errores. Las carnes se cocinan en tandas según los lugares de la plancha, y cada toque (ingredientes, poner y sacar carne) suma un tiempo fijo.
- **Paciencia** = tiempo mínimo × **holgura**. La holgura baja con cada cliente hasta un mínimo mayor que 1, así que la orden siempre es posible.
- La cocción no se acelera: la carne tarda siempre lo mismo. La presión viene solo del tiempo del cliente.

Valores iniciales propuestos (ajustables en el panel):

| Parámetro | Valor |
| --- | --- |
| Tiempo por toque | 0,4 s |
| Holgura inicial | ×4,5 |
| Clientes con holgura completa | 2 |
| Baja por cliente (después) | 0,2 |
| Holgura mínima (tope) | ×1,5, desde el cliente 17 |

Con estos valores, la clásica da unos 32 s en los primeros clientes, 21 s en el cliente 10 y 11 s en el tope; una torre de cuatro carnes en el tope, unos 16 s. Ajustes tras las partidas de prueba: con ×3 desde el primer cliente el arranque resultaba apretado, y con la baja de 0,1 (tope en el cliente 33) la dificultad tardaba demasiado en subir.

Las recetas y la plancha crecen por tramos:

| Clientes | Recetas | Lugares en plancha |
| --- | --- | --- |
| 1–2 | Sencilla o con queso | 2 |
| 3–5 | Doble carne, más verduras y salsas | 2 |
| 6–9 | Triple carne | 3 |
| 10–14 | Cuádruple o pan intermedio | 4 |
| 15+ | Cualquiera | 4 |

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
4. Las verduras (lechuga, tomate, cebolla) van después de la última carne de su sección, sin repetirse dentro de ella.
5. Las salsas (cátsup, mostaza, mayonesa) van al final de la sección, justo antes del siguiente pan. Puede haber como máximo dos por sección.
6. La altura total no supera el límite del plato: 100 px lógicos como valor inicial (ver tamaños en [ASSETS.md](ASSETS.md)).

Las recetas aleatorias del modo infinito se construyen **a partir de la gramática**, nunca combinando ingredientes al azar, así que siempre son válidas. El validador se usa en las pruebas y para revisar las recetas escritas a mano.

### Catálogo inicial

| Receta | Pila (abajo → arriba) | Uso |
| --- | --- | --- |
| Clásica | pan_base · carne · queso · lechuga · tomate · cátsup · pan_tapa | Tutorial y clientes iniciales |
| Sencilla | pan_base · carne · cátsup · mostaza · pan_tapa | Clientes iniciales |
| Doble | pan_base · carne · queso · carne · queso · cebolla · mostaza · pan_tapa | Nivel 2 |
| Triple | pan_base · carne · queso · carne · carne · queso · lechuga · cátsup · pan_tapa | Nivel 3 |
| Cuádruple («la torre») | pan_base · 4 × (carne · queso) · cebolla · mostaza · pan_tapa | Nivel 4 |
| Tres panes | pan_base · carne · queso · lechuga · pan_medio · carne · queso · tomate · mayonesa · pan_tapa | Nivel 4 |

Además del catálogo, el generador crea variantes por nivel. Los nombres son provisionales hasta definir la marca.

## Tutorial

Es un guion de pasos. Cada paso resalta un elemento con una flecha y un texto breve, y solo acepta el toque correcto. Los demás elementos quedan atenuados. Los tiempos de cocción avanzan hasta «perfecta» y se congelan ahí, y la paciencia del cliente no corre.

1. Llega el cliente: «¡Una clásica, por favor!». La comanda aparece resaltada.
2. Flecha a la charola de carne: «Pon la carne en la plancha».
3. Flecha a la casilla de pan: «Mientras se cocina, pon el pan en el plato».
4. La carne llega a perfecta y se congela. Flecha: «¡Lista! Tócala y pasa al pan».
5. Queso, lechuga, tomate y cátsup, cada uno con su flecha.
6. Otra vez la casilla de pan, que ahora pone el de arriba. Entrega y cliente feliz.
7. Mensaje final con «Pídela de verdad» y «Seguir jugando».

La carne quemada no aparece en el tutorial. En el modo infinito, **la primera vez** que ocurre algo nuevo (primera carne quemada, primera receta con pan intermedio, plancha que crece) aparece una pista contextual breve y el tiempo se pausa un momento. Cada pista se muestra una sola vez por visitante.

## Disposición del escenario

El juego se dibuja en un escenario de resolución lógica fija que se escala por múltiplos enteros, para que el pixel no se deforme.

La disposición es una **barra de preparación** y es la misma en escritorio y en móvil. De abajo hacia arriba:

1. **Plancha**, con las **carnes crudas a su derecha** y la basura del otro lado.
2. **Riel de complementos** (pan, queso, lechuga, tomate, cebolla) justo encima.
3. **Plato centrado**, con los **aderezos a su derecha** y la **comanda a la izquierda**.
4. Del otro lado de la barra, el **cliente**, centrado sobre el plato.

**La zona de preparación es la barra**: plancha, complementos, plato y aderezos están sobre el mismo mostrador. La barra es delgada (empieza a media altura de los aderezos) para dar cercanía con el cliente y dejar **amplia la pared del fondo**, donde irán animaciones de pixel art. El cliente está de pie justo detrás, recargado en el borde y con la parte baja del cuerpo tapada por la barra. Es alto, así que su cara queda por encima de las hamburguesas normales. La comanda cuelga a la izquierda, entre la pared y la barra. Si una hamburguesa muy alta llega a su altura, queda delante de él, como en la vida real. Todo lo que se usa en cada hamburguesa queda alrededor del plato y a pocos pasos de la plancha, así que los movimientos son cortos.

**Horizontal, 320 × 200** (escritorio y tableta)

```text
┌────────────────────────────────────────────┐
│ ♥♥♥                    CLIENTES 12 · RÉCORD │
│                  ▬▬▬▬ paciencia             │
│                  CLIENTE                    │
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ BARRA ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│ ┌COMANDA┐                    (tutorial)     │
│ │       │          ↑ pila                   │
│ │       │          │      [CÁT][MOS][MAY]   │
│ └───────┘       (plato)                     │
│      [pan][queso][lechuga][tomate][cebolla] │
│  [🗑]   [ ][ ][ ][ ] PLANCHA    [carne]      │
└────────────────────────────────────────────┘
```

**Vertical, 180 × 280** (móvil): el mismo orden; la comanda ocupa la columna izquierda y la basura queda a la derecha, junto al cliente.

Las coordenadas de cada pieza se definen en un mapa por disposición. La lógica del juego no conoce posiciones.

## Motor

### Por qué HTML/CSS y no una librería de juegos

El juego tiene posiciones fijas, se controla con toques y no necesita física, colisiones ni muchos objetos en movimiento. Un motor propio pequeño sobre el DOM ofrece:

- Botones reales: el teclado, el foco, el tacto y los lectores de pantalla funcionan sin trabajo extra.
- Animaciones con GSAP, que ya está en la plantilla, y ningún bucle de render adicional.
- Escalado responsive con CSS e integración natural con Astro y Lenis.
- Cero dependencias pesadas en la landing.

Alternativas descartadas por ahora: Phaser o PixiJS (demasiado para este alcance, y obligan a rehacer la accesibilidad dentro de un canvas) y Kaplay o LittleJS (ligeros y buenos para pixel art, pero aquí no aportan nada que el DOM no resuelva). Si el juego llegara a necesitar movimiento libre o colisiones, la lógica se conserva y solo cambia la capa de dibujo.

### Arquitectura

```text
src/components/MiniGame.astro   Sección, estilos y carga diferida del juego
src/game/
  main.ts            Monta juego, vista, reloj y pausas por visibilidad
  engine/
    clock.ts         Reloj sobre gsap.ticker con pausas por motivo
    stage.ts         Disposición y escala entera según el espacio
    audio.ts         (F5) Efectos con ZzFX, silencio y desbloqueo con el primer toque
  game/              Lógica pura, sin DOM; probada con node --test (tests/)
    config.ts        Todos los valores ajustables
    ingredients.ts   Ingredientes, tamaños y grupos
    recipes.ts       Gramática, validador, generador por nivel y catálogo
    grill.ts         Lugares, estados de la carne y congelamiento del tutorial
    difficulty.ts    Tramos, holgura, tiempo mínimo y paciencia
    tutorial.ts      Guion de pasos y señales
    session.ts       Máquina de estados, armado, clientes, vidas, pistas y récord
    storage.ts       localStorage protegido, o memoria en pruebas
  layouts/index.ts   Mapas de piezas horizontal (320 × 200) y vertical (180 × 280)
  view/
    game-view.ts     Vista con sprites desde el atlas (antes, vista con bloques)
    debug.ts         Panel de ajuste (desarrollo o ?ajustes)
  sprites/           palette.ts (Endesga 32 y rampas) · define.ts · validate.ts (errores y estilo) ·
                     atlas.ts · bake.ts · convert.ts (PNG → texto) · index.ts (registro) y las definiciones
src/dev/sprites.astro   Página de revisión (solo con pnpm dev)
```

La vista con bloques se sustituyó en F4 por la vista con sprites, que escucha los mismos eventos. No hay carpeta de imágenes: los sprites viajan dentro del JavaScript del juego.

Principios:

- **La lógica está separada del dibujo.** `game/*` no toca el DOM: emite eventos que la capa visual convierte en animaciones. Así la lógica se puede probar con pruebas unitarias y la mecánica se ajusta sin tocar el arte.
- **Un solo reloj de juego.** Se usa `gsap.ticker`, el mismo que mueve Lenis, con tiempo propio que se pausa. El congelamiento del tutorial y las pausas de las pistas viven en `clock.ts`.
- **Se pausa solo** cuando la sección sale de la vista (IntersectionObserver) o la pestaña se oculta (`visibilitychange`).
- **Pixel nítido.** `image-rendering: pixelated`, escala entera calculada según el ancho disponible, sin transformaciones fraccionarias en los sprites (se redondea a pixeles lógicos).
- **Animación de sprites.** Los estados son variantes de la misma definición (cambio de paleta o `patch`), horneadas por adelantado: cambiar de estado es cambiar la imagen del elemento. El movimiento (caída, rebote, apretar, sacudida) se hace con GSAP. Las animaciones cuadro a cuadro (humo, chispas) son tiras horneadas que se usan con `steps()`.
- **El HUD es HTML.** Marcador, comanda, etiquetas, textos del tutorial y botones usan la fuente **Pixelify Sans** (Google Fonts) a 6 × escala, a «medio pixel» del juego para que se lea bien sin ocupar tanto; los títulos, al doble.

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

El juego se construye primero completo con bloques (`div` y botones de color con su nombre) para fijar mecánica y tiempos. Los sprites se hacen al final.

- [x] **F1 · Flujo completo con bloques**: escenario y escalado, reloj, plancha, armado, recetas (gramática, generador y validador), clientes, vidas, dificultad, modo infinito, récord, tutorial y pistas. Incluye un panel de ajuste para cambiar los tiempos mientras se juega. Tutorial, modo infinito, quema, pistas y disposición vertical revisados en navegador; 37 pruebas de lógica.
- [x] **F2 · Ajuste de tiempos y sensación**: casilla única de pan, sin pepinillos, indicador de cocción, barra de preparación, pausa, basura funcional y curva de dificultad ajustada tras partidas de prueba. Los valores pueden seguir afinándose con el panel.
- [x] **F3 · Sprites como texto**: formato `defineSprite`/`defineTilemap`, paleta, validación, horneado, página de revisión y set ancla (pan base, carne, queso y bote). Ver [ASSETS.md](ASSETS.md). Implementado, con atlas único, revisión de estilo e ida y vuelta con Aseprite. Set ancla aprobado.
- [x] **F4 · Inventario completo de sprites**: 20 sprites (ingredientes, salsas, botes, plato, charola, basura con alerta, clientes hombre y mujer con 3 expresiones y 4 looks cada uno, humo, flecha, corazones, azulejo y madera) que sustituyen a los bloques en el juego. Revisado en escritorio y móvil; 124 pruebas. No hizo falta el importador.
- [ ] **F5 · Sonido**: efectos sincronizados con las animaciones de los sprites (apretar el bote, chisporroteo, destello de «lista»), silencio y desbloqueo de audio. Va después de los sprites porque su duración y carácter dependen de ellas.
- [ ] **F6 · Integración y revisión**: sección 2, respaldo sin JS, disposiciones horizontal y vertical, accesibilidad, rendimiento y compilación.

F2 es la fase crítica: si la plancha no se siente bien con bloques, el arte no la va a salvar.

## Criterios de aceptación

- El tutorial no se puede perder y termina en la oferta con las dos opciones.
- En el modo infinito, la carne pasa sola a la hamburguesa solo cuando el siguiente paso es carne. Una carne quemada bloquea su lugar hasta descartarla.
- Todas las recetas generadas pasan el validador y caben en el plato.
- Cada cliente da menos tiempo hasta llegar al tope. La paciencia siempre supera el tiempo mínimo de la orden.
- La pausa detiene todos los tiempos y se activa sola al salir de la sección o de la pestaña.
- Se juega con mouse, tacto y teclado. Funciona en 320 × 200 escalado en escritorio y en la disposición vertical en móvil.
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
6. ~~**Fuente pixel** del HUD.~~ Resuelto: Pixelify Sans a medio pixel del juego (Bytesized quedaba chica y Tiny5, enorme).
7. **Marca y destino** de «Pídela de verdad» (nombre, URL o app de pedidos).
8. **Ingredientes extra**: tocino, cebolla caramelizada, aguacate u otros que encajen con la marca.
