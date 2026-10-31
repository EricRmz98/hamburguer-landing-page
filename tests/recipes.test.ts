import assert from 'node:assert/strict';
import { describe, it } from 'node:test';
import { DEFAULT_CONFIG } from '../src/game/game/config.ts';
import { stackHeight, type IngredientId } from '../src/game/game/ingredients.ts';
import { CATALOG, generateRecipe, validateRecipe } from '../src/game/game/recipes.ts';
import { seeded } from './helpers.ts';

const MAX = DEFAULT_CONFIG.maxStackHeight;
const count = (stack: readonly IngredientId[], id: IngredientId) => stack.filter((x) => x === id).length;

describe('validateRecipe', () => {
  it('acepta todo el catálogo dentro de la altura máxima', () => {
    for (const [key, recipe] of Object.entries(CATALOG)) {
      assert.deepEqual(validateRecipe(recipe.stack, MAX), [], key);
    }
  });

  const invalid: Record<string, IngredientId[]> = {
    'panes juntos abajo': ['pan_base', 'pan_tapa', 'carne', 'queso'],
    'sin carne': ['pan_base', 'lechuga', 'catsup', 'pan_tapa'],
    'queso sin carne debajo': ['pan_base', 'queso', 'carne', 'pan_tapa'],
    'verdura entre carnes': ['pan_base', 'carne', 'lechuga', 'carne', 'pan_tapa'],
    'salsa antes de verdura': ['pan_base', 'carne', 'catsup', 'lechuga', 'pan_tapa'],
    'dos panes de en medio': ['pan_base', 'carne', 'pan_medio', 'carne', 'pan_medio', 'carne', 'pan_tapa'],
    'pan de en medio sin carne arriba': ['pan_base', 'carne', 'pan_medio', 'lechuga', 'pan_tapa'],
    'cinco carnes': ['pan_base', 'carne', 'carne', 'carne', 'carne', 'carne', 'pan_tapa'],
    'tres salsas': ['pan_base', 'carne', 'catsup', 'mostaza', 'mayonesa', 'pan_tapa'],
    'verdura repetida': ['pan_base', 'carne', 'tomate', 'tomate', 'pan_tapa'],
  };
  for (const [name, stack] of Object.entries(invalid)) {
    it(`rechaza: ${name}`, () => assert.notDeepEqual(validateRecipe(stack, MAX), []));
  }

  it('rechaza recetas más altas que el límite', () => {
    assert.notDeepEqual(validateRecipe(CATALOG.cuadruple.stack, stackHeight(CATALOG.cuadruple.stack) - 1), []);
  });
});

describe('generateRecipe', () => {
  for (const tier of [1, 2, 3, 4, 5]) {
    it(`genera 500 recetas válidas en el nivel ${tier}`, () => {
      const rng = seeded(tier);
      for (let i = 0; i < 500; i++) {
        const { stack } = generateRecipe(tier, MAX, rng);
        assert.deepEqual(validateRecipe(stack, MAX), [], stack.join(' '));
      }
    });
  }

  it('respeta el número de carnes de los niveles 1 a 3', () => {
    for (const [tier, carnes] of [[1, 1], [2, 2], [3, 3]]) {
      const rng = seeded(100 + tier);
      for (let i = 0; i < 100; i++) assert.equal(count(generateRecipe(tier, MAX, rng).stack, 'carne'), carnes);
    }
  });

  it('el nivel 4 produce torres de cuatro carnes y recetas de tres panes', () => {
    const rng = seeded(7);
    const recipes = Array.from({ length: 200 }, () => generateRecipe(4, MAX, rng).stack);
    assert.ok(recipes.some((s) => count(s, 'carne') === 4 && !s.includes('pan_medio')));
    assert.ok(recipes.some((s) => s.includes('pan_medio')));
  });
});
