import type { SpriteDef, TilemapDef } from './define.ts';
import { carne, cebolla, lechuga, panBase, panMedio, panTapa, queso, salsa, tomate } from './ingredients.ts';
import { cliente, clienta } from './people.ts';
import { azulejo, madera } from './tiles.ts';
import { corazon, flecha, humo } from './ui.ts';
import {
  bandejaCebolla, bandejaLechuga, bandejaPan, bandejaQueso, bandejaTomate,
  basura, bote, charola, plancha, planchaVertical, plato,
} from './utensils.ts';

// Registro de todas las definiciones, por id.

const list: SpriteDef[] = [
  panBase, panMedio, panTapa, carne, queso, lechuga, tomate, cebolla, salsa,
  bote, plato, charola, basura, plancha, planchaVertical,
  bandejaPan, bandejaQueso, bandejaLechuga, bandejaTomate, bandejaCebolla,
  cliente, clienta,
  humo, flecha, corazon,
  azulejo, madera,
];

export const SPRITES: Record<string, SpriteDef> = Object.fromEntries(list.map((def) => [def.id, def]));
export const TILEMAPS: Record<string, TilemapDef> = {};
