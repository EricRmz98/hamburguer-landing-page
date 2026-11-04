"""Dining room studies, separate from runtime. Pixel geometry + exact approved matrices."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json, math
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'source-sprites.json').read_text());P=DATA['palette'];S=DATA['sprites']
def c(v):return P.get(v,v)
def rect(im,b,col):ImageDraw.Draw(im).rectangle(tuple(round(v) for v in b),fill=c(col))
def poly(im,pts,col):ImageDraw.Draw(im).polygon([(round(x),round(y)) for x,y in pts],fill=c(col))
def line(im,pts,col,w=1):ImageDraw.Draw(im).line([(round(x),round(y)) for x,y in pts],fill=c(col),width=w)
def spr(im,k,x,y):
 s=S[k];o=Image.new('RGBA',(s['width'],s['height']))
 for j,row in enumerate(s['frames'][0]):
  for i,k in enumerate(row):
   if k!='.':o.putpixel((i,j),tuple(bytes.fromhex(P[s['colors'][k]][1:]))+(255,))
 im.paste(o,(x,y),o)
def proj(x,z,h=0):return (160+x*95/(z+1.6),45+(110-h*70)/(z+1.6))
def world(im,x,z,w,d,h,col,edge='cafe-oscuro'):
 p=[proj(x-w/2,z+d/2,h),proj(x+w/2,z+d/2,h),proj(x+w/2,z-d/2,h),proj(x-w/2,z-d/2,h)]
 poly(im,p,col);line(im,p+[p[0]],edge)
 return p

def table(im,x,z,mat,chair,roundtop=False):
 # Chairs behind table, leg silhouettes grounded on floor.
 for dx in [-.56,.56]:
  xx,yy=proj(x+dx,z+.24);scale=95/(z+1.6)
  rect(im,(xx-3,yy-scale*.3,xx+3,yy-scale*.13),chair)
  line(im,[(xx-3,yy-scale*.13),(xx-3,yy)],'negro');line(im,[(xx+3,yy-scale*.13),(xx+3,yy)],'negro')
 # Floor contact shadow.
 world(im,x,z,.98,.55,0,'noche','noche')
 for dx,dz in [(-.36,-.2),(.36,-.2),(-.36,.2),(.36,.2)]:
  line(im,[proj(x+dx,z+dz,.45),proj(x+dx,z+dz,0)],'cafe-oscuro',2)
 p=world(im,x,z,1.13,.66,.48,mat)
 line(im,[p[3],p[2]],'canela' if mat in ['cafe','canela'] else 'gris-azul',2)
 # Tiny napkin and ketchup at a believable distant scale.
 xx,yy=proj(x,z,.49);rect(im,(xx-2,yy-1,xx+2,yy+1),'gris');rect(im,(xx+4,yy-4,xx+5,yy),'rojo-oscuro')
 # Front chair at side avoids hiding whole tabletop.
 xx,yy=proj(x-.68,z-.36);ss=95/(z+1.6)
 rect(im,(xx-3,yy-ss*.2,xx+3,yy-ss*.1),chair)
 line(im,[(xx-3,yy-ss*.1),(xx-3,yy+1)],'negro');line(im,[(xx+3,yy-ss*.1),(xx+3,yy+1)],'negro')

def door(im,x,w,night=False):
 rect(im,(x-3,8,x+w+3,62),'cafe-oscuro');rect(im,(x,10,x+w,60),'gris-azul')
 rect(im,(x+2,12,x+w-2,56),'azul-oscuro' if night else 'gris')
 # Street seen through glass: opposite shop, sidewalk, window panes.
 rect(im,(x+3,28,x+w-3,45),'noche' if night else 'pizarra')
 for xx in range(x+5,x+w-4,9):rect(im,(xx,32,xx+3,37),'ambar' if night else 'gris-azul')
 rect(im,(x+2,48,x+w-2,57),'pizarra' if night else 'gris-claro')
 line(im,[(x+4,24),(x+w-5,14)],'gris-claro');line(im,[(x+4,28),(x+w-5,18)],'gris')
 line(im,[(x+w//2,11),(x+w//2,58)],'noche')
 rect(im,(x+w//2+3,36,x+w//2+4,42),'crema');rect(im,(x-4,61,x+w+4,64),'gris-azul')
 # Welcome mat extends onto floor, marking the threshold.
 poly(im,[(x-1,65),(x+w+1,65),(x+w+7,70),(x-7,70)],'noche')
 rect(im,(x+w//2-8,3,x+w//2+8,7),'verde-noche');line(im,[(x+w//2-4,5),(x+w//2+4,5)],'gris')

def window(im,x,w):
 rect(im,(x,15,x+w,44),'cafe-oscuro');rect(im,(x+2,17,x+w-2,42),'gris-azul')
 rect(im,(x+3,30,x+w-3,40),'pizarra');line(im,[(x+w/2,17),(x+w/2,42)],'noche')
 line(im,[(x+4,24),(x+w-5,18)],'gris');rect(im,(x-2,44,x+w+2,46),'cafe')
def plant(im,x,y,s=1):
 rect(im,(x-3*s,y-5*s,x+3*s,y),'cafe');rect(im,(x-2*s,y-4*s,x+2*s,y-1),'canela')
 line(im,[(x,y-5*s),(x,y-16*s)],'verde-oscuro',s)
 for dx,dy in [(-4,-12),(3,-15),(-3,-17),(4,-9)]:poly(im,[(x,y+(dy+4)*s),(x+dx*s,y+dy*s),(x,y+(dy-1)*s)],'verde-oscuro')
def lamp(im,x,y):
 line(im,[(x,0),(x,y)],'negro');poly(im,[(x-4,y),(x+4,y),(x+8,y+5),(x-8,y+5)],'cafe-oscuro');line(im,[(x-6,y+6),(x+6,y+6)],'ambar')
def booth(im,x,z,mat):
 # Backrest and seat in world space: several planes, never pasted on back wall.
 p=world(im,x,z,1.35,.5,.13,mat)
 for side in [-.65,.65]:
  a=proj(x+side,z+.3,.15);b=proj(x+side,z+.3,.75)
  line(im,[a,b],'cafe-oscuro',3)
 poly(im,[proj(x-.65,z+.3,.2),proj(x+.65,z+.3,.2),proj(x+.65,z+.3,.75),proj(x-.65,z+.3,.75)],mat)
 line(im,[proj(x-.6,z+.3,.7),proj(x+.6,z+.3,.7)],'cafe')

def interior(n):
 im=Image.new('RGB',(320,122),c('noche'))
 wall=['cafe-oscuro','noche','verde-noche','pizarra','cafe-oscuro','noche'][n-1]
 floor=['cafe','pizarra','cafe-oscuro','noche','cafe','pizarra'][n-1]
 rect(im,(28,0,291,61),wall)
 poly(im,[(0,0),(28,0),(28,62),(0,89)],'negro' if n in [2,6] else 'noche')
 poly(im,[(292,0),(319,0),(319,89),(292,62)],'noche')
 poly(im,[(28,62),(292,62),(319,89),(319,121),(0,121),(0,89)],floor)
 line(im,[(0,89),(28,62),(292,62),(319,89)],'cafe-oscuro',2)
 # Strong converging floor grid establishes depth; plank/ceramic varies by concept.
 for xx in range(-400,721,45):line(im,[(160+(xx-160)*.23,62),(xx,121)],('negro' if n in [3,4] else 'cafe-oscuro' if n in [1,5] else 'noche'))
 for yy in [65,71,80,94,115]:line(im,[(0,yy),(319,yy)],('negro' if n in [3,4] else 'cafe-oscuro' if n in [1,5] else 'noche'))
 # Wall dado with small framed artwork; architectural lines remain above the floor.
 line(im,[(28,48),(292,48)],'cafe' if n in [1,5] else 'gris-azul')
 if n==1:
  door(im,140,38);window(im,39,65);window(im,218,64)
  lamp(im,88,14);lamp(im,235,14)
  for x,z in [(-2.4,5),(2.4,5),(-2.1,2.5),(2.1,2.5),(-2.3,.6),(2.3,.6)]:table(im,x,z,'canela','rojo-oscuro')
 elif n==2:
  door(im,244,32,True);window(im,46,73);window(im,143,69)
  for x,z in [(-2.4,4.4),(-1.6,1.5),(2.3,1.0)]:
   booth(im,x,z+.65,'rojo-oscuro');table(im,x,z,'gris','rojo-oscuro')
  lamp(im,94,11);lamp(im,204,11)
 elif n==3:
  door(im,40,36);window(im,104,72);window(im,206,73)
  for x,z in [(1.4,4.7),(2.4,2.3),(-2.3,1),(1.8,.3)]:table(im,x,z,'canela','verde-oscuro')
  plant(im,85,65);plant(im,283,69);lamp(im,154,13);lamp(im,265,17)
 elif n==4:
  door(im,143,34);window(im,40,72);window(im,209,73)
  for x,z in [(-2.4,4.7),(2.4,4.7),(-2.1,1.8),(2.1,1.8)]:table(im,x,z,'gris-azul','pizarra')
  for x in [89,232]:lamp(im,x,12)
  plant(im,121,65);plant(im,196,65)
 elif n==5:
  door(im,231,40);window(im,45,69);window(im,135,68)
  for x,z in [(-2.4,4.5),(-2,2),(1.8,2),(-2.3,.1)]:
   booth(im,x,z+.5,'verde-oscuro');table(im,x,z,'canela','verde-noche')
  lamp(im,75,13);lamp(im,174,13);plant(im,285,68)
 elif n==6:
  door(im,46,34,True);window(im,112,75);window(im,214,66)
  for x,z in [(1.5,4.5),(-2,2.2),(2,1.7),(-2.6,.2)]:table(im,x,z,'cafe','rojo-oscuro')
  lamp(im,150,12);lamp(im,250,12)
  line(im,[(94,9),(281,9)],'rojo-oscuro');plant(im,91,66)
 # Small occupied distant seat, avoiding central customer silhouette.
 xx,yy=proj(2.4 if n in [1,3,4] else -2.4,4.6,.65)
 rect(im,(xx-2,yy-5,xx+2,yy-1),'cafe');rect(im,(xx-3,yy,xx+3,yy+6),'pizarra')
 return im

def bar(n):
 im=Image.new('RGB',(320,78),c('noche'))
 base=['cafe','gris-azul','verde-noche','pizarra','cafe-oscuro','noche'][n-1]
 rect(im,(0,0,319,77),base)
 # Work surface is a continuous horizontal plane; a narrow front lip only at bottom.
 if n in [1,5]:
  for yy in [0,17,39,67]:
   line(im,[(0,yy),(319,yy)],'canela' if n==1 else 'cafe')
   line(im,[(0,yy+1),(319,yy+1)],'cafe-oscuro' if n==1 else 'negro')
  for x,yy in [(12,8),(275,8),(22,29),(288,51),(48,61),(190,28)]:line(im,[(x,yy),(x+14,yy)],'cafe-oscuro' if n==1 else 'cafe')
  for x,y0,y1 in [(32,1,16),(279,18,38),(43,40,66)]:line(im,[(x,y0),(x-2,y1)],'cafe-oscuro' if n==1 else 'negro')
 elif n==2:
  for yy in [1,3,71]:line(im,[(0,yy),(319,yy)],'gris')
  for x in [12,304]:line(im,[(x,6),(x-4,68)],'pizarra')
 elif n in [3,4]:
  # Tile joints fan toward the vanishing point, unlike vertical cabinet panels.
  for xx in range(-160,481,48):line(im,[(160+(xx-160)*.68,0),(xx,72)],'negro' if n==3 else 'noche')
  for yy in [0,14,36,70]:line(im,[(0,yy),(319,yy)],'verde-oscuro' if n==3 else 'gris-azul')
 else:
  for x,yy in [(9,7),(267,9),(12,45),(289,61)]:line(im,[(x,yy),(x+7,yy+2),(x+11,yy+7)],'pizarra')
  line(im,[(0,1),(319,1)],'gris-azul')
 rect(im,(0,73,319,77),'cafe-oscuro' if n in [1,3,5] else 'negro')
 line(im,[(0,73),(319,73)],'canela' if n in [1,3,5] else 'gris-azul')
 line(im,[(0,0),(319,0)],'canela' if n in [1,5] else 'gris-azul')
 return im

def scene(n):
 im=Image.new('RGB',(320,200),c('negro'));im.paste(interior(n),(0,0));spr(im,'cliente:azul',136,46);im.paste(bar(n),(0,122))
 spr(im,'plato',145,120)
 for k,x in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:spr(im,k,x,103)
 for k,x in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:spr(im,k,x,139)
 spr(im,'plancha',82,165);spr(im,'charola',244,165);spr(im,'basura',40,170)
 for x in [97,135]:spr(im,'carne:perfecta',x,168)
 for k,x,y in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:spr(im,k,x,y)
 return im
NAMES=[('Salón de barrio','Acceso central · mesas de madera · sillas burdeos','Roble horizontal'),('Diner de esquina','Entrada derecha · booths rojos · calle nocturna','Acero satinado'),('Comedor jardín','Entrada izquierda · recorrido diagonal · plantas','Cerámica verde'),('Local urbano','Eje central abierto · mesas metálicas · suelo oscuro','Baldosa azul'),('Cantina de madera','Entrada derecha · bancos verdes · madera cálida','Nogal de trabajo'),('Hamburguesería nocturna','Acceso izquierdo · mesas escalonadas · acento rojo','Piedra grafito')]
def font(s):return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',s)
def text(im,xy,t,s=22,col='gris'):ImageDraw.Draw(im).text(xy,t,font=font(s),fill=c(col))
for n in range(1,7):
 interior(n).save(ROOT/f'interior-{n:02}-clean-1x.png');bar(n).save(ROOT/f'bar-{n:02}-clean-1x.png');scene(n).save(ROOT/f'pair-{n:02}-context-1x.png')
# Clean interiors have room to read furniture and entrance, without placeholder UI.
out=Image.new('RGB',(2048,1610),c('negro'));text(out,(40,25),'EL COMEDOR / SEIS INTERIORES',34,'crema');text(out,(40,74),'Desde el puesto del cocinero · fondos limpios · píxel ×3',22)
for n,(name,desc,bname) in enumerate(NAMES,1):
 x=40+(n-1)%2*1000;y=128+(n-1)//2*475
 text(out,(x,y),f'F{n:02}  {name}',27,'crema');text(out,(x,y+36),desc,20)
 out.paste(interior(n).resize((960,366),Image.Resampling.NEAREST),(x,y+72))
text(out,(40,1570),'Los objetos más pequeños están al fondo; el pasillo llega hasta el mostrador. Sin interfaz superpuesta.',19)
out.save(ROOT/'interiors-six-options.png')
out=Image.new('RGB',(2048,2240),c('negro'));text(out,(40,25),'SEIS BARRAS / SEIS PAREJAS',34,'crema');text(out,(40,74),'Superficies de trabajo horizontales · sprites finales intactos · píxel ×3',22)
for n,(name,desc,bname) in enumerate(NAMES,1):
 x=40+(n-1)%2*1000;y=130+(n-1)//2*690
 text(out,(x,y),f'B{n:02}  {bname} + F{n:02}',27,'crema');text(out,(x,y+36),name,20)
 out.paste(scene(n).resize((960,600),Image.Resampling.NEAREST),(x,y+72))
text(out,(40,2208),'Mismas posiciones del juego. Sin comanda ni globo para comparar el espacio; su composición queda pendiente.',18)
out.save(ROOT/'bars-six-pairs.png')
allowed={tuple(bytes.fromhex(v[1:])) for v in P.values()}
for p in ROOT.glob('*-1x.png'):assert set(Image.open(p).getdata())<=allowed,p
print('18 native PNGs + 2 sheets; palette verified.')
