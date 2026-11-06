import { tocino, tocinoPlancha, charolaTocino } from './bacon.ts';
import type { SpriteDef, TilemapDef } from './define.ts';
import { carne, cebolla, lechuga, panBase, panMedio, panTapa, queso, salsa, tomate } from './ingredients.ts';
import { cliente } from './people.ts';
import { azulejo, madera } from './tiles.ts';
import { comedor, comedorVertical, barraRoja, barraRojaVertical } from './environment.ts';
import { corazon, flecha, globoCliente, globoClienteVertical, humo, pacienciaUrgente, casillaComanda, casillaComandaCompacta } from './ui.ts';
import {
  bandejaCebolla, bandejaLechuga, bandejaPan, bandejaQueso, bandejaTomate,
  basura, bote, charola, plancha, planchaVertical, plato,
} from './utensils.ts';

// Registro de todas las definiciones, por id.

const list: SpriteDef[] = [
  tocino, tocinoPlancha, charolaTocino,
  panBase, panMedio, panTapa, carne, queso, lechuga, tomate, cebolla, salsa,
  bote, plato, charola, basura, plancha, planchaVertical,
  bandejaPan, bandejaQueso, bandejaLechuga, bandejaTomate, bandejaCebolla,
  cliente,
  humo, flecha, corazon, globoCliente, globoClienteVertical, pacienciaUrgente, casillaComanda, casillaComandaCompacta,
  azulejo, madera, comedor, comedorVertical, barraRoja, barraRojaVertical,
];

export const SPRITES: Record<string, SpriteDef> = Object.fromEntries(list.map((def) => [def.id, def]));
export const TILEMAPS: Record<string, TilemapDef> = {};
