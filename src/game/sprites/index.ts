import type { SpriteDef, TilemapDef } from './define.ts';
import { carne, panBase, queso } from './ingredients.ts';
import { bote } from './utensils.ts';

// Registro de todas las definiciones, por id.

const list: SpriteDef[] = [panBase, carne, queso, bote];

export const SPRITES: Record<string, SpriteDef> = Object.fromEntries(list.map((def) => [def.id, def]));
export const TILEMAPS: Record<string, TilemapDef> = {};
