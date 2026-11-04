import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { DEFAULT_CONFIG } from '../src/game/game/config.ts';
import { levelFor, minimumTime, patienceFor } from '../src/game/game/difficulty.ts';
import { Grill, pattyState } from '../src/game/game/grill.ts';
import { CATALOG } from '../src/game/game/recipes.ts';

const c = DEFAULT_CONFIG.grill;

describe('pattyState', () => {
  it('recorre cruda → cocinándose → perfecta → aviso → quemada', () => {
    assert.equal(pattyState(0, c), 'cruda');
    assert.equal(pattyState(c.cookTime * c.rawFraction, c), 'cocinandose');
    assert.equal(pattyState(c.cookTime, c), 'perfecta');
    assert.equal(pattyState(c.cookTime + c.perfectWindow, c), 'aviso');
    assert.equal(pattyState(c.cookTime + c.perfectWindow + c.warnTime, c), 'quemada');
  });
});

describe('Grill', () => {
  it('solo usa los lugares activos', () => {
    const grill = new Grill(4, 2);
    assert.equal(grill.add(), 0);
    assert.equal(grill.add(), 1);
    assert.equal(grill.add(), -1);
    grill.setActive(3);
    assert.equal(grill.add(), 2);
  });

  it('reporta cada cambio de estado una sola vez', () => {
    const grill = new Grill(4);
    grill.add();
    const states: string[] = [];
    for (let i = 0; i < 200; i++) for (const change of grill.update(0.05, c)) states.push(change.state);
    assert.deepEqual(states, ['cocinandose', 'perfecta', 'aviso', 'quemada']);
  });

  it('congelada (tutorial) nunca pasa de perfecta', () => {
    const grill = new Grill(4);
    grill.add();
    for (let i = 0; i < 1000; i++) grill.update(0.1, c, true);
    assert.equal(grill.state(0), 'perfecta');
  });
});

describe('Dificultad', () => {
  const p = DEFAULT_CONFIG.patience;

  it('mantiene tres lugares desde el inicio mientras las recetas suben de nivel', () => {
    assert.deepEqual(
      [1, 8, 13, 21].map((n) => [levelFor(n, DEFAULT_CONFIG).tier, levelFor(n, DEFAULT_CONFIG).slots]),
      [[1, 3], [3, 3], [4, 3], [5, 3]],
    );
  });

  it('la holgura baja con cada cliente y se detiene en el tope', () => {
    assert.equal(levelFor(1, DEFAULT_CONFIG).slack, p.slackStart);
    assert.equal(levelFor(p.slackGrace, DEFAULT_CONFIG).slack, p.slackStart, 'los primeros clientes no bajan');
    assert.ok(levelFor(p.slackGrace + 1, DEFAULT_CONFIG).slack < p.slackStart);
    assert.ok(levelFor(p.slackGrace + 2, DEFAULT_CONFIG).slack < levelFor(p.slackGrace + 1, DEFAULT_CONFIG).slack);
    assert.equal(levelFor(500, DEFAULT_CONFIG).slack, p.slackMin);
    assert.ok(p.slackMin > 1, 'con holgura ≤ 1 una orden perfecta no alcanzaría');
  });

  it('el tiempo mínimo cuenta tandas de carne y toques', () => {
    const torre = CATALOG.cuadruple.stack; // 4 carnes, 12 ingredientes
    assert.equal(minimumTime(torre, 4, DEFAULT_CONFIG), DEFAULT_CONFIG.grill.cookTime + 16 * p.tapTime);
    assert.equal(minimumTime(torre, 2, DEFAULT_CONFIG), 2 * DEFAULT_CONFIG.grill.cookTime + 16 * p.tapTime);
  });

  it('la paciencia siempre supera el tiempo mínimo', () => {
    for (const n of [1, 10, 20, 100]) {
      const level = levelFor(n, DEFAULT_CONFIG);
      for (const recipe of Object.values(CATALOG)) {
        assert.ok(patienceFor(recipe.stack, level, DEFAULT_CONFIG) > minimumTime(recipe.stack, level.slots, DEFAULT_CONFIG));
      }
    }
  });
});
