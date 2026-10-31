import type { GameConfig } from './config.ts';
import { levelFor, patienceFor, type Level } from './difficulty.ts';
import { Grill, isReady, type PattyState } from './grill.ts';
import { inputFor, type IngredientId, type InputId } from './ingredients.ts';
import { CATALOG, generateRecipe, type Recipe } from './recipes.ts';
import type { Store } from './storage.ts';
import { TUTORIAL_STEPS, sameSignal, sameTarget, type Signal, type Target, type TutorialStep } from './tutorial.ts';

export type Mode = 'inicio' | 'tutorial' | 'oferta' | 'infinito' | 'fin';
export type HintId = 'infinito' | 'quemada' | 'plancha' | 'tres-panes';
export type RejectReason =
  | 'tutorial'
  | 'no-toca'
  | 'falta-pan'
  | 'todavia'
  | 'plancha-llena'
  | 'sin-orden'
  | 'sin-quemadas';

export type GameEvent =
  | { type: 'mode'; mode: Mode }
  | { type: 'customer-arrived'; number: number; recipe: Recipe }
  | { type: 'placed'; id: IngredientId; index: number; fromSlot?: number }
  | { type: 'rejected'; target: Target; reason: RejectReason }
  | { type: 'patty-added'; slot: number }
  | { type: 'patty-state'; slot: number; state: PattyState }
  | { type: 'patty-discarded'; slot: number }
  | { type: 'served' }
  | { type: 'customer-left'; lives: number }
  | { type: 'game-over'; served: number; record: boolean }
  | { type: 'hint'; hint: HintId | null }
  | { type: 'tutorial-step'; index: number }
  | { type: 'slots'; count: number }
  | { type: 'paused'; paused: boolean };

export interface Order {
  recipe: Recipe;
  patience: number;
  patienceMax: number;
  look: number; // aspecto del cliente; la vista lo reduce a sus opciones con un módulo
}

/**
 * Estado y reglas de una sesión de juego. No toca el DOM: la vista llama a las acciones
 * y escucha los eventos para animar.
 */
export class Game {
  mode: Mode = 'inicio';
  order: Order | null = null;
  stack: IngredientId[] = [];
  grill: Grill;
  level: Level;
  lives: number;
  served = 0;
  customerNumber = 0;
  best: number;
  tutorialStep = 0;
  between = 0; // segundos hasta que llegue el siguiente cliente
  hints: HintId[] = [];
  paused = false;

  readonly config: GameConfig;
  private store: Store;
  private rng: () => number;
  private listeners = new Set<(event: GameEvent) => void>();

  constructor(config: GameConfig, store: Store, rng: () => number = Math.random) {
    this.config = config;
    this.store = store;
    this.rng = rng;
    this.grill = new Grill(config.grill.maxSlots);
    this.level = levelFor(1, config);
    this.lives = config.lives;
    this.best = store.get('record', 0);
  }

  on(listener: (event: GameEvent) => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private emit(event: GameEvent) {
    for (const listener of this.listeners) listener(event);
  }

  get tutorialDone(): boolean {
    return this.store.get('tutorial', false);
  }

  get hint(): HintId | null {
    return this.hints[0] ?? null;
  }

  get step(): TutorialStep | null {
    return this.mode === 'tutorial' ? (TUTORIAL_STEPS[this.tutorialStep] ?? null) : null;
  }

  get nextIngredient(): IngredientId | null {
    return this.order?.recipe.stack[this.stack.length] ?? null;
  }

  get playing(): boolean {
    return this.mode === 'tutorial' || this.mode === 'infinito';
  }

  /** Si el elemento acepta toques ahora mismo (en el tutorial, solo el que señala la flecha). */
  allows(target: Target): boolean {
    if (this.paused) return false;
    if (this.mode === 'tutorial') {
      const expected = this.step?.target;
      if (!expected || !sameTarget(expected, target)) return false;
      return target.kind !== 'slot' || target.index === undefined || isReady(this.grill.state(target.index));
    }
    return this.mode === 'infinito' && !this.hint;
  }

  // ── Flujo ────────────────────────────────────────────────────────────────

  play() {
    if (this.tutorialDone) this.startInfinite();
    else this.startTutorial();
  }

  startTutorial() {
    this.reset();
    this.setMode('tutorial');
    this.tutorialStep = 0;
    this.order = { recipe: CATALOG.clasica, patience: Infinity, patienceMax: Infinity, look: 0 };
    this.emit({ type: 'customer-arrived', number: 0, recipe: CATALOG.clasica });
    this.emit({ type: 'tutorial-step', index: 0 });
  }

  startInfinite() {
    this.reset();
    this.setMode('infinito');
    this.nextCustomer();
    this.showHint('infinito');
  }

  /** Detiene el tiempo de la partida en curso (cocción, paciencia y llegada de clientes). */
  pause() {
    if (!this.playing || this.paused) return;
    this.paused = true;
    this.emit({ type: 'paused', paused: true });
  }

  resume() {
    if (!this.paused) return;
    this.paused = false;
    this.emit({ type: 'paused', paused: false });
  }

  /** Vuelve a empezar el modo actual desde cero. */
  restart() {
    if (this.mode === 'tutorial') this.startTutorial();
    else this.startInfinite();
  }

  dismissHint() {
    if (!this.hints.length) return;
    this.hints.shift();
    this.emit({ type: 'hint', hint: this.hint });
  }

  private reset() {
    this.grill.clear();
    this.stack = [];
    this.order = null;
    this.lives = this.config.lives;
    this.served = 0;
    this.customerNumber = 0;
    this.between = 0;
    this.hints = [];
    this.paused = false;
    this.level = levelFor(1, this.config);
    this.grill.setActive(this.level.slots);
  }

  private setMode(mode: Mode) {
    this.mode = mode;
    this.emit({ type: 'mode', mode });
  }

  private nextCustomer() {
    this.customerNumber++;
    const level = levelFor(this.customerNumber, this.config);
    this.level = level;
    if (level.slots > this.grill.active) {
      this.grill.setActive(level.slots);
      this.emit({ type: 'slots', count: level.slots });
      this.showHint('plancha');
    }
    const recipe = generateRecipe(level.tier, this.config.maxStackHeight, this.rng);
    const patience = patienceFor(recipe.stack, level, this.config);
    this.order = { recipe, patience, patienceMax: patience, look: Math.floor(this.rng() * 1024) };
    this.stack = [];
    this.emit({ type: 'customer-arrived', number: this.customerNumber, recipe });
    if (recipe.stack.includes('pan_medio')) this.showHint('tres-panes');
  }

  private showHint(hint: HintId) {
    const seen = this.store.get<HintId[]>('pistas', []);
    if (seen.includes(hint)) return;
    this.store.set('pistas', [...seen, hint]);
    this.hints.push(hint);
    if (this.hints.length === 1) this.emit({ type: 'hint', hint });
  }

  // ── Acciones del jugador ─────────────────────────────────────────────────

  ok() {
    if (this.allows({ kind: 'ok' })) this.signal({ kind: 'ok' });
  }

  tapCharola() {
    const target: Target = { kind: 'charola' };
    if (!this.allows(target)) return this.reject(target, this.blockedReason());
    const slot = this.grill.add();
    if (slot < 0) return this.reject(target, 'plancha-llena');
    this.emit({ type: 'patty-added', slot });
    this.signal({ kind: 'patty-added' });
  }

  tapIngredient(input: InputId) {
    const target: Target = { kind: 'ingredient', id: input };
    if (!this.allows(target)) return this.reject(target, this.blockedReason());
    if (!this.order || this.between > 0) return this.reject(target, 'sin-orden');
    const next = this.nextIngredient;
    if (!next || inputFor(next) !== input) {
      this.penalize();
      return this.reject(target, 'no-toca');
    }
    this.place(next);
  }

  tapSlot(index: number) {
    const target: Target = { kind: 'slot', index };
    const state = this.grill.state(index);
    if (state === null) return;
    if (!this.allows(target)) return this.reject(target, this.blockedReason());
    if (state === 'quemada') {
      this.grill.remove(index);
      this.emit({ type: 'patty-discarded', slot: index });
      return;
    }
    if (!isReady(state)) return this.reject(target, 'todavia');
    if (!this.order || this.between > 0) return this.reject(target, 'sin-orden');
    if (this.nextIngredient !== 'carne') return this.reject(target, this.stack.length ? 'no-toca' : 'falta-pan');
    this.grill.remove(index);
    this.place('carne', index);
  }

  /** Tira de una vez todas las carnes quemadas de la plancha. */
  tapBasura() {
    const target: Target = { kind: 'basura' };
    if (!this.allows(target)) return this.reject(target, this.blockedReason());
    const burnt = this.grill.cooking.map((_, i) => i).filter((i) => this.grill.state(i) === 'quemada');
    if (!burnt.length) return this.reject(target, 'sin-quemadas');
    for (const slot of burnt) {
      this.grill.remove(slot);
      this.emit({ type: 'patty-discarded', slot });
    }
  }

  private blockedReason(): RejectReason {
    return this.mode === 'tutorial' ? 'tutorial' : 'sin-orden';
  }

  private reject(target: Target, reason: RejectReason) {
    this.emit({ type: 'rejected', target, reason });
  }

  private penalize() {
    if (this.mode === 'infinito' && this.order) this.order.patience -= this.config.wrongPenalty;
  }

  private place(id: IngredientId, fromSlot?: number) {
    this.stack.push(id);
    this.emit({ type: 'placed', id, index: this.stack.length - 1, fromSlot });
    this.signal({ kind: 'placed', id });
    if (this.order && this.stack.length === this.order.recipe.stack.length) this.serve();
  }

  private serve() {
    this.emit({ type: 'served' });
    this.order = null;
    if (this.mode === 'tutorial') {
      this.store.set('tutorial', true);
      this.grill.clear();
      this.setMode('oferta');
      return;
    }
    this.served++;
    this.between = this.config.betweenCustomers;
  }

  private signal(signal: Signal) {
    const step = this.step;
    if (!step || !sameSignal(step.until, signal)) return;
    this.tutorialStep++;
    this.emit({ type: 'tutorial-step', index: this.tutorialStep });
    // Si la carne ya estaba lista al llegar al paso de espera, no hay que esperar.
    const next = this.step;
    if (next?.until.kind === 'perfecta' && this.grill.cooking.some((_, i) => isReady(this.grill.state(i)))) {
      this.signal({ kind: 'perfecta' });
    }
  }

  // ── Tiempo ───────────────────────────────────────────────────────────────

  update(dt: number) {
    if (!this.playing || this.paused || this.hint) return;
    const tutorial = this.mode === 'tutorial';

    const changes = this.grill.update(dt, this.config.grill, tutorial);
    for (const { slot, state } of changes) {
      this.emit({ type: 'patty-state', slot, state });
      if (state === 'perfecta') this.signal({ kind: 'perfecta' });
      if (state === 'quemada') this.showHint('quemada');
    }
    if (tutorial || this.hint) return;

    if (this.between > 0) {
      this.between -= dt;
      if (this.between <= 0) {
        this.between = 0;
        this.nextCustomer();
      }
      return;
    }
    if (this.order) {
      this.order.patience -= dt;
      if (this.order.patience <= 0) this.customerLeaves();
    }
  }

  private customerLeaves() {
    this.lives--;
    this.order = null;
    this.stack = [];
    this.emit({ type: 'customer-left', lives: this.lives });
    if (this.lives <= 0) return this.gameOver();
    this.between = this.config.betweenCustomers;
  }

  private gameOver() {
    const record = this.served > this.best;
    if (record) {
      this.best = this.served;
      this.store.set('record', this.best);
    }
    this.setMode('fin');
    this.emit({ type: 'game-over', served: this.served, record });
  }

  // ── Herramientas del panel de ajuste ─────────────────────────────────────

  debugJumpTo(customer: number) {
    if (this.mode !== 'infinito') {
      this.reset();
      this.setMode('infinito');
    }
    this.hints = [];
    this.stack = [];
    this.between = 0;
    this.customerNumber = Math.max(0, customer - 1);
    this.nextCustomer();
  }

  debugResetProgress() {
    this.store.set('tutorial', false);
    this.store.set('pistas', []);
    this.store.set('record', 0);
    this.best = 0;
    this.grill.clear();
    this.order = null;
    this.stack = [];
    this.hints = [];
    this.paused = false;
    this.setMode('inicio');
  }
}
