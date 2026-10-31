import { defineSprite } from './define.ts';

// Set ancla de ingredientes (vista lateral). Estilo: 16-bit, sombreado plano y contorno selectivo;
// luz desde arriba a la izquierda. Letras: o = contorno, s = sombra, b = base, l = luz, h = brillo.

export const panBase = defineSprite({
  id: 'pan_base',
  size: [32, 8],
  materials: ['pan'],
  colors: { o: 'cafe', s: 'canela', b: 'durazno', l: 'crema' },
  pixels: `
    ..ssssssssssssssssssssoooooooo..
    .sllllllllllllllllllllllllllllo.
    slllllllblllllllllbllllllbllllso
    sllbbbbbbbbbbbbbbbbbbbbbbbbbbbso
    sbbbbbbbbbbbbbbbbbbbbbbbbbbbbsso
    obbbbbbbbbbbbbbbbbbbbbbbbbbsssso
    .osssssssssssssssssssssssssssso.
    ..oooooooooooooooooooooooooooo..
  `,
});

export const carne = defineSprite({
  id: 'carne',
  size: [32, 6],
  materials: ['carne'],
  colors: { o: 'negro', s: 'cafe-oscuro', b: 'cafe', l: 'canela', h: 'piel' },
  pixels: `
    ...ooooo.ooooooooooo.oooooooo...
    .ollhlllbbbbbbllbbbbbbbbbbbbsso.
    ollbbbbbbbbsbbbbbbbbbsbbbbbbssso
    obbbsbbbbbbssbbbbbbbsbbbbbssssso
    ossbbbssssssssssssssssssssssssso
    ..oooooooooooooooooooooooooooo..
  `,
  variants: {
    perfecta: {},
    cruda: { materials: ['carne-cruda'], colors: { o: 'ciruela', s: 'magenta', b: 'rosa', l: 'piel-clara', h: 'blanco' } },
    cocinandose: { materials: ['carne-cocinandose'], colors: { o: 'cafe-oscuro', s: 'cafe', b: 'canela', l: 'piel', h: 'piel-clara' } },
    quemada: {
      materials: ['carne-quemada'],
      colors: { o: 'negro', s: 'negro', b: 'noche', l: 'pizarra', h: 'gris-azul' },
      patch: { 2: 'ollbbbbobbbbbboobbbbbbbbobbbssso' },
    },
  },
});

export const queso = defineSprite({
  id: 'queso',
  size: [34, 5],
  materials: ['queso'],
  colors: { o: 'oxido', s: 'naranja', b: 'ambar', l: 'amarillo' },
  pixels: `
    .oooooooooooooooooooooooooooooooo.
    ollllllbbbbbbbbbbbbbbbbbbbbbbbbbso
    oblbbbbbbbbbbbbbbbbbbbbbbbbbbbbbso
    obbooooooooooobsooooooooooooooosso
    .oo...........oo...............oo.
  `,
});

export const panMedio = defineSprite({
  id: 'pan_medio',
  size: [32, 6],
  materials: ['pan'],
  colors: { o: 'cafe', s: 'canela', b: 'durazno', l: 'crema' },
  pixels: `
    ..oooooooooooooooooooooooooooo..
    .sllllllllllllllllllllllllllllo.
    sllbbbbbbbbbbbbbbbbbbbbbbbbbbbso
    sbbbbbbbbbbbbbbbbbbbbbbbbbbbssso
    osssssssssssssssssssssssssssssso
    .oooooooooooooooooooooooooooooo.
  `,
});

export const panTapa = defineSprite({
  id: 'pan_tapa',
  size: [32, 14],
  materials: ['pan'],
  colors: { o: 'cafe', s: 'canela', b: 'durazno', l: 'crema', e: 'crema' },
  pixels: `
    ..........oooooooooooo..........
    .......olllllbbbbbbbbbsso.......
    .....ollllbbbbbebbbbbbebsso.....
    ...olllbbebbbbbbbbebbbbbbssso...
    ..ollbbbbbbbbbbebbbbbebbbsssso..
    .ollbbbbebbbbbbbbbebbbbbbssssso.
    .olbbbbbbbbebbbbbbbbbbbbsssssso.
    obbbbbbbbbbbbbbbbbbbbbbbbsssssso
    obbbbbbbbbbbbbbbbbbbbbbbssssssso
    obbbbbbbbbbbbbbbbbbbbbbsssssssso
    obbbbbbbbbbbbbbbbbbbbsssssssssso
    obbbbbbbbbbbbbbbbsssssssssssssso
    osssssssssssssssssssssssssssssso
    .oooooooooooooooooooooooooooooo.
  `,
});

export const lechuga = defineSprite({
  id: 'lechuga',
  size: [34, 5],
  materials: ['lechuga'],
  colors: { o: 'verde-noche', s: 'verde-oscuro', b: 'verde', l: 'verde-claro' },
  pixels: `
    .ooo..oooo.ooooo..oooo.ooooo..ooo.
    ollllbbbbbblllbbbbbbbbllbbbbbbbsso
    obblbbbbbbbbbbbbbbbbbbbbbbbbssssso
    obbbbbbbbssbbbbbbsssssssssssssssso
    .oooo.oooooo.oooooo.oooooo.ooooo..
  `,
});

export const tomate = defineSprite({
  id: 'tomate',
  size: [30, 3],
  materials: ['tomate'],
  colors: { o: 'rojo-oscuro', s: 'rojo-oscuro', b: 'rojo', l: 'rosa' },
  pixels: `
    .oooooooooooooooooooooooooooo.
    ollllbbbbbbbbbbbbbbbbbbbbbbsso
    .oooooooooooooooooooooooooooo.
  `,
});

export const cebolla = defineSprite({
  id: 'cebolla',
  size: [30, 3],
  materials: ['cebolla'],
  colors: { o: 'ciruela', s: 'magenta', b: 'piel-clara', l: 'blanco' },
  pixels: `
    .oooooooooooooooooooooooooooo.
    ollbbbbbsbbbbbbsbbbbbbsbbbbsso
    .oooooooooooooooooooooooooooo.
  `,
});

export const salsa = defineSprite({
  id: 'salsa',
  size: [30, 3],
  materials: ['catsup'],
  colors: { o: 'cafe-oscuro', s: 'rojo-oscuro', b: 'rojo', l: 'rosa' },
  pixels: `
    ..oooooooooooooooooooooooooo..
    olllbbbbbbbbbbbbbbbbbbbbbbssso
    .oo...oo......ooo.....oo....oo
  `,
  variants: {
    catsup: {  },
    mostaza: { materials: ['mostaza'], colors: { o: 'oxido', s: 'tostado', b: 'ambar', l: 'amarillo' } },
    mayonesa: { materials: ['mayonesa'], colors: { o: 'canela', s: 'durazno', b: 'crema', l: 'blanco' } },
  },
});
