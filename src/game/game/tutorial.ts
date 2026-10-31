import type { IngredientId, InputId } from './ingredients.ts';

/** Elementos con los que se puede interactuar. */
export type Target =
  | { kind: 'ok' }
  | { kind: 'charola' }
  | { kind: 'basura' }
  | { kind: 'ingredient'; id: InputId }
  | { kind: 'slot'; index?: number };

/** Lo que hace avanzar un paso del tutorial. */
export type Signal =
  | { kind: 'ok' }
  | { kind: 'patty-added' }
  | { kind: 'perfecta' }
  | { kind: 'placed'; id: IngredientId };

export interface TutorialStep {
  text: string;
  target: Target | null;
  until: Signal;
}

const place = (input: InputId, text: string, placed: IngredientId = input as IngredientId): TutorialStep => ({
  text,
  target: { kind: 'ingredient', id: input },
  until: { kind: 'placed', id: placed },
});

// Guion para la hamburguesa clásica (CATALOG.clasica). Los tiempos están congelados.
export const TUTORIAL_STEPS: TutorialStep[] = [
  {
    text: '¡Llegó tu primer cliente! Quiere una clásica. La comanda dice qué lleva, de abajo hacia arriba.',
    target: { kind: 'ok' },
    until: { kind: 'ok' },
  },
  {
    text: 'Primero lo que más tarda: pon una carne en la plancha.',
    target: { kind: 'charola' },
    until: { kind: 'patty-added' },
  },
  place('pan', 'Mientras se cocina, pon el pan en el plato.', 'pan_base'),
  {
    text: 'Mira la barra de la carne: amarillo es que se está cocinando; en verde, está lista.',
    target: null,
    until: { kind: 'perfecta' },
  },
  {
    text: '¡Lista! Tócala y pasa sola al pan.',
    target: { kind: 'slot' },
    until: { kind: 'placed', id: 'carne' },
  },
  place('queso', 'Ahora el queso.'),
  place('lechuga', 'Lechuga…'),
  place('tomate', '…tomate…'),
  place('catsup', 'Un poco de cátsup.'),
  place('pan', 'Cierra con pan y entrégala. Siempre es la misma casilla: pone el pan que toque.', 'pan_tapa'),
];

export function sameTarget(expected: Target, actual: Target): boolean {
  if (expected.kind !== actual.kind) return false;
  if (expected.kind === 'ingredient' && actual.kind === 'ingredient') return expected.id === actual.id;
  if (expected.kind === 'slot' && actual.kind === 'slot') return expected.index === undefined || expected.index === actual.index;
  return true;
}

export function sameSignal(expected: Signal, actual: Signal): boolean {
  if (expected.kind !== actual.kind) return false;
  if (expected.kind === 'placed' && actual.kind === 'placed') return expected.id === actual.id;
  return true;
}
