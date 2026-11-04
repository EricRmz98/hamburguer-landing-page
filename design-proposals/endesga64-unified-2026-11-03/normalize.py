"""Art-direction import: one-time native reduction, restricted official colors, then editable masters.
Final environment_gen.py only reads those native masters; runtime never rescales this artwork.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json,re
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
P={a or b:h for a,b,h in re.findall(r"(?:'([^']+)'|([\w-]+)):\s*'(#[0-9a-f]{6})'",(ROOT/'src/game/sprites/palette.ts').read_text())}
# Material-specific subset; no neon accents or skin colors in concrete/plaster/glass.
NAMES='negro carbon grafito gris-oscuro gris-neutro gris-medio plata blanco gris-claro gris gris-azul pizarra noche azul-tinta tinta cafe-negro cafe-oscuro cafe oxido rojo-oscuro carmesi rojo-ladrillo rojo coral crema tostado verde-noche verde-oscuro verde verde-claro'.split()
RGB={n:tuple(bytes.fromhex(P[n][1:])) for n in NAMES}
CACHE={}
def nearest(rgb):
 if rgb not in CACHE:
  r,g,b=rgb
  choices=NAMES
  # Warm low-saturation plaster becomes neutral, while red upholstery stays red.
  if max(rgb)-min(rgb)<42: choices=NAMES[:16]
  CACHE[rgb]=RGB[min(choices,key=lambda n:sum(w*(a-b)**2 for w,a,b in zip((.26,.55,.19),rgb,RGB[n])))]
 return CACHE[rgb]
def native(source,size):
 # BOX averages one native cell, then hard-assigns one official color; zero dithering/alpha.
 small=Image.open(source).convert('RGB').resize(size,Image.Resampling.BOX)
 out=Image.new('RGB',size);out.putdata([nearest(c) for c in small.getdata()]);return out
def counter(w,h):
 im=Image.new('RGB',(w,h),P['rojo-oscuro']);d=ImageDraw.Draw(im)
 # Small, restrained ceramic bevels, straight tile joints matching the service equipment.
 for y in range(5,h-3,17):
  for x in range(0,w,32):
   d.rectangle((x,y,x+31,min(y+16,h-3)),fill=P['rojo-oscuro'])
   d.rectangle((x+1,y+1,x+30,min(y+15,h-4)),fill=P['carmesi'])
   d.line((x+2,y+1,x+29,y+1),fill=P['rojo-ladrillo'])
   d.line((x+1,y+2,x+1,min(y+13,h-4)),fill=P['rojo-ladrillo'])
   if (x//32+y//17)%3==0:d.line((x+3,y+3,x+7,y+3),fill=P['rojo-ladrillo'])
 # Neutral stainless service lip and dark contact edge; no oversized saturated bevel.
 d.rectangle((0,0,w-1,1),fill=P['gris-claro']);d.line((0,2,w-1,2),fill=P['gris-azul']);d.line((0,3,w-1,3),fill=P['noche'])
 d.rectangle((0,h-2,w-1,h-1),fill=P['noche']);return im
for id,size,source in [('comedor',(320,122),'referencia-horizontal.png'),('comedor_v',(180,200),'referencia-vertical.png')]:
 if not (OUT/source).exists():continue
 im=native(OUT/source,size)
 if id=='comedor':
  # Reverse the right chair together with its immediate contact shadow, native cell for cell.
  box=(183,62,218,115);im.paste(ImageOps.mirror(im.crop(box)),box[:2])
 im.save(ROOT/'scripts/sprites/environment-native'/f'{id}.png')
 im.resize((size[0]*4,size[1]*4),Image.Resampling.NEAREST).save(OUT/f'{id}-4x.png')
for id,size in [('barra_roja',(320,78)),('barra_roja_v',(180,80))]:counter(*size).save(ROOT/'scripts/sprites/environment-native'/f'{id}.png')
