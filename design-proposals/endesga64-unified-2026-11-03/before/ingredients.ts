import { defineSprite } from './define.ts';

// Ingredientes en vista frontal elevada 3/4 (cámara a 32° de altura, girada 12°).
// Se generaron modelando cada objeto con vóxeles y proyectándolo: cara de arriba = luz, frente e
// izquierda = base, derecha y contacto = sombra, contorno selectivo y textura por material.
// Son texto como cualquier otro sprite: se pueden retocar a mano. Las anclas (base de cada objeto
// dentro del sprite) están en anchors.ts.

export const panBase = defineSprite({
  id: 'pan_base',
  size: [24, 16],
  materials: ['pan'],
  colors: { o: 'oxido', s: 'canela', b: 'piel', l: 'crema' },
  pixels: `
    ........bo.bbbo.........
    ......bbllbbllbbbbo.....
    ..bbbblllllllllllllbo...
    ..bllllllllbbllllllllo..
    .bblllllllllblllllllllo.
    blllbblllllllllllllllllo
    blllllllllllllbbbbbblllo
    blllllbbbblllllllllllllo
    bllllllllbbllllllllllbbo
    sblllllllllllllllllbblbo
    obbllllllllllbblllllllbo
    .obblllllllllllllllbsbo.
    ..obbbblllllllbblbbbso..
    ...obbbbbsbbsbbbbbooo...
    ....oooobsbbsbbboo......
    ........oooooooo........
  `,
});

export const panMedio = defineSprite({
  id: 'pan_medio',
  size: [24, 15],
  materials: ['pan'],
  colors: { o: 'oxido', s: 'canela', b: 'piel', l: 'crema' },
  pixels: `
    .........bbo............
    .....bbbblbbbbbbbbo.....
    ...bbllllllllllllllo....
    ..bllllllllbblllllllbo..
    ..blllllllllllllllllllo.
    bbllbblllllllllllllllllo
    blllllllllllllbbbbbblllo
    bllllbbbbbbllllllllllllo
    sllllllllllllllllllblbbo
    obllllllllllllllllllblbo
    .obsllllllllbbllllllllo.
    ..sbbllllllllllllllslo..
    ..oobbsbbbslllblbbbooo..
    ....oooobslllbllooo.....
    ........oooooooo........
  `,
});

export const panTapa = defineSprite({
  id: 'pan_tapa',
  size: [24, 16],
  materials: ['pan'],
  colors: { o: 'oxido', s: 'canela', b: 'piel', l: 'tostado', e: 'crema', p: 'tostado' },
  pixels: `
    .......bbbbbbbbbo.......
    ....bbbppppllllblbbo....
    ...bllllpplllllbblllo...
    ..blllllllbblllllllleo..
    .bllllllllllllllllllllo.
    bllllllelbbbblllllellllo
    sllllllllbbbbllbblsslllo
    bllsellblllllllbesllssbo
    slllsllbsllllllsebbslsso
    sblllbssllllllllssblsbbo
    sbblbsllbbslsbblllsslsbo
    obbbsllbssllbssbsblbslbo
    .obblbbbllbbsllslblbsbo.
    ..oobbsbbbsslbblbbbboo..
    ....ooobbssbsbbsbooo....
    .......oooooooooo.......
  `,
});

export const carne = defineSprite({
  id: 'carne',
  size: [27, 17],
  materials: ['carne'],
  colors: { k: 'negro', m: 'cafe-oscuro', n: 'cafe', p: 'canela', h: 'piel' },
  pixels: `
    .......nnnnnnnnnk..........
    ......nppppphhpppnnnnk.....
    ....nnpnnnppppmmnnppppnnk..
    ....nppmmpmppppppppppnmmk..
    ...nmpppppppppppmmnmpppnk..
    .nnnnnpmmmmhpppppppnnppnnk.
    .nmmmnppppppppnnmmmmpppppk.
    mnnppppphhmmmmppppnnnppppk.
    mnnmmppppnnpppppppmmpmppppk
    mnnppnnpppmpmmpmpppppppnnpk
    knnnnmmnppnnpppppppppmmpmnk
    .kknnnppppppppmmppppppnmmnk
    ...mnnnnpppppppppppnmmnmmk.
    ...kkknnnnnmnpnnmnnnnnnkk..
    ......knmnnnnnnnmmnknkk....
    .......kkknnnnnnkkk.k......
    ..........kkkkkk...........
  `,
  variants: {
    perfecta: {  },
    cruda: { materials: ['carne-cruda'], colors: { k: 'ciruela', m: 'magenta', n: 'rosa', p: 'piel-clara', h: 'blanco' } },
    cocinandose: { materials: ['carne-cocinandose'], colors: { k: 'cafe-oscuro', m: 'cafe', n: 'canela', p: 'piel', h: 'piel-clara' } },
    quemada: { materials: ['carne-quemada'], colors: { k: 'negro', m: 'negro', n: 'noche', p: 'pizarra', h: 'gris-azul' } },
  },
});

export const queso = defineSprite({
  id: 'queso',
  size: [24, 15],
  materials: ['queso'],
  colors: { q: 'canela', r: 'ambar', t: 'amarillo', u: 'vainilla' },
  pixels: `
    ....tttttq..............
    ....tuuuuuttttttttq.....
    ...tuuuuuuuuuuuuuuuttttq
    ...tuuuuuuuuuuuuuuuuuuuq
    ..tuuuuuuuuuuuuuuuuuuuuq
    ..tuuuuuuuuuuuuuuuuuuuq.
    ..tuuuuuuuuuuuuuuuuuuq..
    .tuuuuuuuuuuuuuuuuuuuq..
    .tuuuuuuuuuuuuuuuuuuuq..
    tuuuuuuuuuuuuuuuuuuuq...
    rtqquuuuuuuuuuuuuuuuq...
    rq..qqqqqqqqquuuuuuq....
    qq...........qqqqqtq....
    ..................rq....
    ..................qq....
  `,
});

export const lechuga = defineSprite({
  id: 'lechuga',
  size: [28, 16],
  materials: ['lechuga'],
  colors: { v: 'verde-noche', w: 'oliva', x: 'lima', y: 'verde-claro', V: 'pistacho' },
  pixels: `
    ................xxxv........
    .......xv......xVyyv........
    .....xxVxxxxxxxVyxxxv.......
    .....xyyxxxyyyyVyxxxxv...xv.
    ....xVyyyyxyyVxxxxxxyxwxxyyv
    ....xyyyyyxxVxxxyyyVVyxyyyyv
    .xxxyyyyyyxVxxxxyyVVyyyyywxv
    .xyyyyyyVVyyyyyyVyyyyyyyxxwv
    vxxxyyxVVyyyyyyVxxyyyyyyyyv.
    .vxxxVxxyyyyyVxxxxxxxxxxxyyv
    ..vvVxxxyyyyVyxxxyyyyyyxxxxv
    ....xyyyyyyVyyyyxxxxxxxyxwxv
    ....vyyyVyyyyyyyVyyxxxyvvvvv
    .....wxxxwxxxyyyyyyxxyv.....
    .....vvvvvvvvvwxyyyxwv......
    ..............vvvvvvv.......
  `,
});

export const tomate = defineSprite({
  id: 'tomate',
  size: [22, 13],
  materials: ['tomate'],
  colors: { A: 'rojo-oscuro', C: 'rojo', D: 'coral', B: 'tostado' },
  pixels: `
    ......CCCCCCCCCA......
    ...CCCDDCCCDDDDDCCA...
    ..CDDDCCBCCCCCCCDDA...
    ..CDDCCCCBCDDCCBCCDCA.
    .CDDCCCDDCCCCDCCCCDDDA
    .CDDCBBDDCCCCDDCCCDDDA
    ADDCCCCDDDDDCDBBBCDDA.
    ADDDDCCCCBBCCCCCCDDDA.
    .ACDDDCCCCBCCCCCDDDCA.
    ..ACCDDDDDDDDDDDDACA..
    ...AACCCCDDDDCDCAAA...
    .....AAAAAAACAAA......
    ............A.........
  `,
});

export const cebolla = defineSprite({
  id: 'cebolla',
  size: [22, 12],
  materials: ['cebolla'],
  colors: { E: 'ciruela', F: 'magenta', G: 'piel-clara', H: 'blanco' },
  pixels: `
    ......GGGGGGGGGGE.....
    ...GGGFFFHHHFFFFHGE...
    ..GHHFHHHHHHHHHHFHHE..
    .GHFFHHHFHHHHFFHHHFHE.
    .GHFHHFHHHHHHHFHHHFHHE
    .GHFHHHFHHHHHHHFHHFHE.
    EHHFHHHFHHHHHHFHHHFHE.
    .EHHFHHHHFFHFHHHFFHHE.
    ..EHHHHHHHHHHHHFFHHE..
    ...EEHHHHHHFHHHHEEE...
    .....EEEEEEEHEEE......
    ............E.........
  `,
});

export const salsa = defineSprite({
  id: 'salsa',
  size: [20, 13],
  materials: ['catsup'],
  colors: { I: 'cafe-oscuro', J: 'rojo-oscuro', K: 'rojo-ladrillo', L: 'alerta' },
  pixels: `
    .....KI.......KI....
    ...KKLLKKKKKKKLLI...
    ...KLLLLLLLLLLLLLI..
    ...KLLLLLLLLLLLLI...
    ..KLLLLLLLLLLLLLLI..
    .KLLLLLLLLLLLLLLLLI.
    KLLLLLLLLLLLLLLLLLLI
    IILLLLLLLLLLLLLLLLLI
    ..JIIILLLLLLLLIIIII.
    ..I...ILLLLLLI......
    ..I....IIILII..JI...
    ..I.......I....II...
    ..........I.........
  `,
  variants: {
    catsup: {  },
    mostaza: { materials: ['mostaza'], colors: { I: 'oxido', J: 'ambar', K: 'amarillo', L: 'vainilla' } },
    mayonesa: { materials: ['mayonesa'], colors: { I: 'arena', J: 'crema', K: 'vainilla', L: 'blanco' } },
  },
});
