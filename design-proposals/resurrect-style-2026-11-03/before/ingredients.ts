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
  colors: { o: 'cafe', s: 'canela', b: 'durazno', l: 'crema' },
  pixels: `
    ........bo.bbbo.........
    ......bbllbllllbbbo.....
    ..bbbbllllllllllbllbo...
    ..bblllllllllllllllllo..
    .bllllllllllllllllllllo.
    blllllllllllllllllbblllo
    bllllllllllllllllllllllo
    bllllllllllllllllllllllo
    bllllbbllllllblllllllllo
    sblbllllllllllllllllllbo
    obbllllllllllllllllllbbo
    .obbllllbllllllllllbsbo.
    ..obbbbblllllllllbbbso..
    ...obbbbbsbbsbbbbbooo...
    ....oooobsbbsbbboo......
    ........oooooooo........
  `,
});

export const panMedio = defineSprite({
  id: 'pan_medio',
  size: [24, 15],
  materials: ['pan'],
  colors: { o: 'cafe', s: 'canela', b: 'durazno', l: 'crema' },
  pixels: `
    .........bbo............
    .....bbbblllbbbbbbo.....
    ...bblbllllllllllllo....
    ..blllblllllllllllllbo..
    ..bllllllllllllllbllllo.
    bbbllllllllllllllllllllo
    blllbllllllllllllllllllo
    blllbllllllllllllllllllo
    sllllllllllllllllllllllo
    ollllllllllllllllllllllo
    .obsllllllllllllllllllo.
    ..slbllllllllllllllslo..
    ..oobbsbbbslllllbbbooo..
    ....oooobslllbllooo.....
    ........oooooooo........
  `,
});

export const panTapa = defineSprite({
  id: 'pan_tapa',
  size: [24, 16],
  materials: ['pan'],
  colors: { o: 'cafe', s: 'canela', b: 'canela', l: 'durazno', e: 'crema' },
  pixels: `
    .......bbbbbbbbbo.......
    ....bbblllellllllbbo....
    ...belllllllllllllllo...
    ..bllllllllllllllllleo..
    .bllllllllllllllllllllo.
    bllllllellllllllllellllo
    slllllllllllllllllsslllo
    bllsellbllllllllesllsslo
    slllsllbsllllllsellslsso
    sblllbssllllllllssblslbo
    sbblbsllbbslsbblllsslsbo
    obbbsllbsslllssbsblbslbo
    .obblbbbllllsllslblbsbo.
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
    ......nppppppmpppnnnnk.....
    ....nnppmmmpmmmpppppppnnk..
    ....nppppppppppmppppppppk..
    ...nppppmppmpppmpppmppppk..
    .nnpmmpppppppppmppmpppmppk.
    .nppppppmmppppmpppppmppppk.
    mhppppppmhpppppppmpppppppk.
    mnphppppppmpmpppppppppmmppk
    mnnpmpphpmpppppppmppmppppmk
    knnnnppppppppppppppppppppnk
    .kknnnhpppppmpmmmppmppnmmnk
    ...mnnnnppmppppmpppnnmnmmk.
    ...kkknnmnnnmpnnmnnnnmnkk..
    ......kmnnnnnnmnmmnknkk....
    .......kkkmnnnmnkkk.k......
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
  colors: { q: 'oxido', r: 'naranja', t: 'ambar', u: 'amarillo' },
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
  colors: { v: 'verde-noche', w: 'verde-oscuro', x: 'verde', y: 'verde-claro' },
  pixels: `
    ................xxxv........
    .......xv......xyyyv........
    .....xxyyxxxxxxyyyyyv.......
    .....xyyyyyyyxyxyyyyyv...xv.
    ....xyyxyyxyyyyyyyyyyywxxyyv
    ....xyyyyxxxxyyyxyyyyxyyxyyv
    .xxxyyxyyyyyyyyyxyxxyyyyywxv
    .xyyyyyyyyyyyyyyyyyxyyyyyywv
    vxyyxxyyyyyyxyyxyxxyyyyyxyv.
    .vyxyyxyyyxyyyyyyyyyyyxyyyyv
    ..vvyyyyyyyxxyyyyyyyyyyxyyyv
    ....xyyyyxyyyyyyyyxxxxyyxwxv
    ....vyyyyxyyyyyyyyxxyyxvvvvv
    .....wxyxwyyxyyyyyxyxyv.....
    .....vvvvvvvvvwxyyyxwv......
    ..............vvvvvvv.......
  `,
});

export const tomate = defineSprite({
  id: 'tomate',
  size: [22, 13],
  materials: ['tomate'],
  colors: { A: 'rojo-oscuro', C: 'rojo', D: 'rosa' },
  pixels: `
    ......CCCCCCCCCA......
    ...CCCDDCCCDDDDDCCA...
    ..CDDDDCCCDDDCCDDDA...
    ..CDDCDCDDDDDDDDDDDCA.
    .CDDCCCDCCCCCDDDDCDDDA
    .CDDDDDDCCCCCCDDDDDDDA
    ADDDCDDDCCCCCCDCCDDDA.
    ADDDDDCDDCCDDCCCCDDDA.
    .ACDDDCCCCDDCCCCDDDCA.
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
  colors: { I: 'cafe-oscuro', J: 'rojo-oscuro', K: 'rojo', L: 'rosa' },
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
    mostaza: { materials: ['mostaza'], colors: { I: 'oxido', J: 'tostado', K: 'ambar', L: 'amarillo' } },
    mayonesa: { materials: ['mayonesa'], colors: { I: 'canela', J: 'durazno', K: 'crema', L: 'blanco' } },
  },
});
