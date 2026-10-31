import { defineSprite } from './define.ts';

// Tiles de fondo de 20 × 20 que se repiten: azulejo para la pared, madera para la barra.

export const azulejo = defineSprite({
  id: 'azulejo',
  size: [20, 20],
  materials: ['pared'],
  colors: { g: 'negro', b: 'noche', l: 'pizarra' },
  pixels: `
    gggggggggggggggggggg
    lllllllllglllllllllg
    bbbbbbbbbgbbbbbbbbbg
    bbbbbbbbbgbbbbbbbbbg
    bbbbbbbbbgbbbbbbbbbg
    gggggggggggggggggggg
    llllglllllllllglllll
    bbbbgbbbbbbbbbgbbbbb
    bbbbgbbbbbbbbbgbbbbb
    bbbbgbbbbbbbbbgbbbbb
    gggggggggggggggggggg
    lllllllllglllllllllg
    bbbbbbbbbgbbbbbbbbbg
    bbbbbbbbbgbbbbbbbbbg
    bbbbbbbbbgbbbbbbbbbg
    gggggggggggggggggggg
    llllglllllllllglllll
    bbbbgbbbbbbbbbgbbbbb
    bbbbgbbbbbbbbbgbbbbb
    bbbbgbbbbbbbbbgbbbbb
  `,
});

export const madera = defineSprite({
  id: 'madera',
  size: [20, 20],
  materials: ['madera'],
  colors: { o: 'cafe-oscuro', s: 'cafe', b: 'canela', l: 'piel' },
  pixels: `
    llllllllllllllllllll
    bbbbbbsssbbbbbbbbbbb
    bbbbbbbbbbbbbbbbbbbb
    bbbbbbbbbbbbssssbbbb
    oooooooooooooooooooo
    llllllllllllllllllll
    bbbbbbbbbbbbbbsssbbb
    bbbbbbbbbbbbbbbbbbbb
    bbbsssssbbbbbbbbbbbb
    oooooooooooooooooooo
    llllllllllllllllllll
    bbbbbbbbbssssbbbbbbb
    bbbbbbbbbbbbbbbbbbbb
    bbbbbbbbbbbbbbbsssbb
    oooooooooooooooooooo
    llllllllllllllllllll
    bbssssbbbbbbbbbbbbbb
    bbbbbbbbbbbbbbbbbbbb
    bbbbbbbbbbssssbbbbbb
    oooooooooooooooooooo
  `,
});
