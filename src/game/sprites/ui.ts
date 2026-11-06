import { defineSprite } from './define.ts';

// Efectos y elementos de interfaz.

export const humo = defineSprite({
  id: 'humo',
  size: [8, 8],
  materials: ['metal'],
  colors: { w: 'gris-claro', g: 'gris' },
  frames: [
    `
      ........
      ........
      ........
      ........
      ........
      ...ww...
      ..wwgg..
      ...gg...
    `,
    `
      ........
      ........
      ........
      ...ww...
      ..wwwg..
      ..wggg..
      ...gg...
      ........
    `,
    `
      ........
      ..ww....
      .wwwg...
      .wwggg..
      ..ggg...
      ........
      ........
      ........
    `,
    `
      ..w.....
      .ww.w...
      .w..gg..
      .....g..
      ........
      ........
      ........
      ........
    `,
  ],
  variants: {
    blanco: {},
    negro: { colors: { w: 'gris-azul', g: 'noche' } },
  },
});

export const flecha = defineSprite({
  id: 'flecha',
  size: [9, 8],
  materials: ['acento'],
  colors: { o: 'oxido', s: 'naranja', b: 'ambar', l: 'amarillo' },
  pixels: `
    ..ooooo..
    ..ollbo..
    ..ollbo..
    olllbbbso
    .olbbbso.
    ..obbso..
    ...oso...
    ....o....
  `,
});

export const corazon = defineSprite({
  id: 'corazon',
  size: [7, 6],
  materials: ['corazon'],
  colors: { o: 'rojo-oscuro', b: 'rojo', l: 'rosa' },
  pixels: `
    .oo.oo.
    olbobbo
    obbbbbo
    .obbbo.
    ..obo..
    ...o...
  `,
  variants: {
    lleno: {  },
    vacio: { materials: ['pared'], colors: { o: 'negro', b: 'noche', l: 'pizarra' } },
  },
});

// Cola triangular pequeña, centrada en el lateral izquierdo.
export const globoCliente = defineSprite({
  id: 'globo_cliente',
  size: [60, 23],
  materials: ['pared', 'pelo-oscuro'],
  colors: { o: 'cafe-oscuro', p: 'crema' },
  pixels: `
    .........oooooooooooooooooooooooooooooooooooooooooooooooo...
    .......ooppppppppppppppppppppppppppppppppppppppppppppppppoo.
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    .....opppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ....oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ...opppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ....oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    .....opppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppo
    .......ooppppppppppppppppppppppppppppppppppppppppppppppppoo.
    .........oooooooooooooooooooooooooooooooooooooooooooooooo...
  `,
});

// Cola triangular pequeña, centrada en el lateral izquierdo.
export const globoClienteVertical = defineSprite({
  id: 'globo_cliente_v',
  size: [62, 23],
  materials: ['pared', 'pelo-oscuro'],
  colors: { o: 'cafe-oscuro', p: 'crema' },
  pixels: `
    .........oooooooooooooooooooooooooooooooooooooooooooooooooo...
    .......ooppppppppppppppppppppppppppppppppppppppppppppppppppoo.
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    .....opppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ....oppppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ...opppppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ....oppppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    .....opppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    ......oppppppppppppppppppppppppppppppppppppppppppppppppppppppo
    .......ooppppppppppppppppppppppppppppppppppppppppppppppppppoo.
    .........oooooooooooooooooooooooooooooooooooooooooooooooooo...
  `,
});

// Alerta gruesa, sin fondo, contorno ni sombra.
export const pacienciaUrgente = defineSprite({
  id: 'paciencia_urgente', size: [2, 5], materials: ['corazon'],
  colors: { r: 'rojo' },
  pixels: `
    rr
    rr
    rr
    ..
    rr
  `,
  variants: {
    amarillo: { materials: ['mostaza'], colors: { r: 'ambar-oscuro' } },
  },
});

// Checkbox de siete celdas con check nativo; sin glifos tipográficos.
export const casillaComanda = defineSprite({
  id: 'casilla_comanda', size: [7, 7],
  materials: ['acento', 'pared'],
  colors: { o: 'oxido', b: 'crema' },
  pixels: `
    ooooooo
    obbbbbo
    obbbbbo
    obbbbbo
    obbbbbo
    obbbbbo
    ooooooo
  `,
  variants: {
    marcada: {
      materials: ['pared', 'ropa-verde'],
      colors: { o: 'verde-oscuro', b: 'verde-oscuro', c: 'crema' },
      pixels: `
        ooooooo
        obbbbco
        obbbcco
        ocbccbo
        occcbbo
        obcbbbo
        ooooooo
      `,
    },
  },
});

// Versión de cinco celdas para las comandas con muchas filas.
export const casillaComandaCompacta = defineSprite({
  ...casillaComanda,
  id: 'casilla_comanda_compacta', size: [5, 5],
  pixels: `
    ooooo
    obbbo
    obbbo
    obbbo
    ooooo
  `,
  variants: {
    marcada: {
      materials: ['pared', 'ropa-verde'],
      colors: { o: 'verde-oscuro', b: 'verde-oscuro', c: 'crema' },
      pixels: `
        ooooo
        obbco
        occco
        obcbo
        ooooo
      `,
    },
  },
});
