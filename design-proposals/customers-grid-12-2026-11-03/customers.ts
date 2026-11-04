import { clienteNuevoLia } from './01-lia.ts';
import { clienteNuevoBruno } from './02-bruno.ts';
import { clienteNuevoZoe } from './03-zoe.ts';
import { clienteNuevoCiro } from './04-ciro.ts';
import { clienteNuevoMika } from './05-mika.ts';
import { clienteNuevoAlma } from './06-alma.ts';
import { clienteNuevoRafa } from './07-rafa.ts';
import { clienteNuevoDante } from './08-dante.ts';
import { clienteNuevoVega } from './09-vega.ts';
import { clienteNuevoInes } from './10-ines.ts';
import { clienteNuevoGael } from './11-gael.ts';
import { clienteNuevoSasha } from './12-sasha.ts';

export const NEW_CUSTOMER_SPRITES = [clienteNuevoLia, clienteNuevoBruno, clienteNuevoZoe, clienteNuevoCiro, clienteNuevoMika, clienteNuevoAlma, clienteNuevoRafa, clienteNuevoDante, clienteNuevoVega, clienteNuevoInes, clienteNuevoGael, clienteNuevoSasha] as const;
export const NEW_CUSTOMER_PROFILES = [
  {
    "id": "cliente_nuevo_lia",
    "name": "Lía",
    "style": "Skater"
  },
  {
    "id": "cliente_nuevo_bruno",
    "name": "Bruno",
    "style": "Indie"
  },
  {
    "id": "cliente_nuevo_zoe",
    "name": "Zoe",
    "style": "Gótica"
  },
  {
    "id": "cliente_nuevo_ciro",
    "name": "Ciro",
    "style": "Fútbol"
  },
  {
    "id": "cliente_nuevo_mika",
    "name": "Mika",
    "style": "Techwear"
  },
  {
    "id": "cliente_nuevo_alma",
    "name": "Alma",
    "style": "Arte"
  },
  {
    "id": "cliente_nuevo_rafa",
    "name": "Rafa",
    "style": "Rockabilly"
  },
  {
    "id": "cliente_nuevo_dante",
    "name": "Dante",
    "style": "Metal"
  },
  {
    "id": "cliente_nuevo_vega",
    "name": "Vega",
    "style": "Rave"
  },
  {
    "id": "cliente_nuevo_ines",
    "name": "Inés",
    "style": "Kawaii"
  },
  {
    "id": "cliente_nuevo_gael",
    "name": "Gael",
    "style": "Surf"
  },
  {
    "id": "cliente_nuevo_sasha",
    "name": "Sasha",
    "style": "Streetwear"
  }
] as const;
