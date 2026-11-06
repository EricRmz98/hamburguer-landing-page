import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { createConfig } from '../src/game/game/config.ts';
import { cookingGauge } from '../src/game/view/cooking-gauge.ts';

describe('Barra continua de cocción', () => {
  const config = createConfig().grill;
  it('conserva las zonas amarilla, verde y roja aunque cambie el avance', () => {
    for (const elapsed of [0, 1.5, 3, 4.2, 5]) {
      const gauge = cookingGauge(elapsed, config);
      assert.equal(gauge.cookingEnd, 60);
      assert.equal(gauge.readyEnd, 84);
    }
    assert.equal(cookingGauge(1.5, config).progress, 30);
    assert.equal(cookingGauge(3, config).progress, 60);
    assert.ok(Math.abs(cookingGauge(4.2, config).progress - 84) < 1e-10);
  });
  it('limita el avance al intervalo de la barra', () => {
    assert.equal(cookingGauge(-1, config).progress, 0);
    assert.equal(cookingGauge(5, config).progress, 100);
    assert.equal(cookingGauge(8, config).progress, 100);
  });
  it('adapta los límites y el avance a los tiempos configurados', () => {
    const adjusted = { ...config, cookTime: 2, perfectWindow: 4, warnTime: 2 };
    const gauge = cookingGauge(3, adjusted);
    assert.equal(gauge.cookingEnd, 25);
    assert.equal(gauge.readyEnd, 75);
    assert.equal(gauge.progress, 37.5);
  });
});
