import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { createConfig } from '../src/game/game/config.ts';
import { Grill } from '../src/game/game/grill.ts';
import { minimumTime } from '../src/game/game/difficulty.ts';
import { CATALOG, generateRecipe, validateRecipe } from '../src/game/game/recipes.ts';
import { Game } from '../src/game/game/session.ts';
import { memoryStore } from '../src/game/game/storage.ts';
import { seeded } from './helpers.ts';

describe('Tocino en la misma plancha', () => {
  const config = createConfig();
  it('está listo a los 2 s; la carne sigue necesitando 3 s', () => {
    const grill = new Grill(3);
    grill.add('tocino');
    grill.add();
    grill.update(1.99, config.grill);
    assert.equal(grill.state(0), 'cocinandose');
    grill.update(0.01, config.grill);
    assert.equal(grill.state(0), 'perfecta');
    assert.equal(grill.state(1), 'cocinandose');
    grill.update(1, config.grill);
    assert.equal(grill.state(1), 'perfecta');
    assert.equal(grill.configFor(0, config.grill).cookTime, 2);
  });

  it('conserva su ventana lista y se quema a los 4 s', () => {
    const grill = new Grill(1);
    grill.add('tocino');
    grill.update(3.2, config.grill);
    assert.equal(grill.state(0), 'aviso');
    grill.update(0.8, config.grill);
    assert.equal(grill.state(0), 'quemada');
    grill.remove(0);
    assert.equal(grill.ingredient(0), null);
    grill.add();
    assert.equal(grill.ingredient(0), 'carne');
  });

  it('rechaza tocino crudo o una carne cuando la comanda pide tocino', () => {
    const game = new Game(createConfig(), memoryStore());
    game.startInfinite();
    while (game.hint) game.dismissHint();
    game.order = { recipe: CATALOG.conTocino, patience: 60, patienceMax: 60, look: 0 };
    game.stack = ['pan_base', 'carne', 'queso'];
    game.tapCharola('tocino');
    game.tapCharola();
    game.tapSlot(0);
    assert.equal(game.stack.length, 3);
    game.update(3);
    game.tapSlot(1);
    assert.equal(game.grill.ingredient(1), 'carne');
    assert.equal(game.stack.length, 3);
    game.tapSlot(0);
    assert.equal(game.stack.at(-1), 'tocino');
    assert.equal(game.grill.state(0), null);
  });

  it('incluye tocino desde el segundo nivel y valida su orden en la receta', () => {
    const rng = seeded(22);
    assert.ok(Array.from({ length: 100 }, () => generateRecipe(2, 100, rng)).some(r => r.stack.includes('tocino')));
    assert.deepEqual(validateRecipe(CATALOG.conTocino.stack), []);
    assert.notDeepEqual(validateRecipe(['pan_base', 'tocino', 'carne', 'pan_tapa']), []);
    assert.notDeepEqual(validateRecipe(['pan_base', 'carne', 'tocino', 'tocino', 'pan_tapa']), []);
  });

  it('cuenta la cocción de ambos ingredientes en la paciencia', () => {
    const stack = ['pan_base', 'carne', 'tocino', 'pan_tapa'] as const;
    assert.equal(minimumTime(stack, 1, config), 5 + 6 * config.patience.tapTime);
    assert.equal(minimumTime(stack, 2, config), 3 + 6 * config.patience.tapTime);
  });
});
