from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'scene-source.json').read_text());P=DATA['palette']
CX=32;WAIST=76;SIZE=(64,118)
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def color(name):return tuple(bytes.fromhex(P[name][1:]))+(255,)
def prototype():return Image.open(ROOT/'customer-full-1x.png').convert('RGBA')
def text(im,xy,label,size=22,ink='gris-claro'):
 ImageDraw.Draw(im).text(xy,label,font=ImageFont.truetype(FONT,size),fill=P[ink])
def sprite(key):
 d=DATA['sprites'][key];im=Image.new('RGBA',(d['width'],d['height']))
 for y,row in enumerate(d['frames'][0]):
  for x,letter in enumerate(row):
   if letter!='.':im.putpixel((x,y),color(d['colors'][letter]))
 return im

def scene(orientation='horizontal',with_burger=True):
 l=DATA['layouts'][orientation];im=Image.new('RGBA',(l['w'],l['h']),color('noche'))
 def place(key,x,y):im.alpha_composite(sprite(key),(round(x),round(y)))
 vertical=orientation=='vertical'
 place('comedor_v' if vertical else 'comedor',0,0)
 # Native 1:1 placement: the silhouette is about twice as wide as the plate.
 person=prototype().crop((0,0,64,80)).resize((96,120),Image.Resampling.NEAREST);pos=tuple(l['customer'][:2])
 im.alpha_composite(person,pos)
 place('barra_roja_v' if vertical else 'barra_roja',*l['counter'][:2])
 place('plato',*l['plate'][:2])
 for name,rect in l['bottles'].items():place('bote:'+name,*rect[:2])
 for name,rect in l['bins'].items():
  key='bandeja_'+name;obj=sprite(key)
  place(key,rect[0]+(rect[2]-obj.width)//2,rect[1]+rect[3]-obj.height)
 place('plancha_v' if vertical else 'plancha',*l['grill'][:2])
 for key in ['charola','basura']:
  rect=l[key];obj=sprite(key)
  place(key,rect[0]+(rect[2]-obj.width)//2,rect[1]+rect[3]-obj.height)
 if with_burger:
  px,py=l['plate'][:2];base=py+DATA['anchors']['plato'][1]
  for key,h in [('pan_base',3),('carne:perfecta',3),('queso',1),('lechuga',2),('tomate',2),('pan_tapa',7)]:
   ax,ay=DATA['anchors'][key.split(':')[0]];place(key,px+15-ax,base-ay);base-=h
 return im


def export():
 for orientation in ['horizontal','vertical']:
  im=scene(orientation);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/f'context-{orientation}.png')
 out=Image.new('RGB',(1460,850),P['negro'])
 text(out,(24,20),'CONVERSIÓN A LA PALETA DEL JUEGO',30,'crema')
 text(out,(24,68),'Mismo modelo · escala uniforme · píxeles reales',21)
 text(out,(24,116),'SPRITE COMPLETO',20,'crema')
 bg=Image.new('RGB',(368,600),P['noche'])
 im=prototype().resize((256,472),Image.Resampling.NEAREST);bg.paste(im,(56,42),im);out.paste(bg,(24,154))
 text(out,(430,116),'PRUEBA EN EL ESCENARIO',20,'crema')
 im=scene().resize((960,600),Image.Resampling.NEAREST);out.paste(im,(430,154),im)
 text(out,(24,780),'64 × 118 píxeles · 4 colores de la paleta',20,'crema')
 text(out,(430,780),'Recorte para la barra: 64 × 80 · misma cuadrícula que los clientes actuales',20,'crema')
 out.save(ROOT/'palette-review.png')
if __name__=='__main__':export()
