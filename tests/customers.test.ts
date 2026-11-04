import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';
import { LAYOUTS } from '../src/game/layouts/index.ts';
import { rasterize, resolveSprite } from '../src/game/sprites/define.ts';
import { cliente, CUSTOMERS, CUSTOMER_PROFILES } from '../src/game/sprites/people.ts';

const approved = JSON.parse(readFileSync(new URL('../scripts/sprites/customers-native.json', import.meta.url), 'utf8'));

describe('Elenco nativo aprobado en Endesga 64', () => {
  it('incluye los doce dibujos y alterna la orientación en el orden aprobado', () => {
    assert.equal(CUSTOMERS.length, 12);
    assert.equal(new Set(CUSTOMERS).size, 12);
    assert.deepEqual(CUSTOMER_PROFILES.map(p => p.name), approved.customers.map((p: { name: string }) => p.name));
    assert.deepEqual(Object.keys(cliente.variants), approved.customers.map((p: { id: string }) => p.id));
    CUSTOMER_PROFILES.forEach((p, i) => assert.equal(p.facing, i % 2 ? 'left' : 'right'));
  });

  it('conserva cada celda aprobada después del cambio de paleta', () => {
    for (const person of approved.customers) {
      const resolved = resolveSprite(cliente, person.id);
      const pixels = rasterize(resolved);
      assert.equal(resolved.frames.length, 1);
      assert.equal(createHash('sha256').update(pixels).digest('hex'), person.approved_sha256, person.name);
      assert.deepEqual(resolved.frames[0], person.pixels);
    }
  });

  it('conserva la menor escala de Inés y deja el rostro despejado en ambas disposiciones', () => {
    assert.equal(approved.customers.find((p: { id: string }) => p.id === 'ines').proportion_scale, .85);
    for (const person of approved.customers) {
      const [, top] = person.face_bounds;
      for (const layout of Object.values(LAYOUTS)) {
        assert.ok(layout.customer[1] + top > layout.patience[1] + layout.patience[3]);
      }
    }
  });

  it('comparte la cuadrícula del entorno, sin ampliación fraccionaria ni deformación', () => {
    assert.deepEqual(cliente.size, [96, 120]);
    for (const layout of Object.values(LAYOUTS)) {
      const [x, y, width, height] = layout.customer;
      assert.equal(width / cliente.size[0], 1);
      assert.equal(height / cliente.size[1], 1);
      assert.equal(x + width / 2, layout.w / 2);
      assert.equal(y + approved.waist, layout.counter[1]);
      assert.ok(x >= 0 && x + width <= layout.w);
      assert.ok(layout.patience[1] + layout.patience[3] <= y + 8);
    }
  });
});
