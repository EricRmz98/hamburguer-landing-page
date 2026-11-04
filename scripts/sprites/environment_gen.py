"""Build native Endesga64 environment matrices from the editable pixel masters.
Masters are exact native PNGs: no resizing, filtering or palette remapping here.
Run: python3 scripts/sprites/environment_gen.py (requires Pillow).
"""
from pathlib import Path
from PIL import Image
import re,json
ROOT=Path(__file__).resolve().parents[2]
P={a or b:h for a,b,h in re.findall(r"(?:'([^']+)'|([\w-]+)):\s*'(#[0-9a-f]{6})'",(ROOT/'src/game/sprites/palette.ts').read_text())}
def write_sprite(name,id,im,materials,reason):
 reverse={tuple(bytes.fromhex(h[1:])):name for name,h in P.items()}
 letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#'
 used=sorted(set(im.getdata()));colors={letters[i]:reverse[rgb] for i,rgb in enumerate(used)}
 lookup={rgb:letters[i] for i,rgb in enumerate(used)}
 rows=[''.join(lookup[im.getpixel((x,y))] for x in range(im.width)) for y in range(im.height)]
 return f"export const {name} = defineSprite({{\n  id: '{id}',\n  size: [{im.width}, {im.height}],\n  materials: {json.dumps(materials)},\n  lint: {{ light: false, reason: {json.dumps(reason,ensure_ascii=False)} }},\n  colors: {json.dumps(colors,ensure_ascii=False)},\n  pixels: `\n"+'\n'.join('    '+row for row in rows)+"\n  `,\n});\n"

if __name__=='__main__':
 text="// Generated from scripts/sprites/environment-native/*.png; exact native cells.\nimport { defineSprite } from './define.ts';\n\n"
 reason='Escena con materiales y objetos a distintas profundidades: no corresponde comparar el centroide global de sus colores.'
 for name,id,size in [('comedor','comedor',(320,122)),('comedorVertical','comedor_v',(180,200)),('barraRoja','barra_roja',(320,90)),('barraRojaVertical','barra_roja_v',(180,100))]:
  im=Image.open(ROOT/'scripts/sprites/environment-native'/f'{id}.png').convert('RGB')
  assert im.size==size,(id,im.size)
  assert set(im.getdata()) <= {tuple(bytes.fromhex(h[1:])) for h in P.values()},f'{id}: color outside Endesga64'
  text+=write_sprite(name,id,im,['interior'] if id.startswith('comedor') else ['azulejo-rojo'],reason)+'\n'
 (ROOT/'src/game/sprites/environment.ts').write_text(text.rstrip()+'\n')
 print('4 exact native environment matrices written.')
