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
