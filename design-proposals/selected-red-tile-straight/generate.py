"""Selected B03 + F05, isolated visual refinement. No production writes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'cartoon-dining-2026-10-31'
# Reuse pixel drawing helpers and approved sprite matrices without running sheet exports.
source=(BASE/'generate.py').read_text().split('for n in range(1,7):')[0]
ns={'__file__':str(BASE/'generate.py')};exec(compile(source,str(BASE/'generate.py'),'exec'),ns)
rect,line,poly,rounded,ellipse=[ns[k] for k in ['rect','line','poly','rounded','ellipse']]
c=ns['c'];spr=ns['spr'];P=ns['P']

def interior():
 im=Image.new('RGB',(320,122),c('pizarra'))
 # White painted walls, dark structural steel and exposed conduit.
 rect(im,(26,0,293,61),'gris-claro')
 poly(im,[(0,0),(26,0),(26,61),(0,85)],'gris-azul')
 poly(im,[(294,0),(319,0),(319,85),(294,61)],'gris')
 for x in [29,119,211,289]:
  rect(im,(x,0,x+3,60),'pizarra');line(im,[(x,0),(x,59)],'gris-azul')
 rect(im,(27,0,293,4),'noche');line(im,[(27,5),(293,5)],'gris')
 line(im,[(34,9),(280,9),(280,17)],'gris-azul',2)
 # Red lower wall and white protective rail.
 rect(im,(26,47,293,61),'rojo-oscuro');line(im,[(26,48),(293,48)],'rojo')
 line(im,[(26,46),(293,46)],'blanco',2)
 # Polished concrete: broad slabs and restrained hard-edged reflections, no checkerboard.
 poly(im,[(26,62),(294,62),(319,85),(319,121),(0,121),(0,85)],'gris-azul')
 poly(im,[(42,65),(104,65),(84,80),(16,80)],'gris')
 poly(im,[(141,65),(196,65),(215,79),(142,79)],'gris')
 poly(im,[(234,65),(271,65),(301,80),(255,80)],'gris')
 for pts in [[(90,63),(49,121)],[(220,63),(272,121)],[(0,100),(319,100)]]:line(im,pts,'pizarra')
 for x,y,w in [(27,87,19),(259,91,24),(107,112,33),(194,86,17)]:
  line(im,[(x,y),(x+w,y)],'gris');line(im,[(x+3,y+2),(x+w-3,y+2)],'gris')
 for x,y in [(16,114),(303,106),(119,94),(217,116),(39,83)]:rect(im,(x,y,x+1,y),'pizarra')
 # F05 preserved: entry right, two windows, asymmetric booths and tables.
 # Reuse rounded frames recolored from warm timber into red enamel/steel.
 def recolor_draw(fn,*args):
  layer=Image.new('RGB',im.size,c('alerta'));fn(layer,*args)
  mapping={c('cafe'):c('rojo-oscuro'),c('canela'):c('rojo'),c('durazno'):c('rosa'),c('cafe-oscuro'):c('noche')}
  pix=layer.load();dst=im.load()
  for y in range(122):
   for x in range(320):
    col=pix[x,y]
    if col!=tuple(bytes.fromhex(P['alerta'][1:])):
     hx='#%02x%02x%02x'%col;v=mapping.get(hx,hx);dst[x,y]=tuple(bytes.fromhex(v[1:]))
 recolor_draw(ns['door'],231,40)
 recolor_draw(ns['window'],45,69);recolor_draw(ns['window'],135,68)
 ns['lamp'](im,75,13);ns['lamp'](im,174,13)
 # White diner tops, red padded booths. Original F05 furniture positions.
 for x,z in [(-2.4,4.5),(-2,2),(1.8,2),(-2.3,.1)]:
  ns['booth'](im,x,z+.5,'rojo-oscuro')
  ns['table'](im,x,z,'gris-claro','rojo-oscuro')
 ns['plant'](im,285,68)
 return im

def red_bar():
 im=Image.new('RGB',(320,78),c('rojo-oscuro'))
 # Equal aligned tiles; only horizontal and vertical joints, matching equipment axes.
 for y in range(4,72,17):
  for x in range(0,320,32):
   rect(im,(x,y,x+31,min(y+16,72)),'cafe-oscuro')
   rect(im,(x+1,y+1,x+30,min(y+15,71)),'rojo-oscuro')
   line(im,[(x+2,y+1),(x+29,y+1)],'rojo')
   line(im,[(x+1,y+2),(x+1,min(y+13,70))],'rojo')
 rect(im,(0,0,319,3),'cafe-oscuro');line(im,[(0,1),(319,1)],'rojo')
 rect(im,(0,73,319,77),'cafe-oscuro');line(im,[(0,73),(319,73)],'rojo')
 return im

def scene():
 im=Image.new('RGB',(320,200),c('negro'));im.paste(interior(),(0,0));spr(im,'cliente:azul',136,46)
 im.paste(red_bar(),(0,122))
 spr(im,'plato',145,120)
 for k,x in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:spr(im,k,x,103)
 for k,x in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:spr(im,k,x,139)
 spr(im,'plancha',82,165);spr(im,'charola',244,165);spr(im,'basura',40,170)
 for x in [97,135]:spr(im,'carne:perfecta',x,168)
 for k,x,y in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:spr(im,k,x,y)
 return im
im=scene();bg=interior();im.save(ROOT/'selected-context-1x.png');bg.save(ROOT/'selected-interior-1x.png');red_bar().save(ROOT/'selected-bar-1x.png')
im.resize((1280,800),Image.Resampling.NEAREST).save(ROOT/'selected-context-4x.png')
bg.resize((1280,488),Image.Resampling.NEAREST).save(ROOT/'selected-interior-4x.png')
allowed={tuple(bytes.fromhex(v[1:])) for v in P.values()}
assert set(im.getdata())<=allowed;assert set(bg.getdata())<=allowed
print('Selected B03 + F05 rendered; Endesga 32 verified; final sprite matrices unchanged.')
