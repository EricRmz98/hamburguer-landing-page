import { rasterize, resolveSprite, type SpriteDef } from './define.ts';

// Atlas: todos los sprites y sus variantes en una sola imagen, acomodados en filas.
// Es lógica pura (sin DOM) para poder probarla; bake.ts la convierte en imagen.

export interface AtlasEntry {
  x: number;
  y: number;
  width: number; // de un cuadro
  height: number;
  frames: number; // los cuadros van uno junto a otro a partir de x
}

export interface Atlas {
  width: number;
  height: number;
  data: Uint8ClampedArray;
  entries: Record<string, AtlasEntry>;
}

export const atlasKey = (id: string, variant?: string) => (variant ? `${id}:${variant}` : id);

export function buildAtlas(sprites: readonly SpriteDef[], maxWidth = 256, gap = 1): Atlas {
  const items = sprites.flatMap((def) =>
    [undefined, ...Object.keys(def.variants ?? {})].map((variant) => {
      const resolved = resolveSprite(def, variant);
      const used = [...new Set(resolved.frames.flat().join(''))].sort();
      // Variantes que no cambian nada (p. ej. «perfecta» o «catsup») comparten el mismo lugar.
      const signature = JSON.stringify([resolved.frames, used.map((letter) => resolved.colors[letter] ?? '')]);
      return { key: atlasKey(def.id, variant), resolved, signature, w: resolved.width * resolved.frames.length, h: resolved.height, x: 0, y: 0 };
    }),
  );

  const placed = new Map<string, (typeof items)[number]>();
  const unique = items.filter((item) => !placed.has(item.signature) && placed.set(item.signature, item));
  unique.sort((a, b) => b.h - a.h || b.w - a.w);

  let x = 0;
  let y = 0;
  let rowHeight = 0;
  let width = 0;
  for (const item of unique) {
    if (x > 0 && x + item.w > maxWidth) {
      x = 0;
      y += rowHeight + gap;
      rowHeight = 0;
    }
    item.x = x;
    item.y = y;
    x += item.w + gap;
    rowHeight = Math.max(rowHeight, item.h);
    width = Math.max(width, item.x + item.w);
  }
  const height = y + rowHeight;

  const data = new Uint8ClampedArray(width * height * 4);
  for (const item of unique) {
    const pixels = rasterize(item.resolved);
    for (let row = 0; row < item.h; row++) {
      data.set(pixels.subarray(row * item.w * 4, (row + 1) * item.w * 4), ((item.y + row) * width + item.x) * 4);
    }
  }

  const entries: Record<string, AtlasEntry> = {};
  for (const item of items) {
    const at = placed.get(item.signature)!;
    entries[item.key] = { x: at.x, y: at.y, width: item.resolved.width, height: item.resolved.height, frames: item.resolved.frames.length };
  }
  return { width, height, data, entries };
}
