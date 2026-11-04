import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { describe, it } from 'node:test';
import { atlasKey, buildAtlas } from '../src/game/sprites/atlas.ts';
import { imageToSprite, nearestColor } from '../src/game/sprites/convert.ts';
import { defineSprite, defineTilemap, rasterize, resolveSprite, rows } from '../src/game/sprites/define.ts';
import { SPRITES } from '../src/game/sprites/index.ts';
import { LAYOUTS } from '../src/game/layouts/index.ts';
import { PALETTE, rgb, type ColorName } from '../src/game/sprites/palette.ts';
import { lintSprite, validateSprite, validateTilemap } from '../src/game/sprites/validate.ts';

const pixel = (data: Uint8ClampedArray, stripWidth: number, x: number, y: number) =>
  [...data.subarray((y * stripWidth + x) * 4, (y * stripWidth + x) * 4 + 4)];

const tiny = defineSprite({
  id: 'prueba',
  size: [3, 2],
  colors: { a: 'rojo', b: 'azul' },
  pixels: `
    ab.
    .ba
  `,
  variants: {
    fria: { colors: { a: 'cian' } },
    parche: { patch: { 1: 'aaa' } },
  },
});

describe('Paleta', () => {
  it('contiene los 64 colores originales de Endesga 64, sin sustituciones ni colores añadidos', () => {
    const values = Object.values(PALETTE);
    const official = JSON.parse(readFileSync(new URL('../scripts/sprites/endesga-64.json', import.meta.url), 'utf8'));
    assert.equal(values.length, 64);
    assert.equal(new Set(values).size, 64);
    assert.deepEqual(values, official.colors.map((hex: string) => `#${hex}`));
  });
});

describe('Sprites registrados', () => {
  for (const [id, def] of Object.entries(SPRITES)) {
    it(`«${id}» es válido`, () => assert.deepEqual(validateSprite(def), []));
    it(`«${id}» cumple la guía de estilo`, () => assert.deepEqual(lintSprite(def), []));
    it(`«${id}» se rasteriza en todas sus variantes`, () => {
      for (const variant of [undefined, ...Object.keys(def.variants ?? {})]) {
        const resolved = resolveSprite(def, variant);
        const data = rasterize(resolved);
        assert.equal(data.length, resolved.width * resolved.frames.length * resolved.height * 4);
      }
    });
  }
});

describe('Formato', () => {
  it('ignora la sangría y rasteriza los colores de la paleta', () => {
    const data = rasterize(resolveSprite(tiny));
    assert.deepEqual(pixel(data, 3, 0, 0), [...rgb('rojo'), 255]);
    assert.deepEqual(pixel(data, 3, 1, 0), [...rgb('azul'), 255]);
    assert.deepEqual(pixel(data, 3, 2, 0), [0, 0, 0, 0]);
  });

  it('las variantes cambian colores o filas', () => {
    assert.deepEqual(pixel(rasterize(resolveSprite(tiny, 'fria')), 3, 0, 0), [...rgb('cian'), 255]);
    assert.deepEqual(resolveSprite(tiny, 'parche').frames[0], ['ab.', 'aaa']);
  });

  it('completa en espejo los sprites simétricos (ancho par e impar)', () => {
    const par = defineSprite({ id: 'par', size: [4, 1], colors: { a: 'rojo', b: 'azul' }, mirror: 'x', pixels: 'ab' });
    const impar = defineSprite({ id: 'impar', size: [5, 1], colors: { a: 'rojo', b: 'azul' }, mirror: 'x', pixels: 'aab' });
    assert.deepEqual(validateSprite(par), []);
    assert.deepEqual(resolveSprite(par).frames[0], ['abba']);
    assert.deepEqual(resolveSprite(impar).frames[0], ['aabaa']);
  });

  it('los cuadros se colocan en una tira horizontal', () => {
    const anim = defineSprite({ id: 'anim', size: [1, 1], colors: { a: 'rojo', b: 'azul' }, frames: ['a', 'b'] });
    const data = rasterize(resolveSprite(anim));
    assert.deepEqual(pixel(data, 2, 1, 0), [...rgb('azul'), 255]);
  });
});

describe('Validación', () => {
  const broken = (patch: object) => validateSprite({ ...tiny, ...patch } as typeof tiny);

  it('detecta filas de otro ancho, filas de más y letras sin color', () => {
    assert.ok(broken({ pixels: 'ab\n.ba' }).some((e) => e.includes('mide 2')));
    assert.ok(broken({ pixels: 'ab.\n.ba\nabb' }).some((e) => e.includes('3 filas')));
    assert.ok(broken({ pixels: 'ax.\n.ba' }).some((e) => e.includes('«x»')));
  });

  it('detecta colores que no son de la paleta', () => {
    assert.ok(broken({ colors: { a: 'morado', b: 'azul' } }).some((e) => e.includes('«morado»')));
  });

  it('detecta parches fuera del sprite', () => {
    assert.ok(broken({ variants: { mal: { patch: { 5: 'aaa' } } } }).some((e) => e.includes('fuera')));
  });

  it('exige pixels o frames', () => {
    assert.ok(broken({ pixels: undefined }).some((e) => e.includes('pixels')));
  });

  it('rechaza materiales que no existen', () => {
    assert.ok(broken({ materials: ['plastico'] }).some((e) => e.includes('«plastico»')));
  });

  it('valida los mapas de tiles', () => {
    const tile = defineSprite({ id: 'tile', size: [2, 2], colors: { a: 'rojo' }, pixels: 'aa\naa' });
    const ok = defineTilemap({ id: 'mapa', tileSize: 2, tiles: { t: 'tile' }, map: 'tt\ntt' });
    assert.deepEqual(validateTilemap(ok, { tile }), []);
    assert.ok(validateTilemap({ ...ok, map: 'tx\ntt' }, { tile }).some((e) => e.includes('«x»')));
    assert.ok(validateTilemap({ ...ok, tileSize: 4 }, { tile }).some((e) => e.includes('se esperaba 4')));
  });
});

describe('Revisión de estilo', () => {
  const flip = (source: string) => rows(source).map((row) => [...row].reverse().join('')).join('\n');

  it('avisa si la luz viene del lado contrario', () => {
    const lit = defineSprite({ id: 'luz', size: [8, 3], colors: { l: 'crema', m: 'pizarra', s: 'negro' }, pixels: 'lllmmsss\nlllmmsss\nlllmmsss' });
    assert.deepEqual(lintSprite(lit), []);
    assert.ok(lintSprite({ ...lit, pixels: flip(lit.pixels) }).some((w) => w.includes('derecha')));
  });

  it('avisa si se usan colores fuera de los materiales', () => {
    const pan = SPRITES.pan_base;
    assert.ok(lintSprite({ ...pan, colors: { ...pan.colors, l: 'verde' } }).some((w) => w.includes('«verde»')));
  });

  it('avisa de letras declaradas que no se usan', () => {
    assert.ok(lintSprite({ ...tiny, colors: { ...tiny.colors, z: 'negro' } }).some((w) => w.includes('«z»')));
  });
});

describe('Atlas', () => {
  const defs = Object.values(SPRITES);
  const atlas = buildAtlas(defs);

  it('incluye cada sprite y cada variante', () => {
    for (const def of defs) {
      assert.ok(atlas.entries[atlasKey(def.id)], def.id);
      for (const variant of Object.keys(def.variants ?? {})) assert.ok(atlas.entries[atlasKey(def.id, variant)], `${def.id}:${variant}`);
    }
  });

  it('copia los pixeles sin mezclar sprites', () => {
    for (const def of defs) {
      const entry = atlas.entries[def.id];
      const own = rasterize(resolveSprite(def));
      const stripWidth = entry.width * entry.frames;
      for (let y = 0; y < entry.height; y++) {
        const fromAtlas = atlas.data.subarray(((entry.y + y) * atlas.width + entry.x) * 4, ((entry.y + y) * atlas.width + entry.x + stripWidth) * 4);
        assert.deepEqual([...fromAtlas], [...own.subarray(y * stripWidth * 4, (y + 1) * stripWidth * 4)], `${def.id}, fila ${y}`);
      }
    }
  });

  it('las variantes idénticas comparten lugar', () => {
    assert.deepEqual(atlas.entries['carne:perfecta'], atlas.entries.carne);
    assert.deepEqual(atlas.entries['bote:catsup'], atlas.entries.bote);
  });
});

describe('Importar desde imagen', () => {
  it('importa los 64 colores de Endesga sin perder ninguno ni exceder el alfabeto de celdas', () => {
    const colors = Object.keys(PALETTE) as ColorName[];
    const raw = new Uint8ClampedArray(colors.flatMap(name => [...rgb(name), 255]));
    const imported = imageToSprite(raw, 64, 1, { id: 'paleta_completa' });
    const def = defineSprite({ id: 'paleta_completa', size: [64, 1], colors: imported.colors, pixels: imported.frames[0].join('\n') });
    assert.equal(imported.adjusted, 0);
    assert.equal(Object.keys(imported.colors).length, 64);
    assert.deepEqual(validateSprite(def), []);
    assert.deepEqual(rasterize(resolveSprite(def)), raw);
  });
  it('el color más cercano de un tono fuera de la paleta', () => {
    assert.deepEqual(nearestColor(...rgb('rojo')), { name: 'rojo', exact: true });
    const [r, g, b] = rgb('rojo');
    assert.deepEqual(nearestColor(r + 3, g, b - 2), { name: 'rojo', exact: false });
  });

  it('ida y vuelta: exportar e importar el pan da la misma matriz y las mismas letras', () => {
    const pan = SPRITES.pan_base;
    const resolved = resolveSprite(pan);
    const letters = Object.fromEntries(Object.entries(pan.colors).map(([letter, name]) => [name, letter])) as Partial<Record<ColorName, string>>;
    const result = imageToSprite(rasterize(resolved), resolved.width, resolved.height, { id: 'pan_base', letters });
    assert.deepEqual(result.frames, resolved.frames);
    assert.deepEqual(result.colors, pan.colors);
    assert.equal(result.adjusted, 0);
    assert.match(result.text, /id: 'pan_base',/);
  });

  it('separa una tira de animación en cuadros', () => {
    const bote = SPRITES.bote;
    const resolved = resolveSprite(bote);
    const result = imageToSprite(rasterize(resolved), resolved.width * 2, resolved.height, { id: 'bote', frameWidth: resolved.width });
    assert.equal(result.frames.length, 2);
    assert.match(result.text, /frames: \[/);
  });

  it('sin letras preferidas, asigna de oscuro a claro (o = contorno primero)', () => {
    const data = new Uint8ClampedArray([...rgb('crema'), 255, ...rgb('negro'), 255]);
    const result = imageToSprite(data, 2, 1, { id: 'dos' });
    assert.deepEqual(result.colors, { o: 'negro', s: 'crema' });
    assert.deepEqual(result.frames, [['so']]);
  });

  it('lo importado se puede volver a validar', () => {
    const data = new Uint8ClampedArray([...rgb('rojo'), 255, 0, 0, 0, 0, ...rgb('rojo'), 200, ...rgb('azul'), 255]);
    const result = imageToSprite(data, 2, 2, { id: 'mini' });
    const def = defineSprite({ id: 'mini', size: [2, 2], colors: result.colors, pixels: result.frames[0].join('\n') });
    assert.deepEqual(validateSprite(def), []);
  });
});


describe('Entorno del comedor', () => {
  for (const [name, wall, counter] of [
    ['horizontal', 'comedor', 'barra_roja'],
    ['vertical', 'comedor_v', 'barra_roja_v'],
  ] as const) {
    it(`cubre exactamente el escenario ${name}, sin estirar ni dejar huecos`, () => {
      const layout = LAYOUTS[name];
      assert.deepEqual(SPRITES[wall].size, [layout.w, layout.counter[1]]);
      assert.deepEqual(SPRITES[counter].size, [layout.counter[2], layout.counter[3]]);
      assert.equal(SPRITES[wall].size[1] + SPRITES[counter].size[1], layout.h);
      for (const key of [wall, counter]) {
        const data = rasterize(resolveSprite(SPRITES[key]));
        for (let i = 3; i < data.length; i += 4) assert.equal(data[i], 255, `${key}: pixel transparente`);
      }
    });
  }
});
