import type { GrillConfig } from './config.ts';

export type PattyState = 'cruda' | 'cocinandose' | 'perfecta' | 'aviso' | 'quemada';
export type GrillIngredient = 'carne' | 'tocino';

export function pattyState(t: number, c: GrillConfig): PattyState {
  if (t < c.cookTime * c.rawFraction) return 'cruda';
  if (t < c.cookTime) return 'cocinandose';
  if (t < c.cookTime + c.perfectWindow) return 'perfecta';
  if (t < c.cookTime + c.perfectWindow + c.warnTime) return 'aviso';
  return 'quemada';
}

export const isReady = (state: PattyState | null) => state === 'perfecta' || state === 'aviso';

export interface PattyChange {
  slot: number;
  state: PattyState;
}

/** Plancha con lugares fijos. Cada lugar guarda los segundos de cocción de su ingrediente o null si está libre. */
export class Grill {
  cooking: (number | null)[];
  active: number;
  private states: (PattyState | null)[];
  private ingredients: (GrillIngredient | null)[];

  constructor(maxSlots: number, active = maxSlots) {
    this.cooking = Array(maxSlots).fill(null);
    this.states = Array(maxSlots).fill(null);
    this.ingredients = Array(maxSlots).fill(null);
    this.active = active;
  }

  setActive(count: number) {
    this.active = Math.min(count, this.cooking.length);
  }

  clear() {
    this.cooking.fill(null);
    this.states.fill(null);
    this.ingredients.fill(null);
  }

  /** Pone un ingrediente crudo en el primer lugar libre; devuelve el lugar o -1 si la plancha está llena. */
  add(ingredient: GrillIngredient = 'carne'): number {
    for (let i = 0; i < this.active; i++) {
      if (this.cooking[i] === null) {
        this.cooking[i] = 0;
        this.states[i] = 'cruda';
        this.ingredients[i] = ingredient;
        return i;
      }
    }
    return -1;
  }

  remove(slot: number) {
    this.cooking[slot] = null;
    this.states[slot] = null;
    this.ingredients[slot] = null;
  }

  ingredient(slot: number): GrillIngredient | null {
    return this.ingredients[slot] ?? null;
  }

  configFor(slot: number, c: GrillConfig): GrillConfig {
    return this.ingredient(slot) === 'tocino' ? { ...c, cookTime: c.baconCookTime } : c;
  }

  state(slot: number): PattyState | null {
    return this.states[slot] ?? null;
  }

  progress(slot: number, c: GrillConfig): number {
    c = this.configFor(slot, c);
    const t = this.cooking[slot];
    return t === null ? 0 : t / (c.cookTime + c.perfectWindow + c.warnTime);
  }

  /**
   * Avanza la cocción. Con freezeAtPerfect (tutorial) los ingredientes se detienen a mitad
   * de la ventana perfecta y nunca se queman.
   */
  update(dt: number, c: GrillConfig, freezeAtPerfect = false): PattyChange[] {
    const changes: PattyChange[] = [];
    this.cooking.forEach((t, slot) => {
      if (t === null) return;
      const config = this.configFor(slot, c);
      const freezeAt = config.cookTime + config.perfectWindow / 2;
      let next = t + dt;
      if (freezeAtPerfect) next = Math.min(next, Math.max(t, freezeAt));
      this.cooking[slot] = next;
      const state = pattyState(next, config);
      if (state !== this.states[slot]) {
        this.states[slot] = state;
        changes.push({ slot, state });
      }
    });
    return changes;
  }
}
