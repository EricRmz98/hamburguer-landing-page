# Escribe src/game/sprites/people.ts con los clientes generados por people_gen.py.
# Uso (desde la raíz del proyecto): python3 scripts/sprites/write_people.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from people_gen import frames

def block(rows, indent): return '\n'.join(indent + r for r in rows)
def obj(d): return '{ ' + ', '.join(f"{k}: '{v}'" for k, v in d.items()) + ' }'
def mats(m): return '[' + ', '.join(f"'{x}'" for x in m) + ']'

def sprite(var, sid, female, looks):
    base_mats, base_cols = next(iter(looks.values()))
    fr = '\n'.join("    `\n" + block(f, '      ') + "\n    `," for f in frames(female))
    variants = '\n'.join(f"    {name}: {{ materials: {mats(m)}, colors: {obj(c)} }}," for name, (m, c) in looks.items())
    return f"""export const {var} = defineSprite({{
  id: '{sid}',
  size: [48, 80],
  materials: {mats(base_mats)},
  colors: {obj({'o': 'negro', **base_cols})},
  frames: [
{fr}
  ],
  variants: {{
{variants}
  }},
}});"""

HOMBRE = {
  'azul': (['contorno','piel','pelo-oscuro','ropa-azul'], {'p':'canela','q':'piel','r':'piel-clara','h':'cafe-oscuro','i':'negro','j':'cafe','c':'azul','d':'azul-oscuro','e':'cian'}),
  'rojo': (['contorno','piel','pelo-claro','ropa-roja'], {'p':'piel','q':'piel-clara','r':'crema','h':'tostado','i':'oxido','j':'ambar','c':'rojo','d':'rojo-oscuro','e':'rosa'}),
  'verde': (['contorno','piel','pelo-oscuro','ropa-verde'], {'p':'cafe','q':'canela','r':'piel','h':'negro','i':'negro','j':'cafe-oscuro','c':'verde','d':'verde-oscuro','e':'verde-claro'}),
  'morado': (['contorno','piel','pelo-claro','ropa-morada'], {'p':'canela','q':'piel','r':'piel-clara','h':'oxido','i':'cafe','j':'tostado','c':'magenta','d':'ciruela','e':'rosa'}),
}
MUJER = {
  'roja': (['contorno','piel','pelo-oscuro','ropa-roja','acento'], {'p':'piel','q':'piel-clara','r':'crema','h':'cafe-oscuro','i':'negro','j':'cafe','c':'rojo','d':'rojo-oscuro','e':'rosa','g':'ambar'}),
  'amarilla': (['contorno','piel','pelo-oscuro','acento','avisos'], {'p':'cafe','q':'canela','r':'piel','h':'negro','i':'negro','j':'cafe-oscuro','c':'ambar','d':'naranja','e':'amarillo','g':'cian'}),
  'verde': (['contorno','piel','pelo-claro','ropa-verde','acento'], {'p':'canela','q':'piel','r':'piel-clara','h':'ambar','i':'tostado','j':'amarillo','c':'verde','d':'verde-oscuro','e':'verde-claro','g':'naranja'}),
  'morada': (['contorno','piel','pelo-claro','ropa-morada','acento'], {'p':'piel','q':'piel-clara','r':'crema','h':'oxido','i':'cafe','j':'tostado','c':'magenta','d':'ciruela','e':'rosa','g':'amarillo'}),
}
ORDER = [('cliente','azul'),('clienta','roja'),('cliente','verde'),('clienta','amarilla'),('cliente','rojo'),('clienta','verde'),('cliente','morado'),('clienta','morada')]

out = f"""import {{ atlasKey }} from './atlas.ts';
import {{ defineSprite }} from './define.ts';

// Clientes de la cintura para arriba, detrás de la barra (48 × 80): la barra tapa la cintura y la
// cabeza queda por encima de la hamburguesa. Generados con scripts/sprites/people_gen.py (formas
// trazadas y sombreadas con luz desde la izquierda); se editan como cualquier otro sprite.
// Cuadros = expresiones: 0 esperando, 1 feliz, 2 enojado. Variantes = looks por paleta.
// Letras: o = contorno y rasgos; p/q/r = piel (sombra, base, luz); h/i/j = pelo (base, sombra, luz);
// c/d/e = ropa (base, sombra, luz); g = aretes.

{sprite('cliente', 'cliente', False, HOMBRE)}

{sprite('clienta', 'clienta', True, MUJER)}

/** Todos los aspectos posibles, alternando hombres y mujeres. */
export const CUSTOMERS = [
{chr(10).join(f"  atlasKey('{sid}', '{look}')," for sid, look in ORDER)}
];
"""
open('src/game/sprites/people.ts', 'w', encoding='utf-8').write(out)
print('ok')
