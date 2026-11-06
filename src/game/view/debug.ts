import { minimumTime } from '../game/difficulty.ts';
import type { Game } from '../game/session.ts';
import type { GameView } from './game-view.ts';

// Panel para ajustar tiempos mientras se juega. Aparece en desarrollo o con ?ajustes en la URL.

interface Slider {
  label: string;
  min: number;
  max: number;
  step: number;
  unit: string;
  get(): number;
  set(value: number): void;
}

export function mountDebug(game: Game, view: GameView) {
  const c = game.config;
  const panel = document.createElement('details');
  panel.className = 'mg-debug';
  panel.innerHTML = '<summary>Ajustes del minijuego</summary>';

  const sliders: Slider[] = [
    { label: 'Velocidad del tiempo', min: 0.25, max: 3, step: 0.25, unit: '×', get: () => c.timeScale, set: (v) => (c.timeScale = v) },
    { label: 'Cocción de tocino', min: 0.5, max: 8, step: 0.25, unit: 's', get: () => c.grill.baconCookTime, set: (v) => (c.grill.baconCookTime = v) },
    { label: 'Cocción hasta lista', min: 1, max: 12, step: 0.25, unit: 's', get: () => c.grill.cookTime, set: (v) => (c.grill.cookTime = v) },
    { label: 'Ventana lista', min: 0.5, max: 8, step: 0.25, unit: 's', get: () => c.grill.perfectWindow, set: (v) => (c.grill.perfectWindow = v) },
    { label: 'Aviso antes de quemarse', min: 0.25, max: 5, step: 0.25, unit: 's', get: () => c.grill.warnTime, set: (v) => (c.grill.warnTime = v) },
    { label: 'Holgura inicial', min: 1, max: 6, step: 0.1, unit: '×', get: () => c.patience.slackStart, set: (v) => (c.patience.slackStart = v) },
    { label: 'Clientes con holgura completa', min: 0, max: 10, step: 1, unit: '', get: () => c.patience.slackGrace, set: (v) => (c.patience.slackGrace = v) },
    { label: 'Baja de holgura por cliente', min: 0, max: 0.5, step: 0.01, unit: '×', get: () => c.patience.slackStep, set: (v) => (c.patience.slackStep = v) },
    { label: 'Holgura mínima (tope)', min: 1, max: 4, step: 0.05, unit: '×', get: () => c.patience.slackMin, set: (v) => (c.patience.slackMin = v) },
    { label: 'Tiempo por toque', min: 0.1, max: 1.5, step: 0.05, unit: 's', get: () => c.patience.tapTime, set: (v) => (c.patience.tapTime = v) },
    { label: 'Penalización por error', min: 0, max: 10, step: 0.5, unit: 's', get: () => c.wrongPenalty, set: (v) => (c.wrongPenalty = v) },
    { label: 'Pausa entre clientes', min: 0, max: 3, step: 0.1, unit: 's', get: () => c.betweenCustomers, set: (v) => (c.betweenCustomers = v) },
  ];

  for (const slider of sliders) {
    const row = document.createElement('label');
    row.className = 'mg-debug-row';
    const name = document.createElement('span');
    const input = document.createElement('input');
    Object.assign(input, { type: 'range', min: slider.min, max: slider.max, step: slider.step, value: slider.get() });
    const show = () => (name.textContent = `${slider.label}: ${slider.get()}${slider.unit}`);
    input.addEventListener('input', () => {
      slider.set(Number(input.value));
      show();
    });
    show();
    row.append(name, input);
    panel.append(row);
  }

  const actions = document.createElement('div');
  actions.className = 'mg-debug-actions';
  const jump = document.createElement('input');
  Object.assign(jump, { type: 'number', min: 1, value: 8, ariaLabel: 'Número de cliente' });
  const button = (label: string, fn: () => void) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = label;
    b.addEventListener('click', () => {
      fn();
      view.sync();
    });
    actions.append(b);
  };
  actions.append(jump);
  button('Ir al cliente', () => game.debugJumpTo(Math.max(1, Number(jump.value) || 1)));
  button('+1 vida', () => game.lives++);
  button('Reiniciar progreso', () => game.debugResetProgress());
  button('Copiar valores', () => {
    const values = JSON.stringify(
      {
        grill: c.grill,
        patience: c.patience,
        wrongPenalty: c.wrongPenalty,
        betweenCustomers: c.betweenCustomers,
      },
      null,
      2,
    );
    navigator.clipboard?.writeText(values).catch(() => prompt('Copia los valores:', values));
  });
  panel.append(actions);

  const info = document.createElement('pre');
  info.className = 'mg-debug-info';
  panel.append(info);
  setInterval(() => {
    if (!panel.open) return;
    const l = game.level;
    const o = game.order;
    info.textContent = [
      `Modo: ${game.mode}  ·  cliente ${game.customerNumber}`,
      `Nivel ${l.tier}: ${l.slots} lugares, holgura ×${l.slack.toFixed(2)}`,
      o && Number.isFinite(o.patienceMax)
        ? `Paciencia: ${o.patience.toFixed(1)} / ${o.patienceMax.toFixed(1)}s (mínimo ${minimumTime(o.recipe.stack, l.slots, c).toFixed(1)}s)`
        : 'Paciencia: —',
      `Receta: ${o ? `${o.recipe.name} (${o.recipe.stack.length})` : '—'}`,
    ].join('\n');
  }, 250);

  document.body.append(panel);
}
