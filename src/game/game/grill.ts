import type { GrillConfig } from './config.ts';

export type PattyState = 'cruda' | 'cocinandose' | 'perfecta' | 'aviso' | 'quemada';

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

/** Plancha con lugares fijos. Cada lugar guarda los segundos de cocción de su carne o null si está libre. */
export class Grill {
  cooking: (number | null)[];
  active: number;
  private states: (PattyState | null)[];

  constructor(maxSlots: number, active = maxSlots) {
    this.cooking = Array(maxSlots).fill(null);
    this.states = Array(maxSlots).fill(null);
    this.active = active;
  }

  setActive(count: number) {
    this.active = Math.min(count, this.cooking.length);
  }

  clear() {
    this.cooking.fill(null);
    this.states.fill(null);
  }

  /** Pone una carne cruda en el primer lugar libre; devuelve el lugar o -1 si la plancha está llena. */
  add(): number {
    for (let i = 0; i < this.active; i++) {
      if (this.cooking[i] === null) {
        this.cooking[i] = 0;
        this.states[i] = 'cruda';
        return i;
      }
    }
    return -1;
  }

  remove(slot: number) {
    this.cooking[slot] = null;
    this.states[slot] = null;
  }

  state(slot: number): PattyState | null {
    return this.states[slot] ?? null;
  }

  progress(slot: number, c: GrillConfig): number {
    const t = this.cooking[slot];
    return t === null ? 0 : t / (c.cookTime + c.perfectWindow + c.warnTime);
  }

  /**
   * Avanza la cocción. Con freezeAtPerfect (tutorial) las carnes se detienen a mitad
   * de la ventana perfecta y nunca se queman.
   */
  update(dt: number, c: GrillConfig, freezeAtPerfect = false): PattyChange[] {
    const changes: PattyChange[] = [];
    const freezeAt = c.cookTime + c.perfectWindow / 2;
    this.cooking.forEach((t, slot) => {
      if (t === null) return;
      let next = t + dt;
      if (freezeAtPerfect) next = Math.min(next, Math.max(t, freezeAt));
      this.cooking[slot] = next;
      const state = pattyState(next, c);
      if (state !== this.states[slot]) {
        this.states[slot] = state;
        changes.push({ slot, state });
      }
    });
    return changes;
  }
}
