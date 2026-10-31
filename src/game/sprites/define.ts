import { rgb, type ColorName } from './palette.ts';

// Formato de sprites como texto (ver working-plan/02-minijuego/ASSETS.md).
// Cada letra de la matriz es un color de la paleta; «.» es transparente.

export const TRANSPARENT = '.';

export type Colors = Record<string, ColorName>;

export interface SpriteVariant {
  colors?: Partial<Colors>;
  /** Materiales de esta variante (si cambian respecto al sprite base). */
  materials?: readonly string[];
  /** Filas que se reemplazan (por índice, en todos los cuadros). */
  patch?: Record<number, string>;
  pixels?: string;
  frames?: readonly string[];
}

export interface SpriteDef {
  id: string;
  /** [ancho, alto] en pixeles; sirve de comprobación de la matriz. */
  size: readonly [number, number];
  colors: Colors;
  /** Materiales (rampas de palette.ts) que puede usar; la revisión de estilo avisa si se sale. */
  materials?: readonly string[];
  pixels?: string;
  frames?: readonly string[];
  /** Se escribe solo la mitad izquierda y se completa en espejo. */
  mirror?: 'x';
  variants?: Record<string, SpriteVariant>;
}

export interface TilemapDef {
  id: string;
  tileSize: number;
  /** Letra del mapa → id del sprite del tile. */
  tiles: Record<string, string>;
  map: string;
}

export const defineSprite = <T extends SpriteDef>(def: T): T => def;
export const defineTilemap = <T extends TilemapDef>(def: T): T => def;

/** Separa el texto en filas, sin sangría ni líneas vacías al principio o al final. */
export function rows(text: string): string[] {
  const lines = text.split('\n').map((line) => line.trim());
  while (lines.length && !lines[0]) lines.shift();
  while (lines.length && !lines[lines.length - 1]) lines.pop();
  return lines;
}

/** Ancho de las filas escritas a mano (la mitad, redondeada hacia arriba, si va en espejo). */
export function sourceWidth(def: SpriteDef): number {
  return def.mirror === 'x' ? Math.ceil(def.size[0] / 2) : def.size[0];
}

function mirrorRow(half: string, width: number): string {
  const right = [...half].reverse().join('');
  return width % 2 ? half + right.slice(1) : half + right;
}

export interface ResolvedSprite {
  width: number;
  height: number;
  colors: Colors;
  /** Cuadros como filas de ancho completo. */
  frames: string[][];
}

/** Aplica variante, parches y espejo: deja los cuadros listos para dibujar. */
export function resolveSprite(def: SpriteDef, variant?: string): ResolvedSprite {
  const v = variant ? def.variants?.[variant] : undefined;
  if (variant && !v) throw new Error(`El sprite «${def.id}» no tiene la variante «${variant}»`);
  const colors = { ...def.colors, ...v?.colors } as Colors;
  const sources = v?.frames ?? (v?.pixels !== undefined ? [v.pixels] : undefined) ??
    def.frames ?? (def.pixels !== undefined ? [def.pixels] : []);
  const frames = sources.map((source) => {
    let lines = rows(source);
    if (v?.patch) lines = lines.map((row, y) => v.patch![y]?.trim() ?? row);
    return def.mirror === 'x' ? lines.map((row) => mirrorRow(row, def.size[0])) : lines;
  });
  return { width: def.size[0], height: def.size[1], colors, frames };
}

/** Pixeles RGBA de todos los cuadros, uno junto a otro en una tira horizontal. */
export function rasterize(sprite: ResolvedSprite): Uint8ClampedArray {
  const { width, height, frames, colors } = sprite;
  const stripWidth = width * frames.length;
  const data = new Uint8ClampedArray(stripWidth * height * 4);
  frames.forEach((frame, f) => {
    frame.forEach((row, y) => {
      for (let x = 0; x < width; x++) {
        const letter = row[x];
        if (letter === undefined || letter === TRANSPARENT) continue;
        const name = colors[letter];
        if (!name) throw new Error(`Letra «${letter}» sin color`);
        const [r, g, b] = rgb(name);
        const i = (y * stripWidth + f * width + x) * 4;
        data.set([r, g, b, 255], i);
      }
    });
  });
  return data;
}
