import type { GameConfig } from './config.ts';
import type { IngredientId } from './ingredients.ts';

export interface Level {
  tier: number;
  slots: number;
  slack: number; // holgura sobre el tiempo mínimo de la orden
}

/** Nivel para el cliente número `customer` (1 = primero del modo infinito). */
export function levelFor(customer: number, config: GameConfig): Level {
  const step = config.levels.find((l) => customer <= l.upTo) ?? config.endless;
  const p = config.patience;
  const slack = Math.max(p.slackMin, p.slackStart - p.slackStep * Math.max(0, customer - p.slackGrace));
  return { tier: step.tier, slots: step.slots, slack };
}

/**
 * Tiempo mínimo para preparar la orden sin errores: las carnes se cocinan en tandas
 * según los lugares de la plancha, y cada toque (ingredientes, poner y sacar carne) cuesta tapTime.
 */
export function minimumTime(stack: readonly IngredientId[], slots: number, config: GameConfig): number {
  const carnes = stack.filter((id) => id === 'carne').length;
  const batches = Math.ceil(carnes / Math.max(1, slots));
  const taps = stack.length + carnes;
  return batches * config.grill.cookTime + taps * config.patience.tapTime;
}

/** Paciencia del cliente: siempre mayor que el tiempo mínimo mientras la holgura sea mayor que 1. */
export function patienceFor(stack: readonly IngredientId[], level: Level, config: GameConfig): number {
  return minimumTime(stack, level.slots, config) * level.slack * config.patience.scale;
}
