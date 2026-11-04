// Run from repository root: node design-proposals/kitchen-2026-10-31/export.mjs
import { SPRITES } from '../../src/game/sprites/index.ts';
import { resolveSprite } from '../../src/game/sprites/define.ts';
import { PALETTE } from '../../src/game/sprites/palette.ts';
import { writeFileSync } from 'node:fs';
const sprites = {};
for (const def of Object.values(SPRITES)) {
  for (const variant of [undefined, ...Object.keys(def.variants ?? {})]) {
    sprites[def.id + (variant ? ':' + variant : '')] = resolveSprite(def, variant);
  }
}
writeFileSync(new URL('./source-sprites.json', import.meta.url), JSON.stringify({ palette: PALETTE, sprites }));
