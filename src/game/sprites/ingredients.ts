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
  colors: { o: 'oxido', s: 'canela', b: 'piel', l: 'crema', a: 'piel-clara' },
  pixels: `
    ........bo.bbbo.........
    ......bbbbbbbbbbbbo.....
    ..bbbbbbaallllllllbbo...
    ..bbbllllllaaaallaabbo..
    .bbballlllllallllaallbo.
    bbbabbllllllaalllaaaaabo
    bbblllllaallllbbaabbaabo
    bbllllbbaallllaaaaaaaabo
    bbbllaaaabbaaaaaaaaaabbo
    ssbblllaaaaaaaaaaaabbbbo
    osbbbaaaaaaaaaaaaaaabbbo
    .obbbbbaaaaaaaaabbbbbso.
    ..obbbbbbbbbbbbbbbbbbo..
    ...obbbbbbbbbbssbbooo...
    ....oooosbbbbbssoo......
    ........oooooooo........
  `,
});

export const panMedio = defineSprite({
  id: 'pan_medio',
  size: [24, 15],
  materials: ['pan'],
  colors: { o: 'oxido', s: 'canela', b: 'piel', l: 'crema', a: 'piel-clara' },
  pixels: `
    .........bbo............
    .....bbbbbbbbbbbbbo.....
    ...bbbbaaallllalllbo....
    ..bbbllllllaalallaabbo..
    ..bballllllllllllaallbo.
    bbbabblllllllallaaaaaabo
    bbblllllaallllbbaabbaabo
    bblllbbbaablllaaaaaaaabo
    sbbllaaaalaaaaaaaaababbo
    obbbbllaaaaaaaaaaaaabbbo
    .obbbaaaaaaaaaaaaaaabbo.
    ..sbbbbbbaaaaaaabbbbbo..
    ..oobbbbbbbbbbbbbbsooo..
    ....oooossbbbbbbooo.....
    ........oooooooo........
  `,
});

export const panTapa = defineSprite({
  id: 'pan_tapa',
  size: [24, 16],
  materials: ['pan'],
  colors: { o: 'oxido', s: 'canela', b: 'piel', l: 'tostado', e: 'crema', p: 'tostado', a: 'piel-clara' },
  pixels: `
    .......bbbbbbbbbo.......
    ....bbbllaappppbpbbo....
    ...bllllaapppppbbpbbo...
    ..blllllllbbppppppppeo..
    .bllllllppppppppppbbbbo.
    blllpppepbbbbpppppepbbpo
    sppppppppbbbbppbbpssbbbo
    bppbeppbpppppppbesppssbo
    spppbppbbppppppsebbspsso
    sbpbpbbbppppbbpbssspsbso
    ssbpbbppbbbpsssbbbssbsoo
    oosbbbbbbbppbssssspsssso
    .oosbbbbppbbsbpsbsbssso.
    ..ooosssbbbbsssbssssoo..
    ....oooossossosssooo....
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
    ......nphhppnnpppnnnnk.....
    ....nnmpppppppppnnppppnnk..
    ....nppnnmnmmppppppppppmk..
    ...nhmmppnnppnphhmmnnpppk..
    .nnhppppmpmmpppphhppppppnk.
    .nmhmmpphhhhhpppmmmmnnnnnk.
    mpppppppppmmnnppnnnnnnnnnk.
    mmpmmpphhpppppnmnmmnnnnnnnk
    mmnpphhhhnnnnnnnnnnnnnnmmmk
    knnmnmppnnnnnnnnnmmmmnnnnnk
    .kkmnnnnhnnnnnnnnnnnnnmmnnk
    ...mmnnnhhnnhhnnnnnnmmmmnk.
    ...kkkmnmnnnnnnmmmnnmnnkk..
    ......kmmnnnnnnmmmnknkk....
    .......kkknmmmmmkkk.k......
    ..........kkkkkk...........
  `,
  variants: {
    perfecta: {  },
    cruda: { materials: ['carne-cruda'], colors: { k: 'rojo-oscuro', m: 'rosa-viejo', n: 'rosa', p: 'piel-clara', h: 'blanco' } },
    cocinandose: { materials: ['carne-cocinandose'], colors: { k: 'cafe-oscuro', m: 'cafe', n: 'canela', p: 'piel', h: 'piel-clara' } },
    quemada: { materials: ['carne-quemada'], colors: { k: 'negro', m: 'negro', n: 'carbon', p: 'gris-neutro', h: 'gris-claro' } },
  },
});

export const queso = defineSprite({
  id: 'queso',
  size: [24, 15],
  materials: ['queso'],
  colors: { q: 'canela', r: 'ambar', t: 'amarillo', u: 'vainilla', j: 'tostado' },
  pixels: `
    ....tttttq..............
    ....tuuuuuttttttttq.....
    ...tuuutjttttuuuuuuttttq
    ...tuuutttttttttttttttuq
    ..tuuuuttttjjttttttttttq
    ..tuuuttjjttttttttttttq.
    ..tuuuttttttjjtttttttq..
    .tuuutttttttttttttrttq..
    .tuuuttttttttttjjrrrrq..
    tuuuuttttttttjjttrrrq...
    rrqqttttttttttttrrrrq...
    rq..qqqqqqqqqtttrrrq....
    qq...........qqqqqqq....
    ..................rq....
    ..................qq....
  `,
});

export const lechuga = defineSprite({
  id: 'lechuga',
  size: [28, 16],
  materials: ['lechuga'],
  colors: { v: 'verde-noche', w: 'verde-oscuro', x: 'verde-claro', y: 'lima' },
  pixels: `
    ................xxxv........
    .......xv......xxxxv........
    .....xxxxxxxxxxyyxxxv.......
    .....xyyyyxyxyyyyxxxxv...xv.
    ....xyyyyyyyyxyxxxxxxxwxxxxv
    ....xxyxxxyyxxxxxxxxxxxxxwwv
    .xxxxyxxxxxxyyyyyxxxxxwwwwwv
    .xyyyxyyyyyyxxxyxxxxxxxxxxwv
    vxxxxxxxyxxxxxyyxxxxxxxxwwv.
    .vxxxxxxxxxxxxxxxxxxwwwxxxxv
    ..vvxxxxxxxxxxxxxxwxxxxxxxxv
    ....xxxxxxxxxxxxxxxxxxxxwwwv
    ....vxxxxxxxxxxxxxwwwwwvvvvv
    .....wxxxxxxxxxxxxxxxxv.....
    .....vvvvvvvvvwwxxwwwv......
    ..............vvvvvvv.......
  `,
});

export const tomate = defineSprite({
  id: 'tomate',
  size: [22, 13],
  materials: ['tomate'],
  colors: { A: 'rojo-oscuro', C: 'rojo', D: 'coral', B: 'tostado', a: 'rojo-ladrillo', P: 'piel-clara' },
  pixels: `
    ......CCCCCCCCCA......
    ...CCCDDDDDDDDDDCCA...
    ..CCDDDDDDDaBBPaDDA...
    ..CDDaBaDDDDBBaDDCCCA.
    .CDDBBBBDDDDDDCCCCCCaA
    .CDDDDDDDDPPCCCaaCCCaA
    ACDDDDDDCCCCCCPBBPCCA.
    ACCDDCCaBBaCCCCaaCCaA.
    .ACCCCaaPBaCCCCCCCaCA.
    ..ACCCCCCCCCCCCaaACA..
    ...AACCCCaaaaCaCAAA...
    .....AAAAAAACAAA......
    ............A.........
  `,
});

export const cebolla = defineSprite({
  id: 'cebolla',
  size: [22, 12],
  materials: ['cebolla'],
  colors: { E: 'ciruela', F: 'magenta', G: 'gris-claro', H: 'blanco', i: 'rosa-palido', j: 'gris-claro' },
  pixels: `
    ......GGGGGGGGGGE.....
    ...GGGFHFFHHFFFjjGE...
    ..GiHFFHHiiHHHjjjjiE..
    .GiFFjHiFFHFFFEjjEjiE.
    .GjFjjiFjjjjjjEijEjiiE
    .GijjjiFjjjjjjEijjEiE.
    EiijjjiFjjjjjjEijjEjE.
    .EijFFjiiiiiEijjEjiiE.
    ..EiiijFjjjjjjEEjiiE..
    ...EEiiijjijjiiiEEE...
    .....EEEEEEEiEEE......
    ............E.........
  `,
});

export const salsa = defineSprite({
  id: 'salsa',
  size: [20, 13],
  materials: ['catsup'],
  colors: { I: 'cafe-oscuro', J: 'rojo-oscuro', K: 'rojo-ladrillo', L: 'rojo', O: 'coral' },
  pixels: `
    .....KI.......KI....
    ...KKLKKKKKKKKJJI...
    ...KLLLLLLKKKKKJJI..
    ...KLLLOOLKKKKKKI...
    ..KLLLOOOOKKKKKKJI..
    .KKLLLLLLKKKKKKKKJI.
    KKKKKKKLKKKKKKKKJJJI
    IIKKKKKKKKKKKKJJJJJI
    ..JIIIKKKKJKJJIIIII.
    ..I...IKJJJJJI......
    ..I....IIIJII..JI...
    ..I.......I....II...
    ..........I.........
  `,
  variants: {
    catsup: {  },
    mostaza: { materials: ['mostaza'], colors: { I: 'oxido', J: 'ambar', K: 'amarillo', L: 'vainilla', O: 'crema' } },
    mayonesa: { materials: ['mayonesa'], colors: { I: 'plata', J: 'piel-clara', K: 'crema', L: 'blanco', O: 'blanco' } },
  },
});
