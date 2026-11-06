import gsap from 'gsap';
import { fitStage, type Layout, type Rect } from '../engine/stage.ts';
import type { PattyState } from '../game/grill.ts';
import { BIN_IDS, INGREDIENTS, SALSAS, inputLabel, type BinId, type IngredientId, type SalsaId } from '../game/ingredients.ts';
import type { Game, GameEvent, HintId, RejectReason } from '../game/session.ts';
import type { Target } from '../game/tutorial.ts';
import { LAYOUTS } from '../layouts/index.ts';
import { atlasKey } from '../sprites/atlas.ts';
import { atlasStyle, bakeAtlas, type BakedAtlas } from '../sprites/bake.ts';
import { ANCHORS } from '../sprites/anchors.ts';
import { SPRITES } from '../sprites/index.ts';
import { CUSTOMERS } from '../sprites/people.ts';
import { cookingGauge } from './cooking-gauge.ts';

// Vista del juego: cada pieza es un elemento HTML cuyo fondo es su sprite dentro del atlas.
// Escucha los eventos del juego para animar; la lógica no conoce el DOM.

const PATTY_LABEL: Record<PattyState, string> = {
  cruda: 'cruda',
  cocinandose: 'cocinándose',
  perfecta: 'lista',
  aviso: 'por quemarse',
  quemada: 'quemada',
};

const BACON_LABEL: Record<PattyState, string> = {
  cruda: 'crudo', cocinandose: 'cocinándose', perfecta: 'listo', aviso: 'por quemarse', quemada: 'quemado',
};

const STACK_SPRITE: Record<IngredientId, string> = {
  pan_base: 'pan_base',
  pan_medio: 'pan_medio',
  pan_tapa: 'pan_tapa',
  carne: 'carne:perfecta',
  tocino: 'tocino:perfecta',
  queso: 'queso',
  lechuga: 'lechuga',
  tomate: 'tomate',
  cebolla: 'cebolla',
  catsup: 'salsa:catsup',
  mostaza: 'salsa:mostaza',
  mayonesa: 'salsa:mayonesa',
};

// Cada casilla es una bandeja de metal de restaurante con su ingrediente adentro.
const BIN_SPRITE: Record<BinId, string> = {
  pan: 'bandeja_pan',
  queso: 'bandeja_queso',
  lechuga: 'bandeja_lechuga',
  tomate: 'bandeja_tomate',
  cebolla: 'bandeja_cebolla',
};

const FACE = { esperando: 0, feliz: 1, enojado: 2 } as const;
const SMOKE_FRAME_MS = 140;

const REJECT_TEXT: Partial<Record<RejectReason, string>> = {
  'no-toca': 'Ese no va ahora',
  'falta-pan': 'Primero el pan de abajo',
  todavia: 'Todavía no está lista',
  'plancha-llena': 'La plancha está llena',
  'sin-orden': 'Espera al siguiente cliente',
};

const HINT_TEXT: Record<HintId, (game: Game) => string> = {
  infinito: (g) =>
    `La carne tarda ${g.config.grill.cookTime} s y el tocino ${g.config.grill.baconCookTime} s; comparten la plancha. Toca lo quemado para retirarlo. Los clientes se impacientan y tienes ${g.lives} vidas. ¿Cuántos clientes aguantas?`,
  quemada: () =>
    'Se quemó un ingrediente. La zona roja y el humo avisan que debes retirarlo. Toca el ingrediente quemado para retirarlo y liberar su lugar.',
  plancha: (g) => `¡La plancha creció! Ahora tienes ${g.grill.active} lugares.`,
  'tres-panes': () => 'Esta orden lleva pan en medio. Sigue la comanda de arriba hacia abajo.',
};

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className: string, parent?: HTMLElement, text?: string) {
  const node = document.createElement(tag);
  node.className = className;
  if (text !== undefined) node.textContent = text;
  parent?.append(node);
  return node;
}

function setText(node: HTMLElement, text: string) {
  if (node.textContent !== text) node.textContent = text;
}

interface SlotView {
  button: HTMLButtonElement;
  patty: HTMLDivElement;
  smoke: HTMLDivElement;
  gauge: HTMLDivElement;
  track: HTMLDivElement;
  fill: HTMLDivElement;
  signal: HTMLSpanElement;
}

/** Sprite dentro de un contenedor: se centra (o se apoya abajo) en pixeles lógicos enteros. */
interface SpriteSlot {
  key: string;
  frame: number;
  parent?: Rect; // tamaño del contenedor; si falta, el nodo ya está posicionado
  align?: 'center' | 'bottom';
}

export class GameView {
  readonly stage: HTMLDivElement;

  private root: HTMLElement;
  private game: Game;
  private atlas: BakedAtlas;
  private layout: Layout = LAYOUTS.horizontal;
  private scale = 0;
  private reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  private sprites = new Map<HTMLElement, SpriteSlot>();

  private wall: HTMLDivElement;
  private hud: HTMLDivElement;
  private lives: HTMLSpanElement;
  private score: HTMLSpanElement;
  private best: HTMLSpanElement;
  private pauseButton: HTMLButtonElement;
  private ticket: HTMLDivElement;
  private ticketName: HTMLDivElement;
  private ticketRows: HTMLOListElement;
  private customer: HTMLDivElement;
  private patience: HTMLDivElement;
  private patienceSkin: HTMLDivElement;
  private patienceTime: HTMLSpanElement;
  private patienceAttention: HTMLSpanElement;
  private patienceTrack: HTMLDivElement;
  private patienceFill: HTMLDivElement;
  private counter: HTMLDivElement;
  private plate: HTMLDivElement;
  private stackLayer: HTMLDivElement;
  private grill: HTMLDivElement;
  private slots: SlotView[] = [];
  private bottles = new Map<SalsaId, { button: HTMLButtonElement; sprite: HTMLDivElement }>();
  private bins = new Map<BinId, { button: HTMLButtonElement; sprite: HTMLDivElement; tape: HTMLSpanElement }>();
  private charola: HTMLButtonElement;
  private charolaSprite: HTMLDivElement;
  private charolaTape: HTMLSpanElement;
  private tocino: HTMLButtonElement;
  private tocinoSprite: HTMLDivElement;
  private tocinoTape: HTMLSpanElement;
  private bubble: HTMLDivElement;
  private bubbleText: HTMLParagraphElement;
  private okButton: HTMLButtonElement;
  private arrow: HTMLDivElement;
  private toast: HTMLDivElement;
  private overlay: HTMLDivElement;
  private live: HTMLDivElement;

  private ticketKey: string | null = null;
  private stackKey: string | null = null;
  private livesKey = '';
  private overlayKey = '';
  private lastRecord = false;
  private toastTimer = 0;
  /** Cliente que se va: se sigue viendo un momento, feliz o enojado. */
  private leaving: { key: string; face: number; until: number } | null = null;

  constructor(root: HTMLElement, game: Game) {
    this.root = root;
    this.game = game;
    this.atlas = bakeAtlas(Object.values(SPRITES));
    root.replaceChildren();
    const stage = (this.stage = el('div', 'mg-stage', root));

    this.wall = el('div', 'mg-wall mg-sprite', stage);
    this.wall.setAttribute('aria-hidden', 'true');

    this.hud = el('div', 'mg-hud', stage);
    this.hud.setAttribute('role', 'group');
    this.hud.setAttribute('aria-label', 'Marcador de la partida');
    this.lives = el('span', 'mg-lives', this.hud);
    this.lives.setAttribute('role', 'img');
    this.score = el('span', 'mg-score', this.hud);
    this.best = el('span', 'mg-best', this.hud);
    this.pauseButton = el('button', 'mg-pause', stage);
    el('span', 'mg-pause-icon', this.pauseButton).setAttribute('aria-hidden', 'true');
    this.pauseButton.type = 'button';
    this.pauseButton.setAttribute('aria-label', 'Pausar (P)');
    this.pauseButton.addEventListener('click', () => this.act(() => game.pause()));

    // Orden de pintado: el cliente queda detrás de la barra, y todo lo de cocina encima de ella.
    this.customer = el('div', 'mg-customer mg-sprite', stage);
    this.counter = el('div', 'mg-counter mg-sprite', stage);
    this.counter.setAttribute('aria-hidden', 'true');

    this.ticket = el('div', 'mg-ticket', stage);
    this.ticketName = el('div', 'mg-ticket-name', this.ticket);
    this.ticketRows = el('ol', 'mg-ticket-rows', this.ticket);
    this.ticket.setAttribute('aria-label', 'Comanda');

    this.patience = el('div', 'mg-patience', stage);
    this.patience.setAttribute('role', 'group');
    this.patienceSkin = el('div', 'mg-patience-skin mg-sprite', this.patience);
    this.patienceSkin.setAttribute('aria-hidden', 'true');
    const patienceHead = el('div', 'mg-patience-head', this.patience);
    this.patienceTime = el('span', 'mg-patience-time', patienceHead);
    this.patienceAttention = el('span', 'mg-patience-attention mg-sprite', patienceHead);
    this.patienceAttention.setAttribute('aria-hidden', 'true');
    this.patienceTrack = el('div', 'mg-patience-track', this.patience);
    this.patienceTrack.setAttribute('role', 'progressbar');
    this.patienceTrack.setAttribute('aria-label', 'Paciencia del cliente');
    this.patienceTrack.setAttribute('aria-valuemin', '0');
    this.patienceTrack.setAttribute('aria-valuemax', '100');
    this.patienceFill = el('div', 'mg-patience-fill', this.patienceTrack);

    this.plate = el('div', 'mg-plate mg-sprite', stage);
    this.stackLayer = el('div', 'mg-stack', stage);

    for (const id of SALSAS) {
      const button = this.button('mg-bottle', `Bote de ${INGREDIENTS[id].label}`, () => game.tapIngredient(id));
      this.bottles.set(id, { button, sprite: el('div', 'mg-sprite', button) });
    }

    this.grill = el('div', 'mg-grill mg-sprite', stage);
    for (let i = 0; i < game.config.grill.maxSlots; i++) {
      const button = this.button('mg-slot', '', () => game.tapSlot(i));
      const gauge = el('div', 'mg-gauge', button);
      gauge.setAttribute('aria-hidden', 'true');
      const track = el('div', 'mg-cooking-track', gauge);
      const fill = el('div', 'mg-cooking-fill', track);
      const signal = el('span', 'mg-gauge-signal mg-sprite', gauge);
      this.slots.push({
        button,
        patty: el('div', 'mg-patty mg-sprite', button),
        smoke: el('div', 'mg-smoke mg-sprite', button),
        gauge,
        track,
        fill,
        signal,
      });
    }

    this.charola = this.button('mg-charola', 'Poner carne en la plancha', () => game.tapCharola());
    this.charolaSprite = el('div', 'mg-sprite', this.charola);
    this.charolaTape = el('span', 'mg-tape', this.charola, 'Carne');
    this.charolaTape.setAttribute('aria-hidden', 'true');
    this.tocino = this.button('mg-tocino', 'Poner tocino en la plancha', () => game.tapCharola('tocino'));
    this.tocinoSprite = el('div', 'mg-sprite', this.tocino);
    this.tocinoTape = el('span', 'mg-tape', this.tocino, 'Tocino');
    this.tocinoTape.setAttribute('aria-hidden', 'true');

    // Cada casilla: bandeja de metal con su ingrediente y una etiqueta de cinta masking al frente.
    for (const id of BIN_IDS) {
      const button = this.button('mg-bin', inputLabel(id), () => game.tapIngredient(id));
      const sprite = el('div', 'mg-sprite', button);
      const tape = el('span', 'mg-tape', button, inputLabel(id));
      tape.setAttribute('aria-hidden', 'true');
      this.bins.set(id, { button, sprite, tape });
    }

    this.bubble = el('div', 'mg-bubble', stage);
    this.bubbleText = el('p', 'mg-bubble-text', this.bubble);
    this.okButton = el('button', 'mg-ok', this.bubble, 'Empezar');
    this.okButton.type = 'button';
    this.okButton.addEventListener('click', () => this.act(() => game.ok()));

    this.arrow = el('div', 'mg-arrow mg-sprite', stage);
    this.arrow.setAttribute('aria-hidden', 'true');
    this.toast = el('div', 'mg-toast', stage);
    this.overlay = el('div', 'mg-overlay', stage);
    this.live = el('div', 'mg-live', root);
    this.live.setAttribute('aria-live', 'polite');

    if (!this.reduced) gsap.to(this.arrow, { y: -3, duration: 0.45, repeat: -1, yoyo: true, ease: 'sine.inOut' });

    game.on((event) => this.onEvent(event));
    new ResizeObserver(() => this.fit()).observe(root);
    addEventListener('resize', () => this.fit());
    this.fit();
  }

  private button(className: string, label: string, action: () => void) {
    const button = el('button', `mg-btn ${className}`, this.stage);
    button.type = 'button';
    if (label) button.setAttribute('aria-label', label);
    button.addEventListener('click', () => this.act(action));
    return button;
  }

  private act(action: () => void) {
    action();
    this.sync();
  }

  // ── Sprites ──────────────────────────────────────────────────────────────

  /** Asigna un sprite del atlas a un nodo; solo toca el DOM si cambió. */
  private setSprite(node: HTMLElement, key: string, frame = 0, parent?: Rect, align: SpriteSlot['align'] = 'center') {
    const current = this.sprites.get(node);
    if (current && current.key === key && current.frame === frame && current.parent === parent) return;
    this.sprites.set(node, { key, frame, parent, align });
    this.applySprite(node);
  }

  private applySprite(node: HTMLElement) {
    const slot = this.sprites.get(node);
    if (!slot) return;
    const s = this.scale;
    // Clientes y cocina comparten celdas nativas: una única escala entera para todo el atlas.
    Object.assign(node.style, atlasStyle(this.atlas, slot.key, s, slot.frame));
    if (slot.parent) {
      const entry = this.atlas.entries[slot.key];
      const [, , pw, ph] = slot.parent;
      const left = Math.floor((pw - entry.width) / 2);
      const top = slot.align === 'bottom' ? ph - entry.height : Math.floor((ph - entry.height) / 2);
      Object.assign(node.style, { left: `${left * s}px`, top: `${top * s}px` });
    }
  }

  // ── Escalado y posiciones ────────────────────────────────────────────────

  private fit() {
    const { layout, scale } = fitStage(this.root.clientWidth, innerHeight * 0.9, LAYOUTS);
    if (layout === this.layout && scale === this.scale) return;
    this.layout = layout;
    this.scale = scale;
    this.stage.style.width = `${layout.w * scale}px`;
    this.stage.style.height = `${layout.h * scale}px`;
    this.stage.style.setProperty('--s', String(scale));
    this.stage.dataset.layout = layout.name;

    this.place(this.hud, layout.hud);
    this.place(this.pauseButton, layout.pause);
    this.place(this.ticket, layout.ticket);
    this.place(this.customer, layout.customer);
    this.place(this.patience, layout.customerBubble);
    this.setSprite(this.patienceSkin, layout.name === 'vertical' ? 'globo_cliente_v' : 'globo_cliente');
    this.place(this.counter, layout.counter);
    this.place(this.plate, layout.plate);
    this.place(this.bubble, layout.bubble);
    this.bubble.style.height = ''; // el globo se ajusta a su texto; el alto del layout es el máximo
    this.bubble.style.maxHeight = `${layout.bubble[3] * this.scale}px`;
    this.place(this.grill, layout.grill);
    this.place(this.charola, layout.charola);
    this.place(this.tocino, layout.tocino);
    this.slots.forEach((slot, i) => this.place(slot.button, layout.slots[i]));
    for (const [id, { button }] of this.bottles) this.place(button, layout.bottles[id]);
    for (const [id, { button }] of this.bins) this.place(button, layout.bins[id]);
    this.setSprite(this.wall, layout.name === 'vertical' ? 'comedor_v' : 'comedor');
    this.setSprite(this.counter, layout.name === 'vertical' ? 'barra_roja_v' : 'barra_roja');
    this.place(this.wall, [0, 0, layout.w, layout.counter[1]]);

    // Sprites que dependen del tamaño de su contenedor.
    this.setSprite(this.plate, 'plato');
    this.setSprite(this.charolaSprite, 'charola', 0, layout.charola, 'bottom');
    this.placeTape(this.charolaTape, 'charola', layout.charola, BIN_IDS.length);
    this.setSprite(this.tocinoSprite, 'charola_tocino', 0, layout.tocino, 'bottom');
    this.placeTape(this.tocinoTape, 'charola_tocino', layout.tocino, BIN_IDS.length + 1);
    this.setSprite(this.grill, layout.name === 'vertical' ? 'plancha_v' : 'plancha');
    this.slots.forEach(slot => this.setSprite(slot.signal, 'paciencia_urgente'));
    BIN_IDS.forEach((id, i) => {
      const { sprite, tape } = this.bins.get(id)!;
      this.setSprite(sprite, BIN_SPRITE[id], 0, layout.bins[id], 'bottom');
      this.placeTape(tape, BIN_SPRITE[id], layout.bins[id], i);
    });
    for (const [id, { sprite }] of this.bottles) this.setSprite(sprite, atlasKey('bote', id), 0, layout.bottles[id]);
    for (const node of this.sprites.keys()) this.applySprite(node);

    this.ticketKey = null;
    this.stackKey = null;
    this.livesKey = '';
    this.sync();
  }

  /**
   * Cinta masking sobre el frente de una bandeja apoyada abajo en su casilla: el frente liso mide 9
   * filas y la cinta 7, con 1 de margen arriba y abajo; el texto (mayúsculas de 3.8 pixeles) queda con aire. Cada
   * cinta tiene su propia inclinación y un pequeño desfase, alternando, para que parezcan pegadas a mano.
   */
  private placeTape(tape: HTMLElement, key: string, [, , w, h]: Rect, index: number) {
    const tilt = [-2, 1.5, -1, 2.2, -1.6, 1][index % 6];
    const shift = [0, 1, -1, 0, 1, -1][index % 6];
    const entry = this.atlas.entries[key];
    const s = this.scale;
    Object.assign(tape.style, {
      left: `${(Math.floor((w - entry.width) / 2) + 2 + shift) * s}px`,
      top: `${(h - 9) * s}px`,
      width: `${(entry.width - 4) * s}px`, // «Lechuga», la más larga, mide 25 px
      height: `${7 * s}px`,
      transform: `rotate(${tilt}deg)`,
    });
  }

  private place(node: HTMLElement, [x, y, w, h]: Rect) {
    const s = this.scale;
    Object.assign(node.style, { left: `${x * s}px`, top: `${y * s}px`, width: `${w * s}px`, height: `${h * s}px` });
  }

  private rectFor(target: Target): Rect | null {
    const l = this.layout;
    switch (target.kind) {
      case 'charola':
        return l.charola;
      case 'tocino':
        return l.tocino;
      case 'slot':
        return target.index === undefined ? null : l.slots[target.index];
      case 'ingredient':
        return (l.bins as Record<string, Rect>)[target.id] ?? (l.bottles as Record<string, Rect>)[target.id] ?? null;
      default:
        return null;
    }
  }

  private nodeFor(target: Target): HTMLElement | null {
    switch (target.kind) {
      case 'ok':
        return this.okButton;
      case 'charola':
        return this.charola;
      case 'tocino':
        return this.tocino;
      case 'slot':
        return target.index === undefined ? null : this.slots[target.index].button;
      case 'ingredient':
        return this.bins.get(target.id as BinId)?.button ?? this.bottles.get(target.id as SalsaId)?.button ?? null;
    }
  }

  // ── Sincronización por cuadro ────────────────────────────────────────────

  sync() {
    const g = this.game;
    const order = g.order;
    const now = performance.now();

    this.hud.hidden = !(g.playing || g.mode === 'fin');
    this.pauseButton.hidden = !g.playing || g.paused;
    const livesKey = `${g.lives}/${g.config.lives}`;
    if (livesKey !== this.livesKey) {
      this.livesKey = livesKey;
      for (const node of this.lives.children) this.sprites.delete(node as HTMLElement);
      this.lives.replaceChildren();
      this.lives.setAttribute('aria-label', `${g.lives} de ${g.config.lives} vidas`);
      for (let i = 0; i < g.config.lives; i++) {
        this.setSprite(el('span', 'mg-heart mg-sprite', this.lives), i < g.lives ? 'corazon:lleno' : 'corazon:vacio');
      }
    }
    setText(this.score, `CLIENTES ${String(g.served).padStart(2, '0')}`);
    setText(this.best, `RÉCORD ${String(g.best).padStart(2, '0')}`);

    // Cliente: su look sale de la orden; la cara, de la paciencia (o de cómo se fue).
    const ratio = order && Number.isFinite(order.patienceMax) ? Math.min(1, Math.max(0, order.patience / order.patienceMax)) : 1;
    if (this.leaving && (order || now > this.leaving.until)) this.leaving = null;
    const shown = order
      ? { key: CUSTOMERS[order.look % CUSTOMERS.length], face: ratio < 0.3 ? FACE.enojado : FACE.esperando }
      : this.leaving;
    this.customer.classList.toggle('is-away', !shown);
    if (shown) this.setSprite(this.customer, shown.key, shown.face);
    const timed = !!order && Number.isFinite(order.patienceMax);
    const happy = !order && this.leaving?.face === FACE.feliz;
    const mood = !order && this.leaving ? (happy ? 'feliz' : 'enojado') : ratio < 0.3 ? 'enojado' : ratio < 0.6 ? 'impaciente' : 'tranquilo';
    const timeLabel = order ? (timed ? `${Math.ceil(Math.max(0, order.patience))} s` : 'Sin prisa') : happy ? '¡Gracias!' : 'Sin tiempo';
    this.patience.hidden = !shown;
    this.patience.dataset.mood = mood;
    this.patience.dataset.timed = String(timed);
    this.patienceAttention.hidden = !timed || ratio >= 0.6;
    this.setSprite(this.patienceAttention, ratio < 0.3 ? 'paciencia_urgente' : 'paciencia_urgente:amarillo');
    setText(this.patienceTime, timeLabel);
    this.patience.setAttribute('aria-label', `Cliente ${mood}. ${timed ? `Tiempo restante: ${timeLabel}` : timeLabel}`);
    const patienceRatio = order ? ratio : happy ? 1 : 0;
    this.patienceFill.style.width = `${patienceRatio * 100}%`;
    this.patienceTrack.setAttribute('aria-valuenow', String(Math.round(patienceRatio * 100)));
    this.patienceTrack.setAttribute('aria-valuetext', order && !timed ? 'Sin límite de tiempo' : `${Math.round(patienceRatio * 100)} % de paciencia`);


    const ticketKey = order ? `${order.recipe.name}:${order.recipe.stack.join()}:${g.stack.length}` : '';
    if (ticketKey !== this.ticketKey) {
      this.ticketKey = ticketKey;
      this.renderTicket();
    }
    const stackKey = g.stack.join();
    if (stackKey !== this.stackKey) {
      this.stackKey = stackKey;
      this.renderStack();
    }

    // Las tres zonas conservan su color; la iluminación avanza de forma continua.
    const c = g.config.grill;

    const smokeFrame = this.reduced ? 0 : Math.floor(now / SMOKE_FRAME_MS);
    this.slots.forEach((slot, i) => {
      const state = g.grill.state(i);
      const ingredient = g.grill.ingredient(i);
      const rect = this.layout.slots[i];
      slot.button.classList.toggle('is-off', i >= g.grill.active);
      slot.button.dataset.state = state ?? '';
      slot.button.setAttribute('aria-label', `Lugar ${i + 1} de la plancha: ${state ? `${ingredient === 'tocino' ? 'Tocino' : 'Carne'}, ${ingredient === 'tocino' ? BACON_LABEL[state] : PATTY_LABEL[state]}` : 'vacío'}`);
      slot.patty.hidden = !state;
      if (state) this.setSprite(slot.patty, `${ingredient === 'tocino' ? 'tocino_plancha' : 'carne'}:${state === 'aviso' ? 'perfecta' : state}`, 0, [0, 0, rect[2], rect[3] - 12]);
      const smoking = state === 'aviso' || state === 'quemada';
      slot.smoke.hidden = !smoking;
      if (smoking) this.setSprite(slot.smoke, state === 'quemada' ? 'humo:negro' : 'humo:blanco', smokeFrame, [0, 0, rect[2], 14]);
      slot.gauge.hidden = !state;
      if (state) {
        const gauge = cookingGauge(g.grill.cooking[i] ?? 0, g.grill.configFor(i, c));
        slot.track.style.setProperty('--cook-end', `${gauge.cookingEnd}%`);
        slot.track.style.setProperty('--ready-end', `${gauge.readyEnd}%`);
        slot.fill.style.clipPath = `inset(0 ${100 - gauge.progress}% 0 0)`;
        slot.signal.hidden = state !== 'aviso';
      }
    });

    this.syncTutorial();
    this.syncOverlay();
  }

  private syncTutorial() {
    const g = this.game;
    const tutorial = g.mode === 'tutorial';
    const dim = (node: HTMLElement, target: Target) => node.classList.toggle('is-dim', tutorial && !g.allows(target));
    dim(this.charola, { kind: 'charola' });
    dim(this.tocino, { kind: 'tocino' });
    for (const [id, { button }] of this.bins) dim(button, { kind: 'ingredient', id });
    for (const [id, { button }] of this.bottles) dim(button, { kind: 'ingredient', id });
    this.slots.forEach((slot, index) => dim(slot.button, { kind: 'slot', index }));

    const step = g.step;
    this.bubble.hidden = !step;
    if (step) setText(this.bubbleText, step.text);
    this.okButton.hidden = step?.target?.kind !== 'ok';

    let target = step?.target ?? null;
    if (target?.kind === 'slot') {
      const index = this.slots.findIndex((_, i) => g.allows({ kind: 'slot', index: i }));
      target = index >= 0 ? { kind: 'slot', index } : null;
    }
    const rect = target ? this.rectFor(target) : null;
    this.arrow.hidden = !rect;
    if (rect) {
      const [x, y, w, h] = rect;
      const top = y - 10 < 0 ? y + h + 2 : y - 10;
      this.place(this.arrow, [Math.floor(x + w / 2 - 4), top, 9, 8]);
      this.setSprite(this.arrow, 'flecha');
    }
  }

  private syncOverlay() {
    const g = this.game;
    const hint = g.playing ? g.hint : null;
    const key = `${g.mode}:${g.paused}:${hint}:${g.served}:${g.best}:${g.tutorialDone}`;
    if (key === this.overlayKey) return;
    this.overlayKey = key;

    const o = this.overlay;
    o.replaceChildren();
    const title = (text: string) => el('p', 'mg-overlay-title', o, text);
    const text = (value: string) => el('p', 'mg-overlay-text', o, value);
    const action = (label: string, fn: () => void) => {
      const b = el('button', 'mg-overlay-btn', o, label);
      b.type = 'button';
      b.addEventListener('click', () => this.act(fn));
      return b;
    };
    const orderLink = () => {
      const a = el('a', 'mg-overlay-btn mg-overlay-link', o, 'Pídela de verdad');
      a.href = '#pedir';
    };

    let focus: HTMLElement | null = null;
    if (g.paused) {
      title('Pausa');
      text(g.mode === 'tutorial' ? 'Tómate tu tiempo.' : 'El cliente te espera: el tiempo está detenido.');
      focus = action('Continuar', () => g.resume());
      action('Volver a empezar', () => g.restart()).classList.add('is-secondary');
    } else if (g.mode === 'inicio') {
      title('¡Arma la hamburguesa!');
      text('Un minijuego rapidito: cocina la carne y el tocino y arma la orden del cliente.');
      action('Jugar', () => g.play());
      if (g.tutorialDone) action('Ver tutorial', () => g.startTutorial()).classList.add('is-secondary');
    } else if (g.mode === 'oferta') {
      title('¡Cliente feliz!');
      text('Te salió perfecta. ¿Ya se te antojó?');
      orderLink();
      focus = action('Seguir jugando', () => g.startInfinite());
    } else if (g.mode === 'fin') {
      title('Se acabó el turno');
      text(`Atendiste a ${g.served} ${g.served === 1 ? 'cliente' : 'clientes'}.`);
      text(this.lastRecord ? '¡Nuevo récord!' : `Récord: ${g.best}`);
      focus = action('Jugar otra vez', () => g.startInfinite());
      orderLink();
    } else if (hint) {
      text(HINT_TEXT[hint](g));
      focus = action('Entendido', () => g.dismissHint());
    }
    o.hidden = o.childElementCount === 0;
    focus?.focus({ preventScroll: true });
  }

  private renderTicket() {
    const g = this.game;
    const order = g.order;
    this.ticket.hidden = !order;
    for (const node of this.ticketRows.querySelectorAll('.mg-sprite')) this.sprites.delete(node as HTMLElement);
    this.ticketRows.replaceChildren();
    if (!order) return;
    const items = order.recipe.stack;
    setText(this.ticketName, `${order.recipe.name} · ${g.stack.length}/${items.length}`);
    const rowH = Math.min(9, Math.floor((this.layout.ticket[3] - 18) / items.length));
    this.ticket.style.height = `${(18 + rowH * items.length) * this.scale}px`;
    for (let i = 0; i < items.length; i++) {
      const info = INGREDIENTS[items[i]];
      const li = el('li', 'mg-ticket-row', this.ticketRows);
      li.style.height = `${rowH * this.scale}px`;
      li.classList.toggle('is-done', i < g.stack.length);
      li.classList.toggle('is-next', i === g.stack.length);
      if (i === g.stack.length) li.setAttribute('aria-current', 'step');
      li.setAttribute('aria-label', `${info.label}${i < g.stack.length ? ', completado' : i === g.stack.length ? ', siguiente' : ''}`);
      const checkbox = el('span', 'mg-ticket-check mg-sprite', li);
      checkbox.setAttribute('aria-hidden', 'true');
      const checkboxSprite = rowH < 7 ? 'casilla_comanda_compacta' : 'casilla_comanda';
      this.setSprite(checkbox, i < g.stack.length ? `${checkboxSprite}:marcada` : checkboxSprite);
      const label = items[i] === 'pan_base' ? 'Pan base' : items[i] === 'pan_medio' ? 'Pan medio' : items[i] === 'pan_tapa' ? 'Pan tapa' : info.short;
      el('span', 'mg-ticket-label', li, label);
    }
  }

  /**
   * Pila en vista 3/4: cada capa se apoya por su ancla (su base) sobre el centro del plato y la
   * siguiente sube según el grosor de la anterior; así cada capa tapa la cara de arriba de la de abajo.
   */
  private renderStack() {
    const s = this.scale;
    const [px, py] = this.layout.plate;
    const [plateX, plateY] = ANCHORS.plato;
    for (const node of this.stackLayer.children) this.sprites.delete(node as HTMLElement);
    this.stackLayer.replaceChildren();
    let base = py + plateY;
    for (const id of this.game.stack) {
      const key = STACK_SPRITE[id];
      const [ax, ay] = ANCHORS[key.split(':')[0]];
      const item = el('div', 'mg-stack-item mg-sprite', this.stackLayer);
      item.title = INGREDIENTS[id].label;
      this.setSprite(item, key);
      Object.assign(item.style, { left: `${(px + plateX - ax) * s}px`, top: `${(base - ay) * s}px` });
      base -= INGREDIENTS[id].height;
    }
  }

  // ── Eventos ──────────────────────────────────────────────────────────────

  private squeeze(id: SalsaId) {
    const bottle = this.bottles.get(id);
    if (!bottle) return;
    const rect = this.layout.bottles[id];
    this.setSprite(bottle.sprite, atlasKey('bote', id), 1, rect);
    setTimeout(() => this.setSprite(bottle.sprite, atlasKey('bote', id), 0, this.layout.bottles[id]), 180);
  }

  private onEvent(event: GameEvent) {
    const g = this.game;
    const s = this.scale;
    const anim = !this.reduced;
    switch (event.type) {
      case 'placed': {
        this.sync();
        if (INGREDIENTS[event.id].kind === 'salsa') this.squeeze(event.id as SalsaId);
        const item = this.stackLayer.lastElementChild;
        if (item && anim) {
          gsap.fromTo(item, { y: -12 * s, opacity: 0 }, { y: 0, opacity: 1, duration: 0.18, ease: 'power2.out', clearProps: 'transform,opacity' });
        }
        break;
      }
      case 'rejected': {
        const node = this.nodeFor(event.target);
        if (node && anim) gsap.fromTo(node, { x: -2 * s }, { x: 0, duration: 0.35, ease: 'elastic.out(1, 0.3)', clearProps: 'transform' });
        const message = REJECT_TEXT[event.reason];
        if (message) this.showToast(message);
        break;
      }
      case 'patty-added':
        this.sync();
        if (anim) gsap.fromTo(this.slots[event.slot].patty, { y: -8 * s }, { y: 0, duration: 0.2, ease: 'bounce.out', clearProps: 'transform' });
        break;
      case 'patty-state':
        if (event.state === 'perfecta') this.announce(`${g.grill.ingredient(event.slot) === 'tocino' ? 'Tocino listo' : 'Carne lista'} en el lugar ${event.slot + 1}`);
        if (event.state === 'quemada') this.announce(`Se quemó ${g.grill.ingredient(event.slot) === 'tocino' ? 'el tocino' : 'la carne'} del lugar ${event.slot + 1}`);
        if (event.state === 'perfecta' && anim) {
          gsap.fromTo(this.slots[event.slot].button, { filter: 'brightness(1.8)' }, { filter: 'brightness(1)', duration: 0.4, clearProps: 'filter' });
        }
        break;
      case 'patty-discarded':
        break;
      case 'customer-arrived':
        this.leaving = null;
        this.sync();
        this.announce(`Cliente nuevo: ${event.recipe.name}`);
        if (anim) {
          gsap.fromTo(this.customer, { x: -16 * s, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: 'power2.out', clearProps: 'transform,opacity' });
        }
        break;
      case 'served': {
        this.announce('¡Orden entregada!');
        const key = this.sprites.get(this.customer)?.key;
        if (key) this.leaving = { key, face: FACE.feliz, until: performance.now() + 800 };
        if (anim) gsap.fromTo(this.customer, { y: 0 }, { y: -6 * s, duration: 0.15, yoyo: true, repeat: 1, ease: 'power1.out', clearProps: 'transform' });
        break;
      }
      case 'customer-left': {
        this.showToast('¡Se fue enojado!');
        this.announce(`El cliente se fue enojado. Te quedan ${event.lives} vidas.`);
        const key = this.sprites.get(this.customer)?.key;
        if (key) this.leaving = { key, face: FACE.enojado, until: performance.now() + 800 };
        if (anim) gsap.fromTo(this.customer, { x: -2 * s }, { x: 0, duration: 0.4, ease: 'elastic.out(1, 0.25)', clearProps: 'transform' });
        break;
      }
      case 'game-over':
        this.lastRecord = event.record;
        this.announce(`Fin del turno: atendiste a ${event.served} clientes.`);
        break;
    }
  }

  private showToast(message: string) {
    setText(this.toast, message);
    this.toast.classList.add('is-on');
    clearTimeout(this.toastTimer);
    this.toastTimer = window.setTimeout(() => this.toast.classList.remove('is-on'), 1100);
  }

  private announce(message: string) {
    setText(this.live, message);
  }
}
