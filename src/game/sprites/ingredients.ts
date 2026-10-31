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
