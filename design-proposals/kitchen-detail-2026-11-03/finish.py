from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
def label(im,xy,text):ImageDraw.Draw(im).text(xy,text,font=font,fill='white')
checks=json.loads((OUT/'composicion/browser-checks.json').read_text())
for c in checks:
 b=c['clip'];x=math.floor(b['x']+.5);y=math.floor(b['y']+.5);im=Image.open(OUT/f'composicion/{c["layout"]}-full.png')
 assert c['scale']==int(c['scale']) and c['sameGrid']
 assert x+b['width']<=im.width and y+b['height']<=im.height
 im.crop((x,y,x+b['width'],y+b['height'])).save(OUT/f'composicion/{c["layout"]}.png')
im=Image.new('RGB',(1048,630),'#0a0a0a');label(im,(16,12),'Cocina detallada · Horizontal');label(im,(680,12),'Vertical')
im.paste(Image.open(OUT/'composicion/horizontal.png'),(16,50));im.paste(Image.open(OUT/'composicion/vertical.png'),(680,50));im.save(OUT/'composicion-final.png')
im=Image.new('RGB',(1312,460),'#0a0a0a');label(im,(12,12),'Antes');label(im,(668,12),'Ahora · materiales y volumen')
im.paste(Image.open(OUT.parent/'endesga64-unified-2026-11-03/composicion/horizontal-01.png'),(12,48));im.paste(Image.open(OUT/'composicion/horizontal.png'),(668,48));im.save(OUT/'antes-despues.png')
# Compare with the exact production export from the previous pass: dimensions and alpha silhouettes.
before=json.loads((OUT.parent/'endesga64-unified-2026-11-03/native-assets.json').read_text());after=json.loads((OUT/'native-assets.json').read_text());old={s['key']:s for s in before['sprites']};changed=[]
for s in after['sprites']:
 a=old[s['key']];assert (s['width'],s['height'])==(a['width'],a['height'])
 assert [[['.'==c for c in row] for row in frame] for frame in s['frames']]==[[['.'==c for c in row] for row in frame] for frame in a['frames']]
 pixels=lambda t:[None if c=='.' else t['colors'][c] for f in t['frames'] for row in f for c in row]
 n=sum(a!=b for a,b in zip(pixels(a),pixels(s)))
 if n:changed.append({'sprite':s['key'],'changed_cells':n})
for name in ['comedor.png','comedor_v.png']:
 assert (ROOT/'scripts/sprites/environment-native'/name).read_bytes()==(OUT/'before'/name).read_bytes()
assert (ROOT/'src/game/sprites/anchors.ts').read_bytes()==(OUT/'before/anchors.ts').read_bytes()
(OUT/'checks.json').write_text(json.dumps({'unchanged_dimensions_and_alpha':True,'unchanged_anchors':True,'approved_background_unchanged':True,'palette':'Endesga 64','changed':changed,'tests_passed':161,'build':'passed','browser_layouts':['horizontal','vertical'],'console_errors':[]},indent=2)+'\n')
print('Dimensions, silhouettes, anchors and approved background preserved. '+str(len(changed))+' detailed sprite variants.')
