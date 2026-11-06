import { defineSprite } from './define.ts';

// Opción D: dos tiras anchas con vetas de grasa y carne distribuidas de forma irregular.
export const tocino = defineSprite({
  id: 'tocino', size: [26, 13],
  materials: ['pan', 'catsup'],
  colors: { o: 'rojo-oscuro', f: 'crema', p: 'piel-clara', m: 'coral', s: 'rojo-ladrillo' },
  pixels: `
    ..........................
    ...ppp...............mm...
    ..fmmmpppp.......pppmfff..
    ..mmmmmmffpppppppmmmmmmm..
    ..ffffmmffffffppppmmmfff..
    ...sssfffmfffffmmmmmmmo...
    ..pppmssssmmmffmmmmfffpp..
    .ffffmmmmfssssffffmmmmfff.
    .mmmmffffssss.ssssffffmmm.
    .ffffssss.........ssssfff.
    ..sss.................oo..
    ..........................
    ..........................
  `,
  variants: {
    cruda: {},
    cocinandose: {
      materials: ['pan', 'catsup'],
      colors: { o: 'oxido', f: 'piel-clara', p: 'tostado', m: 'coral', s: 'rojo-ladrillo' },
    },
    perfecta: {
      materials: ['pan', 'catsup'],
      colors: { o: 'cafe', f: 'tostado', p: 'canela', m: 'rojo-ladrillo', s: 'oxido' },
    },
    quemada: {
      materials: ['carne-quemada'],
      colors: { o: 'negro', f: 'carbon', p: 'gris-claro', m: 'carbon', s: 'negro' },
      pixels: `
        ..........................
        ...ppp...............mm...
        ..pmmmpppp.......fffmfff..
        ..mmmmmmppfffffffmmmmmmm..
        ..ppppmmppffffffffmmmfff..
        ...ssspppmfffffmmmmmmmo...
        ..fffmssssmmmffmmmmfffff..
        .ffffmmmmfssssffffmmmmfff.
        .mmmmffffssss.ssssffffmmm.
        .ffffssss.........ssssfff.
        ..sss.................oo..
        ..........................
        ..........................
      `,
    },
  },
});

// Las tiras de la plancha quedan separadas, casi rectas y con sus dos vetas claras.
export const tocinoPlancha = defineSprite({
  ...tocino,
  id: 'tocino_plancha',
  pixels: `
    ..........................
    ..ppppppppppppppppppmmm...
    .ffffmmmmmfffffffmmmmfff..
    .mmmmmmmmmfffffffmmmmmmm..
    .ffffffffffmmmmfffffffff..
    ..sssssssssssssssssssoo...
    ..........................
    ...pppppppppppppppmmmmpp..
    ..fmmmmmfffffffmmmmffffff.
    ..mmmmmmfffffffmmmmmmmmmm.
    ..fffffffmmmmffffffffffff.
    ...sssssssssssssssssssoo..
    ..........................
  `,
  variants: {
    ...tocino.variants,
    // Ceniza clara en el borde superior y grasa carbonizada gris, sobre un centro negro.
    quemada: {
      materials: ['tocino-quemado'],
      colors: { o: 'negro', f: 'gris-neutro', p: 'gris-claro', m: 'carbon', s: 'negro' },
      pixels: `
        ..........................
        ..ppppppppppppfffffffff...
        .pfffmmmmmfpfffffmmmmfff..
        .mmmmmmmmmfpfffffmmmmmmm..
        .sfffpfffffmmmmffffffffs..
        ..sssssssssssssssssssss...
        ..........................
        ...pppppppppppffffffffff..
        ..pmmmmmfffpfffmmmmffffff.
        ..mmmmmmfffpfffmmmmmmmmmm.
        ..sffpfffmmmmfffffffffffs.
        ...sssssssssssssssssssss..
        ..........................
      `,
    },
  },
});

export const charolaTocino = defineSprite({
  id: 'charola_tocino', size: [42, 25], materials: ['metal', 'pan', 'catsup'],
  colors: { K: 'negro', R: 'gris-azul', S: 'gris', U: 'gris-claro', Z: 'pizarra', k: 'rojo-oscuro', m: 'rojo-ladrillo', n: 'coral', p: 'crema', h: 'piel-clara' },
  pixels: `
    ...UUUUUUUUUUUUUUUUUZZZUZZUUUUUUUUUUUUR...
    .UUUUZhhhhhhhhhhhhhhhhhhhhhhhnnnnZZRUUUUR.
    UUURRpppppnnnnnnpppppppppnnnnnppppZZRRRUUR
    UUUKZnnhhhhhhhhhhhhhhhhhhhhhnnnnnhZZZZKUUR
    UUUZZppppnnnnnnpppppppppnnnnnppppppZZZZUUR
    UUUZZZhhhhhhhhhhhhhhhhhhhnnnnnhhhnnZZZZUUR
    UUUZZpnnnnnnpppppppppnnnnnpppppppppZZZZUUR
    UUUZZnnhhhhhhhhhhhhhhhhhnnnnnhhhhhZZZZZUUR
    UUUZZpnnnnnpppppppppnnnnnpppppppppnZZZZUUR
    UUUZZZnnnnnnppppppppnnnnnnnnnnnnnnnZZZZUUR
    UUUZZZpppppppnnnnppppppppppppppppppZZZZUUR
    UUUZZZZmmmmmmmmmmmmmmmmmmmmmmmmkkkZZZZZUUR
    RUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUR
    .RRUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUURR.
    ..RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRK..
    ..RRRSSSUUUUSSSSSSUUUUSRRRRRRRZZZZZZZZZK..
    ..RRRSSSUUUUSSSSSSSSUUUURRRRRRZZZZZZZZZK..
    ..SRRUUSUUUUSSSSSSSSSSUUUURRRRZZZZZZZZZK..
    ..RRRUUUUUUUSSSSSSSSSSSRUUUURRZZZZZZZZZK..
    ..RRRSSSUUUUSSSSSSSSSSSRRRRRRRZZZZZZZZZK..
    ..RRRSSSSSSSSSSSSSSSSSSRRRRRRRZZZZZZZZZK..
    ..RRRSSSSSSSSSSSSSSSSSSRRRRRRRZZZZZZZZZK..
    ..KRRSSSSSSSSSSSSSSSSSSRRRRRRRZZZZZZZZZK..
    ...RRSSSSSSSSSSSSSSSSSRRRRRRRRZZZZZZZZK...
    ...KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK...
  `,
});
