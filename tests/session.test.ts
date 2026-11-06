import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { createConfig } from '../src/game/game/config.ts';
import { inputFor } from '../src/game/game/ingredients.ts';
import { CATALOG } from '../src/game/game/recipes.ts';
import { Game, type GameEvent } from '../src/game/game/session.ts';
import { memoryStore, type Store } from '../src/game/game/storage.ts';
import { seeded } from './helpers.ts';

function setup(store: Store = memoryStore()) {
  const game = new Game(createConfig(), store, seeded(1));
  const events: GameEvent[] = [];
  game.on((e) => events.push(e));
  return { game, events, store };
}

const readySlot = (game: Game, ingredient = 'carne') => game.grill.cooking.findIndex((_, i) => game.grill.state(i) === 'perfecta' && game.grill.ingredient(i) === ingredient);

/** Prepara la orden actual tocando lo que corresponde, esperando la carne cuando hace falta. */
function cookOrder(game: Game) {
  while (game.order && game.nextIngredient) {
    const next = game.nextIngredient;
    if (next === 'carne' || next === 'tocino') {
      if (readySlot(game, next) < 0) {
        if (game.grill.cooking.every((t) => t === null)) game.tapCharola(next);
        game.update(next === 'tocino' ? game.config.grill.baconCookTime : game.config.grill.cookTime);
      }
      game.tapSlot(readySlot(game, next));
    } else {
      game.tapIngredient(inputFor(next)!);
    }
  }
}

describe('Tutorial', () => {
  it('no se puede perder aunque pase mucho tiempo y termina en la oferta', () => {
    const { game, store } = setup();
    game.play();
    assert.equal(game.mode, 'tutorial');

    game.ok();
    game.tapCharola();
    game.tapIngredient('pan');
    for (let i = 0; i < 600; i++) game.update(0.5); // cinco minutos sin tocar
    assert.equal(game.grill.state(0), 'perfecta');
    assert.equal(game.lives, game.config.lives);

    game.tapSlot(0);
    for (const id of ['queso', 'lechuga', 'tomate', 'catsup', 'pan'] as const) game.tapIngredient(id);
    assert.equal(game.mode, 'oferta');
    assert.equal(store.get('tutorial', false), true);
  });

  it('solo acepta el elemento señalado', () => {
    const { game, events } = setup();
    game.play();
    game.tapCharola(); // todavía en el paso del «ok»
    assert.equal(game.grill.add(), 0); // la plancha seguía vacía
    assert.ok(events.some((e) => e.type === 'rejected' && e.reason === 'tutorial'));
  });

  it('salta la espera si la carne ya estaba lista', () => {
    const { game } = setup();
    game.play();
    game.ok();
    game.tapCharola();
    game.update(30); // se cocina antes de poner el pan
    game.tapIngredient('pan');
    assert.equal(game.step?.target?.kind, 'slot');
  });
});

describe('Modo infinito', () => {
  it('quien ya hizo el tutorial entra directo', () => {
    const store = memoryStore();
    store.set('tutorial', true);
    const { game } = setup(store);
    game.play();
    assert.equal(game.mode, 'infinito');
    assert.equal(game.customerNumber, 1);
  });

  it('la carne lista no pasa sin pan', () => {
    const { game, events } = setup();
    game.startInfinite();
    game.dismissHint();
    game.tapCharola();
    game.update(game.config.grill.cookTime);
    game.tapSlot(0);
    assert.equal(game.stack.length, 0);
    assert.ok(events.some((e) => e.type === 'rejected' && e.reason === 'falta-pan'));
  });

  it('la carne quemada ocupa su lugar hasta descartarla', () => {
    const { game } = setup();
    game.startInfinite();
    game.dismissHint();
    game.tapCharola();
    game.tapCharola();
    game.update(30);
    assert.equal(game.hint, 'quemada');
    game.dismissHint();
    game.tapCharola(); // plancha llena de carnes quemadas
    assert.equal(game.grill.state(0), 'quemada');
    game.tapSlot(0);
    assert.equal(game.grill.state(0), null);
  });

  it('la casilla de pan pone el pan que toque: abajo, en medio y arriba', () => {
    const { game } = setup();
    game.startInfinite();
    game.dismissHint();
    game.order = { recipe: CATALOG.tresPanes, patience: 999, patienceMax: 999, look: 0 };
    game.stack = [];
    cookOrder(game);
    assert.equal(game.served, 1);
    const panes = CATALOG.tresPanes.stack.filter((id) => id.startsWith('pan'));
    assert.deepEqual(panes, ['pan_base', 'pan_medio', 'pan_tapa']);
  });

  it('toca cada ingrediente quemado para liberar su lugar sin una basura', () => {
    const { game, events } = setup();
    game.debugJumpTo(13);
    while (game.hint) game.dismissHint();
    game.tapCharola();
    game.tapCharola('tocino');
    game.update(6);
    while (game.hint) game.dismissHint();
    game.tapCharola();
    game.tapSlot(0);
    game.tapSlot(1);
    assert.deepEqual([0, 1, 2].map(i => game.grill.state(i)), [null, null, 'cruda']);
    assert.equal(events.filter(e => e.type === 'patty-discarded').length, 2);
  });

  it('un ingrediente equivocado cuesta paciencia', () => {
    const { game } = setup();
    game.startInfinite();
    game.dismissHint();
    const before = game.order!.patience;
    game.tapIngredient('queso'); // primero va el pan
    assert.equal(game.order!.patience, before - game.config.wrongPenalty);
    assert.equal(game.stack.length, 0);
  });

  it('entregar suma un cliente y llega el siguiente', () => {
    const { game } = setup();
    game.startInfinite();
    game.dismissHint();
    cookOrder(game);
    assert.equal(game.served, 1);
    game.update(game.config.betweenCustomers + 0.01);
    assert.equal(game.customerNumber, 2);
  });

  it('se pierde al acabarse las vidas y guarda el récord', () => {
    const { game, store, events } = setup();
    game.startInfinite();
    game.dismissHint();
    cookOrder(game);
    for (let i = 0; i < 2000 && game.mode === 'infinito'; i++) {
      game.update(0.5);
      while (game.hint) game.dismissHint();
    }
    assert.equal(game.mode, 'fin');
    assert.equal(game.lives, 0);
    assert.equal(store.get('record', 0), 1);
    assert.ok(events.some((e) => e.type === 'game-over' && e.record));
  });

  it('en pausa no corre el tiempo ni se aceptan toques', () => {
    const { game } = setup();
    game.startInfinite();
    game.dismissHint();
    game.tapCharola();
    const patience = game.order!.patience;
    const cooking = game.grill.cooking[0];
    game.pause();
    game.update(60);
    game.tapIngredient('pan');
    assert.equal(game.order!.patience, patience);
    assert.equal(game.grill.cooking[0], cooking);
    assert.equal(game.stack.length, 0);
    game.resume();
    game.update(1);
    assert.ok(game.order!.patience < patience);
  });

  it('volver a empezar reinicia la partida y quita la pausa', () => {
    const { game } = setup();
    game.startInfinite();
    game.dismissHint();
    cookOrder(game);
    game.pause();
    game.restart();
    assert.equal(game.paused, false);
    assert.equal(game.served, 0);
    assert.equal(game.mode, 'infinito');
  });

  it('solo se puede pausar mientras se juega', () => {
    const { game } = setup();
    game.pause();
    assert.equal(game.paused, false);
  });

  it('permite cocinar en los tres lugares desde el primer cliente y conserva esa capacidad', () => {
    const { game } = setup();
    game.startInfinite();
    assert.equal(game.grill.active, 3);
    assert.equal(game.grill.cooking.length, 3);
    while (game.hint) game.dismissHint();
    for (let i = 0; i < 4; i++) game.tapCharola();
    assert.deepEqual(game.grill.cooking, [0, 0, 0]);
    game.debugJumpTo(8);
    assert.equal(game.grill.active, 3);
    game.debugJumpTo(13);
    assert.equal(game.grill.active, 3);
    game.debugJumpTo(30);
    assert.equal(game.grill.active, 3);
  });
});
