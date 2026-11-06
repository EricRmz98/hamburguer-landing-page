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
 * Tiempo mínimo para preparar la orden sin errores: carne y tocino se reparten entre los lugares
 * de la plancha con su duración propia; cada toque cuesta tapTime.
 */
export function minimumTime(stack: readonly IngredientId[], slots: number, config: GameConfig): number {
  const durations = stack.filter(id => id === 'carne' || id === 'tocino')
    .map(id => id === 'tocino' ? config.grill.baconCookTime : config.grill.cookTime)
    .sort((a, b) => b - a);
  const lanes = Array(Math.max(1, slots)).fill(0) as number[];
  for (const duration of durations) {
    const lane = lanes.indexOf(Math.min(...lanes));
    lanes[lane] += duration;
  }
  const taps = stack.length + durations.length;
  return Math.max(...lanes) + taps * config.patience.tapTime;
}

/** Paciencia del cliente: siempre mayor que el tiempo mínimo mientras la holgura sea mayor que 1. */
export function patienceFor(stack: readonly IngredientId[], level: Level, config: GameConfig): number {
  return minimumTime(stack, level.slots, config) * level.slack * config.patience.scale;
}
