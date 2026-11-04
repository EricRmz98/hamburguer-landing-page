"""Write the approved native cast. Run from any directory; no Pillow or proposal dependency."""
from pathlib import Path
import json
from customers_gen import load_cast
ROOT=Path(__file__).resolve().parents[2]
def generate():
    cast=load_cast(); people=cast['customers']; blocks=[]
    for p in people:
        pixels='\n'.join('      '+row for row in p['pixels'])
        blocks.append('  '+p['id']+': { colors: '+json.dumps(p['colors'])+', pixels: `\n'+pixels+'\n  ` },')
    profiles='\n'.join('  { key: atlasKey(\'cliente\', '+json.dumps(p['id'])+'), name: '+json.dumps(p['name'],ensure_ascii=False)+', style: '+json.dumps(p['style'],ensure_ascii=False)+', facing: '+json.dumps(p['facing'])+' },' for p in people)
    return """import { atlasKey } from './atlas.ts';
import { defineSprite, type SpriteVariant } from './define.ts';

// Approved native cast: 12 characters, 96 × 120; Endesga 64.
// One waiting portrait each. Source: scripts/sprites/customers-native.json.
// Proportions and alternating directions are baked into the cells, never scaled with CSS.
const appearances = {
"""+'\n'.join(blocks)+"""
} as const satisfies Record<string, SpriteVariant>;
export const cliente = defineSprite({
  id: 'cliente',
  size: [96, 120],
  colors: appearances.lia.colors,
  pixels: appearances.lia.pixels,
  lint: { light: false, reason: 'Personajes aprobados con varios materiales y orientaciones: la iluminación se revisa visualmente por pieza, no mediante el centroide global.' },
  variants: appearances,
});
export const CUSTOMER_PROFILES = [
"""+profiles+"""
] as const;
export const CUSTOMERS = CUSTOMER_PROFILES.map(person => person.key);
"""
if __name__=='__main__':
    (ROOT/'src/game/sprites/people.ts').write_text(generate(),encoding='utf-8')
    print('12 approved native customers written to people.ts.')
