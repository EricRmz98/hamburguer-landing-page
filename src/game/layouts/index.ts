import type { Layout, Rect } from '../engine/stage.ts';

// Mapas de piezas por disposición. La lógica del juego no conoce posiciones.
// Barra de preparación, igual en ambas disposiciones, de abajo hacia arriba:
//   plancha con las carnes crudas a su derecha → riel de complementos →
//   plato centrado (aderezos a la derecha, comanda a la izquierda).
// La barra es delgada (empieza a media altura de los aderezos) para dejar amplia la pared del fondo.
// El cliente, de pie y recargado en su borde, queda detrás del plato con la cara por encima de las
// hamburguesas normales; una muy alta lo tapa en parte, como en la vida real.

const row = (x: number, y: number, w: number, h: number, gap: number, count: number): Rect[] =>
  Array.from({ length: count }, (_, i) => [x + i * (w + gap), y, w, h] as const);

const binsH = row(67, 140, 34, 20, 4, 5);

export const horizontal: Layout = {
  name: 'horizontal',
  w: 320,
  h: 200,
  hud: [4, 2, 292, 10],
  pause: [302, 1, 14, 11],
  patience: [138, 38, 44, 3],
  customer: [138, 44, 44, 82],
  counter: [0, 122, 320, 78],
  ticket: [8, 30, 60, 106],
  bubble: [192, 30, 120, 56],
  plate: [136, 128, 48, 8],
  bottles: { catsup: [196, 108, 14, 30], mostaza: [214, 108, 14, 30], mayonesa: [232, 108, 14, 30] },
  bins: { pan: binsH[0], queso: binsH[1], lechuga: binsH[2], tomate: binsH[3], cebolla: binsH[4] },
  grill: [82, 163, 156, 36],
  slots: row(86, 165, 34, 32, 4, 4),
  charola: [244, 167, 44, 26],
  basura: [40, 167, 34, 26],
};

const binsV = row(4, 218, 32, 22, 3, 5);

export const vertical: Layout = {
  name: 'vertical',
  w: 180,
  h: 280,
  hud: [4, 2, 156, 10],
  pause: [164, 1, 14, 11],
  patience: [70, 106, 40, 3],
  customer: [70, 112, 40, 92],
  counter: [0, 200, 180, 80],
  ticket: [4, 24, 46, 146],
  bubble: [112, 24, 64, 90],
  plate: [66, 206, 48, 8],
  bottles: { catsup: [118, 186, 14, 30], mostaza: [134, 186, 14, 30], mayonesa: [150, 186, 14, 30] },
  bins: { pan: binsV[0], queso: binsV[1], lechuga: binsV[2], tomate: binsV[3], cebolla: binsV[4] },
  grill: [2, 244, 134, 35],
  slots: row(4, 245, 30, 33, 3, 4),
  charola: [140, 247, 38, 28],
  basura: [146, 130, 28, 30],
};

export const LAYOUTS = { horizontal, vertical };
