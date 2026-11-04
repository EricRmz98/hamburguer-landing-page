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

project=ns['proj']
def box3(im,x,z,w,d,h0,h1,top,front,side):
 # All furniture shares one projection and the same seat/table height units.
 a,b,cc,dd=[project(xx,zz,h1) for xx,zz in [(x-w/2,z+d/2),(x+w/2,z+d/2),(x+w/2,z-d/2),(x-w/2,z-d/2)]]
 bb,bc,bd=[project(xx,zz,h0) for xx,zz in [(x+w/2,z+d/2),(x+w/2,z-d/2),(x-w/2,z-d/2)]]
 poly(im,[b,cc,bc,bb],side);poly(im,[dd,cc,bc,bd],front);poly(im,[a,b,cc,dd],top)
 if top=='gris-claro':
  for px,py in [a,b,cc,dd]:rect(im,(px,py,px,py),'gris-azul')
 line(im,[a,b,cc,dd,a],'gris-azul' if top=='gris-claro' else 'cafe-oscuro');line(im,[dd,bd,bc,cc],'pizarra' if top=='gris-claro' else 'cafe-oscuro');line(im,[a,b],'blanco' if top=='gris-claro' else 'rojo')

def bench(im,x,z,w=1.8,d=.65,orientation='back'):
 # Upholstered seat, dark plinth and padded back. Side backs follow the depth axis.
 box3(im,x,z,w,d,0,.12,'noche','noche','negro')
 box3(im,x,z,w,d,.12,.35,'rojo','rojo-oscuro','rojo-oscuro')
 if orientation=='back':
  box3(im,x,z+d/2-.08,w,.18,.35,.95,'rojo','rojo-oscuro','rojo-oscuro')
  for f in [-.25,.25]:line(im,[project(x+w*f,z+d/2-.19,.4),project(x+w*f,z+d/2-.19,.87)],'cafe-oscuro')
  line(im,[project(x-w/2+.12,z+d/2-.19,.84),project(x+w/2-.12,z+d/2-.19,.84)],'rojo')
 else:
  bx=x+(-w/2+.08 if orientation=='left' else w/2-.08)
  box3(im,bx,z,.18,d,.35,.95,'rojo','rojo-oscuro','rojo-oscuro')
  for f in [-.25,.25]:line(im,[project(bx+(.1 if orientation=='left' else -.1),z+d*f,.4),project(bx+(.1 if orientation=='left' else -.1),z+d*f,.87)],'cafe-oscuro')
 # Seat seam and small corner highlight.
 line(im,[project(x-w/2+.08,z-d/2+.1,.35),project(x+w/2-.08,z-d/2+.1,.35)],'rosa')

def dining_table(im,x,z,w=1.4,d=.85):
 # Four legs ground the table; tabletop height is constant across all distances.
 for dx,dz in [(-.45,-.26),(.45,-.26),(-.45,.26),(.45,.26)]:
  box3(im,x+dx*w,z+dz*d,.08,.08,0,.59,'gris-azul','pizarra','noche')
 box3(im,x,z,w,d,.56,.65,'gris-claro','gris','gris-azul')
 a=project(x-w*.35,z+d*.3,.66);b=project(x+w*.35,z+d*.3,.66);line(im,[a,b],'blanco')
 xx,yy=project(x+.25,z,.66)
 rounded(im,(xx-1,yy-4,xx+1,yy),'rojo-oscuro','cafe-oscuro',1);rect(im,(xx,yy-5,xx,yy-4),'gris')
 xx,yy=project(x-.2,z,.66);rect(im,(xx-2,yy-1,xx+1,yy),'crema')

def chair3(im,x,z,facing='back'):
 # Same physical seat height as sofas; no screen-space scale multipliers.
 w,d=.62,.6
 for dx,dz in [(-.23,-.21),(.23,-.21),(-.23,.21),(.23,.21)]:
  box3(im,x+dx,z+dz,.085,.085,0,.35,'gris-azul','pizarra','noche')
 box3(im,x,z,w,d,.29,.35,'rojo','rojo-oscuro','rojo-oscuro')
 if facing in ['back','front']:
  zz=z+(.25 if facing=='back' else -.25)
  box3(im,x,zz,w,.12,.35,.92,'rojo','rojo-oscuro','rojo-oscuro')
  line(im,[project(x-w/2+.1,zz-.07,.84),project(x+w/2-.1,zz-.07,.84)],'rojo')
 else:
  xx=x+(-.25 if facing=='left' else .25)
  box3(im,xx,z,.12,d,.35,.92,'rojo','rojo-oscuro','rojo-oscuro')
  line(im,[project(xx,z-.2,.84),project(xx,z+.2,.84)],'rojo')

def furniture(im):
 objects=[]
 def put(kind,x,z,*args):objects.append((z,kind,x,args))
 # Window booths: each dining table seats two on the bench and two opposite.
 for x in [-6.1,.65]:
  put('bench',x,5.7,3.1,.72,'back')
  put('table',x,4.65,2.0,.9)
  for dx in [-.53,.53]:put('chair',x+dx,3.68,'front')
 # Side booths: seat backs follow their wall, chairs face them from the aisle side.
 for side in [-1,1]:
  for z,bx,tx,depth in [(2.65,4.55,3.45,1.65),(.65,3.4,2.45,1.4)]:
   put('bench',side*bx,z,.7,depth,'left' if side<0 else 'right')
   put('table',side*tx,z,1.2,1.12)
   put('chair',side*(tx-1.0),z,'right' if side<0 else 'left')
 # Complete central table pairs with the same chair dimensions as all other sets.
 for x,z in [(-1.45,2.65),(.6,1.45)]:
  put('chair',x,z+.82,'back');put('table',x,z,1.3,.88);put('chair',x,z-.82,'front')
 # Check furniture footprints in the common floor coordinate system.
 footprints=[]
 for z,kind,x,args in objects:
  w,d=(.62,.6) if kind=='chair' else args[:2]
  footprints.append((kind,x-w/2,x+w/2,z-d/2,z+d/2))
 collisions=[]
 for i,a in enumerate(footprints):
  for j,b in enumerate(footprints[:i]):
   if min(a[2],b[2])-max(a[1],b[1])>.001 and min(a[4],b[4])-max(a[3],b[3])>.001:
    collisions.append((i,j))
 assert not collisions, f'Overlapping furniture footprints: {collisions}'
 # Stable painter order: distant pieces first, near pieces cover their lower edges.
 for z,kind,x,args in sorted(objects,key=lambda obj:obj[0],reverse=True):
  {'bench':bench,'table':dining_table,'chair':chair3}[kind](im,x,z,*args)

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
 furniture(im)
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
