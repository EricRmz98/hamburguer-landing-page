// Ingredientes del juego. `height` es el grosor en pantalla (vista 3/4): cuánto sube la pila al
// poner el ingrediente; `width`, el ancho de su sprite. El color (de Endesga 32) es el de la comanda.

export type IngredientKind = 'pan' | 'carne' | 'queso' | 'verdura' | 'salsa';

export interface IngredientInfo {
  label: string;
  short: string;
  kind: IngredientKind;
  width: number;
  height: number;
  color: string;
}

export const INGREDIENTS = {
  pan_base: { label: 'Pan de abajo', short: 'Pan ▁', kind: 'pan', width: 24, height: 3, color: '#e4a672' },
  pan_medio: { label: 'Pan de en medio', short: 'Pan ▬', kind: 'pan', width: 24, height: 3, color: '#b86f50' },
  pan_tapa: { label: 'Pan de arriba', short: 'Pan ▀', kind: 'pan', width: 24, height: 7, color: '#d77643' },
  carne: { label: 'Carne', short: 'Carne', kind: 'carne', width: 27, height: 3, color: '#733e39' },
  queso: { label: 'Queso', short: 'Queso', kind: 'queso', width: 24, height: 1, color: '#feae34' },
  lechuga: { label: 'Lechuga', short: 'Lechuga', kind: 'verdura', width: 28, height: 2, color: '#3e8948' },
  tomate: { label: 'Tomate', short: 'Tomate', kind: 'verdura', width: 22, height: 2, color: '#e43b44' },
  cebolla: { label: 'Cebolla', short: 'Cebolla', kind: 'verdura', width: 22, height: 1, color: '#e8b796' },
  catsup: { label: 'Cátsup', short: 'Cátsup', kind: 'salsa', width: 20, height: 1, color: '#a22633' },
  mostaza: { label: 'Mostaza', short: 'Mostaza', kind: 'salsa', width: 20, height: 1, color: '#fee761' },
  mayonesa: { label: 'Mayonesa', short: 'Mayo', kind: 'salsa', width: 20, height: 1, color: '#ead4aa' },
} as const satisfies Record<string, IngredientInfo>;

export type IngredientId = keyof typeof INGREDIENTS;

export const VERDURAS = ['lechuga', 'tomate', 'cebolla'] as const satisfies readonly IngredientId[];
export const SALSAS = ['catsup', 'mostaza', 'mayonesa'] as const satisfies readonly IngredientId[];
export type SalsaId = (typeof SALSAS)[number];

// Casillas de la parte de abajo. Hay una sola de pan: pone el pan que toque (abajo, en medio o arriba).
// Las salsas van en botes y la carne sale de la plancha.
export const BIN_IDS = ['pan', 'queso', 'lechuga', 'tomate', 'cebolla'] as const;
export type BinId = (typeof BIN_IDS)[number];

/** Lo que el jugador toca para poner un ingrediente: una casilla o un bote. */
export type InputId = BinId | SalsaId;

export function inputLabel(input: InputId): string {
  return input === 'pan' ? 'Pan' : INGREDIENTS[input].label;
}

export function inputColor(input: InputId): string {
  return input === 'pan' ? INGREDIENTS.pan_base.color : INGREDIENTS[input].color;
}

/** Qué toque pone este ingrediente; la carne no tiene casilla (sale de la plancha). */
export function inputFor(id: IngredientId): InputId | null {
  if (id === 'carne') return null;
  return INGREDIENTS[id].kind === 'pan' ? 'pan' : (id as InputId);
}

export function stackHeight(stack: readonly IngredientId[]): number {
  return stack.reduce((sum, id) => sum + INGREDIENTS[id].height, 0);
}
