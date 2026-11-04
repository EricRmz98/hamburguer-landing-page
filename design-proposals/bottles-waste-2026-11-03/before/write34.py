import json, sys
d = json.load(open(sys.argv[1]))
LINT_PLANO = set()  # sprites planos vistos desde arriba que no pasan la revisión de luz
def obj(c): return '{ ' + ', '.join(f"{k}: '{v}'" for k, v in c.items()) + ' }'
def mats(m): return '[' + ', '.join(f"'{x}'" for x in m) + ']'
def sprite(var, sid, variants=None, extra_colors=None):
    g = d[sid]; colors = dict(g['colors'])
    for k, v in (extra_colors or {}).items():
        if any(k in r for f in g['frames'] for r in f): colors[k] = v
    lines = [f"export const {var} = defineSprite({{", f"  id: '{sid}',", f"  size: [{g['size'][0]}, {g['size'][1]}],"] + (
        ["  lint: { light: false, reason: 'Superficie plana vista desde arriba: casi todo es cara superior.' },"] if sid in LINT_PLANO else []) + [
             f"  materials: {mats(g['materials'])},", f"  colors: {obj(colors)},"]
    if len(g['frames']) == 1:
        lines += ["  pixels: `", '\n'.join('    ' + r for r in g['frames'][0]), "  `,"]
    else:
        lines.append("  frames: [")
        for f in g['frames']: lines += ["    `", '\n'.join('      ' + r for r in f), "    `,"]
        lines.append("  ],")
    if variants:
        lines.append("  variants: {")
        for name, (vm, vc) in variants.items():
            parts = []
            if vm: parts.append(f"materials: {mats(vm)}")
            if vc: parts.append(f"colors: {obj({k: v for k, v in vc.items() if k in colors})}")
            lines.append(f"    {name}: {{ {', '.join(parts)} }},")
        lines.append("  },")
    lines.append("});")
    return '\n'.join(lines)
HEADER = """import {{ defineSprite }} from './define.ts';

// {what} en vista frontal elevada 3/4 (cámara a 32° de altura, girada 12°).
// Se generaron modelando cada objeto con vóxeles y proyectándolo: cara de arriba = luz, frente e
// izquierda = base, derecha y contacto = sombra, contorno selectivo y textura por material.
// Son texto como cualquier otro sprite: se pueden retocar a mano. Las anclas (base de cada objeto
// dentro del sprite) están en anchors.ts.
"""
ing = HEADER.format(what='Ingredientes') + '\n' + '\n\n'.join([
    sprite('panBase', 'pan_base'), sprite('panMedio', 'pan_medio'), sprite('panTapa', 'pan_tapa'),
    sprite('carne', 'carne', {
        'perfecta': (None, None),
        'cruda': (['carne-cruda'], {'k': 'rojo-oscuro', 'm': 'rosa-viejo', 'n': 'rosa', 'p': 'piel-clara', 'h': 'blanco'}),
        'cocinandose': (['carne-cocinandose'], {'k': 'cafe-oscuro', 'm': 'cafe', 'n': 'canela', 'p': 'piel', 'h': 'piel-clara'}),
        'quemada': (['carne-quemada'], {'k': 'negro', 'm': 'negro', 'n': 'noche', 'p': 'pizarra', 'h': 'gris-azul'}),
    }, extra_colors={'h': 'piel'}),
    sprite('queso', 'queso'), sprite('lechuga', 'lechuga'), sprite('tomate', 'tomate'), sprite('cebolla', 'cebolla'),
    sprite('salsa', 'salsa', {
        'catsup': (None, None),
        'mostaza': (['mostaza'], {'I': 'oxido', 'J': 'ambar', 'K': 'amarillo', 'L': 'vainilla', 'O': 'crema'}),
        'mayonesa': (['mayonesa'], {'I': 'plata', 'J': 'piel-clara', 'K': 'crema', 'L': 'blanco', 'O': 'blanco'}),
    }),
]) + '\n'
ute = HEADER.format(what='Utensilios') + '\n' + '\n\n'.join([
    sprite('bote', 'bote', {
        'catsup': (None, None),
        'mostaza': (['mostaza', 'etiqueta', 'metal'], {'I': 'oxido', 'J': 'ambar', 'K': 'amarillo', 'L': 'vainilla', 'O': 'crema'}),
        'mayonesa': (['mayonesa', 'etiqueta', 'metal'], {'I': 'plata', 'J': 'piel-clara', 'K': 'crema', 'L': 'blanco', 'O': 'blanco'}),
    }),
    sprite('plato', 'plato'), sprite('charola', 'charola'),
    sprite('plancha', 'plancha'), sprite('planchaVertical', 'plancha_v'),
    sprite('bandejaPan', 'bandeja_pan'), sprite('bandejaQueso', 'bandeja_queso'), sprite('bandejaLechuga', 'bandeja_lechuga'),
    sprite('bandejaTomate', 'bandeja_tomate'), sprite('bandejaCebolla', 'bandeja_cebolla'),
    sprite('basura', 'basura'),  # la alerta es solo un contorno rojo por CSS: el bote no cambia de color
]) + '\n'
anchors = """// Anclas: posición (x, y) de la base de cada objeto dentro de su sprite, en pixeles.
// La pila del plato coloca cada ingrediente por su ancla; las generó el mismo script que los sprites.

export const ANCHORS: Record<string, readonly [number, number]> = {
""" + '\n'.join(f"  {k}: [{v['anchor'][0]}, {v['anchor'][1]}]," for k, v in d.items()) + "\n};\n"
open('src/game/sprites/ingredients.ts', 'w', encoding='utf-8').write(ing)
open('src/game/sprites/utensils.ts', 'w', encoding='utf-8').write(ute)
open('src/game/sprites/anchors.ts', 'w', encoding='utf-8').write(anchors)
print('ok')
