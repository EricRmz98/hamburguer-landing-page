import { defineSprite } from './define.ts';

// Set ancla de utensilios. El bote tiene dos cuadros (normal y apretado) y una variante por salsa.
// Letras: o/s/b/l = salsa (contorno, sombra, base, luz); k/c/d = tapa; w/g = etiqueta.

export const bote = defineSprite({
  id: 'bote',
  size: [16, 32],
  materials: ['catsup', 'metal', 'etiqueta'],
  colors: {
    o: 'cafe-oscuro', s: 'rojo-oscuro', b: 'rojo', l: 'rosa',
    k: 'noche', c: 'gris-claro', d: 'gris',
    w: 'blanco', g: 'gris-claro',
  },
  frames: [
    `
      .......kk.......
      ......kcdk......
      ......kcdk......
      .....kccddk.....
      ....kcccdddk....
      ....kkkkkkkk....
      ...oooooooooo...
      ..olllbbbbbbso..
      .olllbbbbbbbbso.
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      olwwwwwwwwwwggso
      olwwwwwwwwwwggso
      olwwwwwwwwwwggso
      olwbbbbbbbbwggso
      olwbbbbbbbbwggso
      olwwwwwwwwwwggso
      olwwwwwwwwwwggso
      olwwwwwwwwwwggso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      osbbbbbbbbbbssso
      .osbbbbbbbbbsso.
      ..osssssssssso..
      ...oooooooooo...
    `,
    `
      .......bb.......
      ......kcdk......
      ......kcdk......
      .....kccddk.....
      ....kcccdddk....
      ....kkkkkkkk....
      ...oooooooooo...
      ..olllbbbbbbso..
      .olllbbbbbbbbso.
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      .olbbbbbbbbbsso.
      .olbbbbbbbbbsso.
      .olbbbbbbbbbsso.
      .owwwwwwwwwwgso.
      .owwwwwwwwwwgso.
      .owwwwwwwwwwgso.
      .owbbbbbbbbwgso.
      .owbbbbbbbbwgso.
      .owwwwwwwwwwgso.
      .owwwwwwwwwwgso.
      .owwwwwwwwwwgso.
      .olbbbbbbbbbsso.
      .olbbbbbbbbbsso.
      .olbbbbbbbbbsso.
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      ollbbbbbbbbbbsso
      osbbbbbbbbbbssso
      .osbbbbbbbbbsso.
      ..osssssssssso..
      ...oooooooooo...
    `,
  ],
  variants: {
    catsup: {},
    mostaza: { materials: ['mostaza', 'metal', 'etiqueta'], colors: { o: 'oxido', s: 'tostado', b: 'ambar', l: 'amarillo' } },
    mayonesa: { materials: ['mayonesa', 'metal', 'etiqueta'], colors: { o: 'canela', s: 'durazno', b: 'crema', l: 'blanco' } },
  },
});

export const plato = defineSprite({
  id: 'plato',
  size: [48, 8],
  materials: ['ceramica'],
  colors: { o: 'gris-azul', s: 'gris', l: 'gris-claro', w: 'blanco' },
  mirror: 'x',
  pixels: `
    ......oooooooooooooooooo
    ...ooollllllllllllllllll
    .oolllwwwwwwwwwwwwwwwwww
    ollwwwwwwwwwwwwwwwwwwwww
    ossllwwwwwwwwwwwwwwwwwww
    .ossssllllllllllllllllll
    ...oosssssssssssssssssss
    .......ooooooooooooooooo
  `,
});

export const charola = defineSprite({
  id: 'charola',
  size: [38, 18],
  materials: ['carne-cruda', 'metal'],
  colors: { o: 'ciruela', s: 'magenta', b: 'rosa', l: 'piel-clara', k: 'negro', m: 'pizarra', n: 'gris-azul', q: 'noche' },
  pixels: `
    ......oooooooooooooooooooooooooooo....
    .....olllbbbbbbbbbbbbbbbbbbbbbbssso...
    .....obbbbbbbbbbbbbbbbbbbbbbbbsssso...
    ......oooooooooooooooooooooooooooo....
    ....oooooooooooooooooooooooooooo......
    ...olllbbbbbbbbbbbbbbbbbbbbbbssso.....
    ...obbbbbbbbbbbbbbbbbbbbbbbbsssso.....
    ....oooooooooooooooooooooooooooo......
    .....oooooooooooooooooooooooooooo.....
    ....olllbbbbbbbbbbbbbbbbbbbbbbssso....
    ....obbbbbbbbbbbbbbbbbbbbbbbbsssso....
    .....oooooooooooooooooooooooooooo.....
    knnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnk
    knnmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmqqk
    .kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmqqk
    ..kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmqqk..
    ...kqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk...
    ....kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk....
  `,
});

export const basura = defineSprite({
  id: 'basura',
  size: [26, 25],
  materials: ['metal'],
  colors: { k: 'negro', m: 'pizarra', n: 'gris-azul', q: 'noche', r: 'pizarra', t: 'gris-azul' },
  pixels: `
    ..........kkkkkk..........
    ..........k....k..........
    .kkkkkkkkkkkkkkkkkkkkkkkk.
    ktttttrrrrrrrrrrrrrrrrrrrk
    kkkkkkkkkkkkkkkkkkkkkkkkkk
    ..knnnnnnnnnnnnnnnnnnnnk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ..knnmmmmqmmmmmqmmmmmqqk..
    ...kqqqqqqqqqqqqqqqqqqk...
    ...kkkkkkkkkkkkkkkkkkkk...
  `,
  variants: {
    alerta: { materials: ['metal', 'avisos'], colors: { r: 'alerta', t: 'blanco' } },
  },
});
