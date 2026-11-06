import type { Layout, Rect } from '../engine/stage.ts';

// Mapas de piezas por disposición. La lógica del juego no conoce posiciones.
// Barra de preparación, igual en ambas disposiciones, de abajo hacia arriba:
//   plancha con las carnes crudas a su derecha → riel de complementos →
//   plato centrado (aderezos a la derecha, comanda a la izquierda).
// La encimera deja margen alrededor del plato sin mover la pared ni el cliente.
// El cliente, de pie y recargado en su borde, queda detrás del plato con la cara por encima de las
// hamburguesas normales; una muy alta lo tapa en parte, como en la vida real.

const row = (x: number, y: number, w: number, h: number, gap: number, count: number): Rect[] =>
  Array.from({ length: count }, (_, i) => [x + i * (w + gap), y, w, h] as const);

const binsH = row(64, 151, 36, 25, 3, 5); // margen para el plato ampliado y un píxel sobre la plancha

export const horizontal: Layout = {
  name: 'horizontal',
  w: 320,
  h: 212,
  hud: [81, 5, 158, 14],
  pause: [294, 1, 22, 22],
  customer: [112, 8, 96, 120], // Cintura nativa (fila 114) apoyada en el borde de la barra.
  customerBubble: [202, 28, 54, 23],
  counter: [0, 122, 320, 90],
  ticket: [10, 32, 62, 115],
  bubble: [194, 62, 118, 42],
  plate: [141, 124, 38, 22],
  bottles: { catsup: [194, 104, 16, 42], mostaza: [212, 104, 16, 42], mayonesa: [230, 104, 16, 42] },
  bins: { pan: binsH[0], queso: binsH[1], lechuga: binsH[2], tomate: binsH[3], cebolla: binsH[4] },
  grill: [101, 177, 118, 35], // centro en x=160, compartido con plato y riel de ingredientes
  slots: row(105, 179, 34, 32, 4, 3),
  charola: [223, 177, 42, 25],
  tocino: [55, 177, 42, 25], // misma altura y ancho que la charola; cuatro píxeles a cada lado de la plancha
};

const binsV = row(0, 238, 36, 25, 0, 5);

export const vertical: Layout = {
  name: 'vertical',
  w: 180,
  h: 300,
  hud: [26, 5, 128, 16],
  pause: [158, 2, 22, 22],
  customer: [42, 86, 96, 120],
  customerBubble: [118, 96, 56, 23],
  counter: [0, 200, 180, 100],
  ticket: [5, 44, 55, 145],
  bubble: [64, 28, 110, 62],
  plate: [71, 205, 38, 22],
  bottles: { catsup: [118, 187, 16, 42], mostaza: [136, 187, 16, 42], mayonesa: [154, 187, 16, 42] },
  bins: { pan: binsV[0], queso: binsV[1], lechuga: binsV[2], tomate: binsV[3], cebolla: binsV[4] },
  grill: [45, 264, 90, 35], // centro común en x=90; tres píxeles entre cada pieza
  slots: row(46, 266, 28, 32, 2, 3),
  charola: [138, 264, 42, 25], // 1 pixel bajo la bandeja de cebolla
  tocino: [0, 264, 42, 25], // equilibra la charola derecha y alinea el extremo izquierdo con el pan
};

export const LAYOUTS = { horizontal, vertical };
