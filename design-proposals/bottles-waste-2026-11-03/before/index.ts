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

const binsH = row(64, 139, 36, 25, 3, 5); // 1 pixel libre sobre la plancha y 1 bajo los aderezos

export const horizontal: Layout = {
  name: 'horizontal',
  w: 320,
  h: 200,
  hud: [4, 2, 292, 10],
  pause: [302, 1, 14, 11],
  patience: [140, 12, 40, 3],
  customer: [112, 8, 96, 120], // 1.5×: cintura (fila 76) apoyada en el borde de la barra.
  counter: [0, 122, 320, 78],
  ticket: [8, 30, 60, 106],
  bubble: [192, 30, 120, 56],
  plate: [145, 120, 31, 18],
  bottles: { catsup: [194, 103, 14, 35], mostaza: [210, 103, 14, 35], mayonesa: [226, 103, 14, 35] },
  bins: { pan: binsH[0], queso: binsH[1], lechuga: binsH[2], tomate: binsH[3], cebolla: binsH[4] },
  grill: [82, 165, 156, 35],
  slots: row(86, 167, 34, 32, 4, 4),
  charola: [244, 165, 44, 25], // 1 pixel bajo la bandeja de cebolla
  basura: [40, 170, 36, 22], // hueco en la barra, a la izquierda de la plancha
};

const binsV = row(0, 219, 36, 25, 0, 5);

export const vertical: Layout = {
  name: 'vertical',
  w: 180,
  h: 280,
  hud: [4, 2, 156, 10],
  pause: [164, 1, 14, 11],
  patience: [70, 90, 40, 3],
  customer: [42, 86, 96, 120],
  counter: [0, 200, 180, 80],
  ticket: [4, 24, 46, 146],
  bubble: [112, 24, 64, 90],
  plate: [75, 199, 31, 18],
  bottles: { catsup: [118, 182, 14, 35], mostaza: [134, 182, 14, 35], mayonesa: [150, 182, 14, 35] },
  bins: { pan: binsV[0], queso: binsV[1], lechuga: binsV[2], tomate: binsV[3], cebolla: binsV[4] },
  grill: [2, 245, 134, 35],
  slots: row(4, 247, 32, 32, 1, 4),
  charola: [138, 245, 42, 25], // 1 pixel bajo la bandeja de cebolla
  basura: [12, 201, 36, 19], // hueco en la barra, a la izquierda del plato
};

export const LAYOUTS = { horizontal, vertical };
