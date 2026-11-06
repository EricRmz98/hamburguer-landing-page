import type { GrillConfig } from '../game/config.ts';

/** Límites fijos de las zonas y avance continuo sobre el tiempo total de cocción. */
export function cookingGauge(elapsed: number, config: GrillConfig) {
  const total = config.cookTime + config.perfectWindow + config.warnTime;
  return {
    cookingEnd: 100 * config.cookTime / total,
    readyEnd: 100 * (config.cookTime + config.perfectWindow) / total,
    progress: 100 * Math.min(1, Math.max(0, elapsed / total)),
  };
}
