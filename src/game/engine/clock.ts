import gsap from 'gsap';

// Reloj del juego sobre gsap.ticker, el mismo que mueve Lenis: no añade otro bucle.
// Se pausa por motivos con nombre (fuera de vista, pestaña oculta…) y reanuda cuando no queda ninguno.

export interface Clock {
  pause(reason: string): void;
  resume(reason: string): void;
  readonly paused: boolean;
  destroy(): void;
}

const MAX_STEP = 0.1; // evita saltos de tiempo tras un tirón del navegador

export function createClock(onTick: (dt: number) => void): Clock {
  const reasons = new Set<string>();
  const tick = (_time: number, deltaMs: number) => {
    if (reasons.size === 0) onTick(Math.min(deltaMs / 1000, MAX_STEP));
  };
  gsap.ticker.add(tick);
  return {
    pause: (reason) => void reasons.add(reason),
    resume: (reason) => void reasons.delete(reason),
    get paused() {
      return reasons.size > 0;
    },
    destroy: () => gsap.ticker.remove(tick),
  };
}
