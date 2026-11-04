// Anclas: posición (x, y) de la base de cada objeto dentro de su sprite, en pixeles.
// La pila del plato coloca cada ingrediente por su ancla; las generó el mismo script que los sprites.

export const ANCHORS: Record<string, readonly [number, number]> = {
  pan_base: [12, 10],
  pan_medio: [12, 9],
  pan_tapa: [12, 10],
  carne: [14, 10],
  queso: [12, 7],
  lechuga: [15, 9],
  tomate: [11, 7],
  cebolla: [11, 6],
  salsa: [10, 6],
  plato: [15, 9],
  bote: [7, 31],
  charola: [2, 14],
  basura: [0, 1],
  plancha: [0, 7],
  plancha_v: [0, 7],
  bandeja_pan: [2, 19],
  bandeja_queso: [2, 17],
  bandeja_lechuga: [2, 15],
  bandeja_tomate: [2, 14],
  bandeja_cebolla: [2, 14],
};
