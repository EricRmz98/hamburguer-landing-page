import gsap from 'gsap';
import { fitStage, type Layout, type Rect } from '../engine/stage.ts';
import type { PattyState } from '../game/grill.ts';
import { BIN_IDS, INGREDIENTS, SALSAS, inputColor, inputLabel, type BinId, type SalsaId } from '../game/ingredients.ts';
import type { Game, GameEvent, HintId, RejectReason } from '../game/session.ts';
import type { Target } from '../game/tutorial.ts';
import { LAYOUTS } from '../layouts/index.ts';

// Vista provisional con bloques de color: sirve para fijar mecánica y tiempos antes de los sprites.

const PATTY: Record<PattyState, { color: string; label: string }> = {
  cruda: { color: '#e8908a', label: 'cruda' },
  cocinandose: { color: '#b86a4b', label: 'cocinando' },
  perfecta: { color: '#a0602a', label: '¡lista!' },
  aviso: { color: '#4a2a14', label: '¡ya!' },
  quemada: { color: '#151111', label: 'quemada' },
};

const LOOKS = ['#e07a5f', '#3d85c6', '#81b29a', '#f2cc8f', '#9b5de5', '#ef476f'];

const REJECT_TEXT: Partial<Record<RejectReason, string>> = {
  'no-toca': 'Ese no va ahora',
  'falta-pan': 'Primero el pan de abajo',
  todavia: 'Todavía no está lista',
  'plancha-llena': 'La plancha está llena',
  'sin-quemadas': 'No hay carne quemada que tirar',
  'sin-orden': 'Espera al siguiente cliente',
};

const HINT_TEXT: Record<HintId, (game: Game) => string> = {
  infinito: (g) =>
    `Ahora va en serio: los clientes se impacientan, la carne se puede quemar y tienes ${g.lives} vidas. ¿Cuántos clientes aguantas?`,
  quemada: () =>
    'Se quemó una carne. Cuando la barra parpadea en rojo, sácala rápido. Si ya se quemó, tócala para tirarla, o toca la basura para tirar todas las quemadas de una vez.',
  plancha: (g) => `¡La plancha creció! Ahora tienes ${g.grill.active} lugares.`,
  'tres-panes': () => 'Esta orden lleva pan en medio. Sigue la comanda de abajo hacia arriba.',
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
  label: HTMLSpanElement;
  gauge: HTMLDivElement;
  fill: HTMLDivElement;
}

export class GreyboxView {
  readonly stage: HTMLDivElement;

  private root: HTMLElement;
  private game: Game;
  private layout: Layout = LAYOUTS.horizontal;
  private scale = 0;
  private reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  private hud: HTMLDivElement;
  private lives: HTMLSpanElement;
  private score: HTMLSpanElement;
  private pauseButton: HTMLButtonElement;
  private ticket: HTMLDivElement;
  private ticketName: HTMLDivElement;
  private ticketRows: HTMLOListElement;
  private customer: HTMLDivElement;
  private face: HTMLSpanElement;
  private patience: HTMLDivElement;
  private patienceBar: HTMLDivElement;
  private counter: HTMLDivElement;
  private plate: HTMLDivElement;
  private stackLayer: HTMLDivElement;
  private grill: HTMLDivElement;
  private slots: SlotView[] = [];
  private bottles = new Map<SalsaId, HTMLButtonElement>();
  private bins = new Map<BinId, HTMLButtonElement>();
  private charola: HTMLButtonElement;
  private basura: HTMLButtonElement;
  private bubble: HTMLDivElement;
  private bubbleText: HTMLParagraphElement;
  private okButton: HTMLButtonElement;
  private arrow: HTMLDivElement;
  private toast: HTMLDivElement;
  private overlay: HTMLDivElement;
  private live: HTMLDivElement;

  private ticketKey: string | null = null;
  private stackKey: string | null = null;
  private overlayKey = '';
  private lastRecord = false;
  private toastTimer = 0;

  constructor(root: HTMLElement, game: Game) {
    this.root = root;
    this.game = game;
    root.replaceChildren();
    const stage = (this.stage = el('div', 'mg-stage', root));

    this.hud = el('div', 'mg-hud', stage);
    this.lives = el('span', 'mg-lives', this.hud);
    this.score = el('span', 'mg-score', this.hud);
    this.pauseButton = el('button', 'mg-pause', stage, '❚❚');
    this.pauseButton.type = 'button';
    this.pauseButton.setAttribute('aria-label', 'Pausar (P)');
    this.pauseButton.addEventListener('click', () => this.act(() => game.pause()));

    // Orden de pintado: el cliente queda detrás de la barra, y todo lo de cocina encima de ella.
    this.customer = el('div', 'mg-customer', stage);
    this.face = el('span', 'mg-face', this.customer);
    this.patience = el('div', 'mg-patience', stage);
    this.patienceBar = el('div', 'mg-patience-bar', this.patience);
    this.counter = el('div', 'mg-counter', stage);

    this.ticket = el('div', 'mg-ticket', stage);
    this.ticketName = el('div', 'mg-ticket-name', this.ticket);
    this.ticketRows = el('ol', 'mg-ticket-rows', this.ticket);
    this.ticket.setAttribute('aria-label', 'Comanda');

    this.plate = el('div', 'mg-plate', stage, 'plato');
    this.stackLayer = el('div', 'mg-stack', stage);

    for (const id of SALSAS) {
      const button = this.button('mg-bottle', INGREDIENTS[id].short, `Bote de ${INGREDIENTS[id].label}`, () =>
        game.tapIngredient(id),
      );
      button.style.background = INGREDIENTS[id].color;
      this.bottles.set(id, button);
    }

    this.grill = el('div', 'mg-grill', stage);
    for (let i = 0; i < game.config.grill.maxSlots; i++) {
      const button = this.button('mg-slot', '', '', () => game.tapSlot(i));
      const gauge = el('div', 'mg-gauge', button);
      gauge.setAttribute('aria-hidden', 'true');
      this.slots.push({
        button,
        patty: el('div', 'mg-patty', button),
        label: el('span', 'mg-slot-label', button),
        gauge,
        fill: el('div', 'mg-gauge-fill', gauge),
      });
    }

    this.charola = this.button('mg-charola', 'Carne cruda', 'Poner carne en la plancha', () => game.tapCharola());
    this.basura = this.button('mg-basura', 'Basura', 'Tirar las carnes quemadas', () => game.tapBasura());

    for (const id of BIN_IDS) {
      const button = this.button('mg-bin', inputLabel(id), inputLabel(id), () => game.tapIngredient(id));
      button.style.background = inputColor(id);
      this.bins.set(id, button);
    }

    this.bubble = el('div', 'mg-bubble', stage);
    this.bubbleText = el('p', 'mg-bubble-text', this.bubble);
    this.okButton = el('button', 'mg-ok', this.bubble, 'Empezar');
    this.okButton.type = 'button';
    this.okButton.addEventListener('click', () => this.act(() => game.ok()));

    this.arrow = el('div', 'mg-arrow', stage, '▼');
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

  private button(className: string, text: string, label: string, action: () => void) {
    const button = el('button', `mg-btn ${className}`, this.stage, text);
    button.type = 'button';
    if (label) button.setAttribute('aria-label', label);
    button.addEventListener('click', () => this.act(action));
    return button;
  }

  private act(action: () => void) {
    action();
    this.sync();
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
    this.place(this.patience, layout.patience);
    this.place(this.counter, layout.counter);
    this.place(this.plate, layout.plate);
    this.place(this.bubble, layout.bubble);
    this.place(this.grill, layout.grill);
    this.place(this.charola, layout.charola);
    this.place(this.basura, layout.basura);
    this.slots.forEach((slot, i) => this.place(slot.button, layout.slots[i]));
    for (const [id, button] of this.bottles) this.place(button, layout.bottles[id]);
    for (const [id, button] of this.bins) this.place(button, layout.bins[id]);

    this.ticketKey = null;
    this.stackKey = null;
    this.sync();
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
      case 'basura':
        return l.basura;
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
      case 'basura':
        return this.basura;
      case 'slot':
        return target.index === undefined ? null : this.slots[target.index].button;
      case 'ingredient':
        return this.bins.get(target.id as BinId) ?? this.bottles.get(target.id as SalsaId) ?? null;
    }
  }

  // ── Sincronización por cuadro ────────────────────────────────────────────

  sync() {
    const g = this.game;
    const order = g.order;

    this.hud.hidden = !(g.mode === 'infinito' || g.mode === 'fin');
    this.pauseButton.hidden = !g.playing || g.paused;
    const lost = Math.max(0, g.config.lives - g.lives);
    setText(this.lives, '♥'.repeat(Math.max(0, g.lives)) + '♡'.repeat(lost));
    setText(this.score, `Clientes ${g.served} · Récord ${g.best}`);

    const ratio = order && Number.isFinite(order.patienceMax) ? Math.max(0, order.patience / order.patienceMax) : 1;
    this.customer.classList.toggle('is-away', !order);
    if (order) this.customer.style.background = LOOKS[order.look % LOOKS.length];
    setText(this.face, ratio < 0.3 ? '•︵•' : '•‿•');
    this.patience.hidden = !order || !Number.isFinite(order.patienceMax);
    this.patienceBar.style.width = `${ratio * 100}%`;
    this.patienceBar.classList.toggle('is-low', ratio < 0.3);

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

    // Zonas del indicador de cocción: amarillo hasta «lista», verde la ventana perfecta, rojo el resto.
    const c = g.config.grill;
    const total = c.cookTime + c.perfectWindow + c.warnTime;
    this.stage.style.setProperty('--g1', `${(c.cookTime / total) * 100}%`);
    this.stage.style.setProperty('--g2', `${((c.cookTime + c.perfectWindow) / total) * 100}%`);

    this.basura.classList.toggle(
      'is-alert',
      g.grill.cooking.some((_, i) => g.grill.state(i) === 'quemada'),
    );

    this.slots.forEach((slot, i) => {
      const state = g.grill.state(i);
      slot.button.classList.toggle('is-off', i >= g.grill.active);
      slot.button.dataset.state = state ?? '';
      slot.patty.hidden = !state;
      if (state) slot.patty.style.background = PATTY[state].color;
      setText(slot.label, state ? PATTY[state].label : '');
      slot.button.setAttribute('aria-label', `Lugar ${i + 1} de la plancha: ${state ? PATTY[state].label : 'vacío'}`);
      slot.gauge.hidden = !state;
      if (state) slot.fill.style.width = `${Math.min(1, g.grill.progress(i, c)) * 100}%`;
    });

    this.syncTutorial();
    this.syncOverlay();
  }

  private syncTutorial() {
    const g = this.game;
    const tutorial = g.mode === 'tutorial';
    const dim = (node: HTMLElement, target: Target) => node.classList.toggle('is-dim', tutorial && !g.allows(target));
    dim(this.charola, { kind: 'charola' });
    dim(this.basura, { kind: 'basura' });
    for (const [id, node] of this.bins) dim(node, { kind: 'ingredient', id });
    for (const [id, node] of this.bottles) dim(node, { kind: 'ingredient', id });
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
      const [x, y, w] = rect;
      const top = y - 10 < 0 ? y + rect[3] + 2 : y - 10;
      this.place(this.arrow, [x + w / 2 - 4, top, 8, 8]);
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
      text('Un minijuego rapidito: cocina la carne y arma la orden del cliente.');
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
    this.ticketRows.replaceChildren();
    if (!order) return;
    setText(this.ticketName, order.recipe.name);
    const items = order.recipe.stack;
    const rowH = Math.min(8, Math.floor((this.layout.ticket[3] - 10) / items.length));
    for (let i = items.length - 1; i >= 0; i--) {
      const info = INGREDIENTS[items[i]];
      const li = el('li', 'mg-ticket-row', this.ticketRows);
      li.style.height = `${rowH * this.scale}px`;
      li.classList.toggle('is-done', i < g.stack.length);
      li.classList.toggle('is-next', i === g.stack.length);
      el('span', 'mg-swatch', li).style.background = info.color;
      el('span', 'mg-ticket-label', li, info.short);
    }
  }

  private renderStack() {
    const s = this.scale;
    const [px, py, pw] = this.layout.plate;
    this.stackLayer.replaceChildren();
    let y = py;
    for (const id of this.game.stack) {
      const info = INGREDIENTS[id];
      y -= info.height;
      const item = el('div', 'mg-stack-item', this.stackLayer);
      item.title = info.label;
      Object.assign(item.style, {
        left: `${(px + pw / 2 - info.width / 2) * s}px`,
        top: `${y * s}px`,
        width: `${info.width * s}px`,
        height: `${info.height * s}px`,
        background: info.color,
      });
    }
  }

  // ── Eventos ──────────────────────────────────────────────────────────────

  private onEvent(event: GameEvent) {
    const s = this.scale;
    const anim = !this.reduced;
    switch (event.type) {
      case 'placed': {
        this.sync();
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
        if (anim) gsap.fromTo(this.slots[event.slot].patty, { scaleX: 0.5 }, { scaleX: 1, duration: 0.2, ease: 'back.out(3)', clearProps: 'transform' });
        break;
      case 'patty-state':
        if (event.state === 'perfecta') this.announce(`Carne lista en el lugar ${event.slot + 1}`);
        if (event.state === 'quemada') this.announce(`Se quemó la carne del lugar ${event.slot + 1}`);
        if (event.state === 'perfecta' && anim) {
          gsap.fromTo(this.slots[event.slot].button, { filter: 'brightness(1.8)' }, { filter: 'brightness(1)', duration: 0.4, clearProps: 'filter' });
        }
        break;
      case 'patty-discarded':
        if (anim) gsap.fromTo(this.basura, { scale: 1.25 }, { scale: 1, duration: 0.3, ease: 'back.out(3)', clearProps: 'transform' });
        break;
      case 'customer-arrived':
        this.sync();
        this.announce(`Cliente nuevo: ${event.recipe.name}`);
        if (anim) {
          gsap.fromTo(this.customer, { x: -16 * s, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3, ease: 'power2.out', clearProps: 'transform,opacity' });
        }
        break;
      case 'served':
        this.announce('¡Orden entregada!');
        if (anim) gsap.fromTo(this.customer, { y: 0 }, { y: -6 * s, duration: 0.15, yoyo: true, repeat: 1, ease: 'power1.out', clearProps: 'transform' });
        break;
      case 'customer-left':
        this.showToast('¡Se fue enojado!');
        this.announce(`El cliente se fue enojado. Te quedan ${event.lives} vidas.`);
        if (anim) gsap.fromTo(this.customer, { x: -2 * s }, { x: 0, duration: 0.4, ease: 'elastic.out(1, 0.25)', clearProps: 'transform' });
        break;
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
