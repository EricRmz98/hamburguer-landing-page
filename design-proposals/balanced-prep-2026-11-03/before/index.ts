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
  hud: [4, 2, 292, 10],
  pause: [302, 1, 14, 11],
  patience: [140, 12, 40, 3],
  customer: [112, 8, 96, 120], // Cintura nativa (fila 114) apoyada en el borde de la barra.
  counter: [0, 122, 320, 90],
  ticket: [8, 30, 60, 106],
  bubble: [192, 30, 120, 56],
  plate: [141, 124, 38, 22],
  bottles: { catsup: [194, 111, 14, 35], mostaza: [210, 111, 14, 35], mayonesa: [226, 111, 14, 35] },
  bins: { pan: binsH[0], queso: binsH[1], lechuga: binsH[2], tomate: binsH[3], cebolla: binsH[4] },
  grill: [128, 177, 118, 35],
  slots: row(132, 179, 34, 32, 4, 3),
  charola: [252, 177, 44, 25],
  basura: [82, 178, 44, 24], // abertura a la izquierda de la plancha, sin mueble metálico añadido
};

const binsV = row(0, 238, 36, 25, 0, 5);

export const vertical: Layout = {
  name: 'vertical',
  w: 180,
  h: 300,
  hud: [4, 2, 156, 10],
  pause: [164, 1, 14, 11],
  patience: [70, 90, 40, 3],
  customer: [42, 86, 96, 120],
  counter: [0, 200, 180, 100],
  ticket: [4, 24, 46, 146],
  bubble: [112, 24, 64, 90],
  plate: [71, 205, 38, 22],
  bottles: { catsup: [118, 194, 14, 35], mostaza: [134, 194, 14, 35], mayonesa: [150, 194, 14, 35] },
  bins: { pan: binsV[0], queso: binsV[1], lechuga: binsV[2], tomate: binsV[3], cebolla: binsV[4] },
  grill: [46, 264, 90, 35],
  slots: row(47, 266, 28, 32, 2, 3),
  charola: [138, 264, 42, 25], // 1 pixel bajo la bandeja de cebolla
  basura: [0, 267, 44, 24], // residuos a la izquierda, carne cruda a la derecha
};

export const LAYOUTS = { horizontal, vertical };
