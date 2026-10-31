import { buildAtlas, type AtlasEntry } from './atlas.ts';
import { rasterize, resolveSprite, rows, type SpriteDef, type TilemapDef } from './define.ts';

// «Horneado»: convierte cada definición en una imagen una sola vez y la guarda en caché.
// En el DOM, cada sprite es un solo elemento con esa imagen (nunca un elemento por pixel).

export interface BakedSprite {
  url: string;
  width: number; // de un cuadro
  height: number;
  frames: number;
}

const cache = new Map<string, BakedSprite>();

function toUrl(data: Uint8ClampedArray, width: number, height: number): string {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  canvas.getContext('2d')!.putImageData(new ImageData(new Uint8ClampedArray(data), width, height), 0, 0);
  return canvas.toDataURL('image/png');
}

export function bakeSprite(def: SpriteDef, variant?: string): BakedSprite {
  const key = `${def.id}:${variant ?? ''}`;
  const cached = cache.get(key);
  if (cached) return cached;
  const resolved = resolveSprite(def, variant);
  const frames = resolved.frames.length;
  const baked = {
    url: toUrl(rasterize(resolved), resolved.width * frames, resolved.height),
    width: resolved.width,
    height: resolved.height,
    frames,
  };
  cache.set(key, baked);
  return baked;
}

/** Hornea un fondo de tiles completo como una sola imagen. */
export function bakeTilemap(def: TilemapDef, sprites: Record<string, SpriteDef>): BakedSprite {
  const key = `mapa:${def.id}`;
  const cached = cache.get(key);
  if (cached) return cached;
  const lines = rows(def.map);
  const size = def.tileSize;
  const width = (lines[0]?.length ?? 0) * size;
  const height = lines.length * size;
  const data = new Uint8ClampedArray(width * height * 4);
  const tiles = new Map(Object.entries(def.tiles).map(([letter, id]) => [letter, rasterize(resolveSprite(sprites[id]))]));
  lines.forEach((row, ty) =>
    [...row].forEach((letter, tx) => {
      const tile = tiles.get(letter)!;
      for (let y = 0; y < size; y++) {
        const from = y * size * 4;
        data.set(tile.subarray(from, from + size * 4), ((ty * size + y) * width + tx * size) * 4);
      }
    }),
  );
  const baked = { url: toUrl(data, width, height), width, height, frames: 1 };
  cache.set(key, baked);
  return baked;
}

/** Vacía la caché (la página de revisión la usa al recargar definiciones). */
export function clearBakeCache() {
  cache.clear();
}

export interface BakedAtlas {
  url: string;
  width: number;
  height: number;
  entries: Record<string, AtlasEntry>;
}

/** Hornea todos los sprites y variantes en una sola imagen. */
export function bakeAtlas(sprites: readonly SpriteDef[]): BakedAtlas {
  const atlas = buildAtlas(sprites);
  return { url: toUrl(atlas.data, atlas.width, atlas.height), width: atlas.width, height: atlas.height, entries: atlas.entries };
}

/** Estilos CSS para mostrar un cuadro de un sprite del atlas a cierta escala entera. */
export function atlasStyle(atlas: BakedAtlas, key: string, scale: number, frame = 0) {
  const entry = atlas.entries[key];
  if (!entry) throw new Error(`El atlas no tiene «${key}»`);
  return {
    width: `${entry.width * scale}px`,
    height: `${entry.height * scale}px`,
    backgroundImage: `url(${atlas.url})`,
    backgroundSize: `${atlas.width * scale}px ${atlas.height * scale}px`,
    backgroundPosition: `${-(entry.x + (frame % entry.frames) * entry.width) * scale}px ${-entry.y * scale}px`,
  };
}
