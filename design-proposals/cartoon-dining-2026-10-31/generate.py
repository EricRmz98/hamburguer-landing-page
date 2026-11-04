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

def rounded(im,box,fill,outline,r=3):
 box=tuple(round(v) for v in box)
 ImageDraw.Draw(im).rounded_rectangle(box,radius=r,fill=c(fill),outline=c(outline),width=1)
def ellipse(im,box,fill):ImageDraw.Draw(im).ellipse(tuple(round(v) for v in box),fill=c(fill))
def chair_sprite(im,x,y,size,mat):
 w=max(6,round(size*.34));h=max(8,round(size*.51))
 shadow,light={'rojo-oscuro':('cafe-oscuro','rojo'),'verde-oscuro':('verde-noche','verde'),'verde-noche':('verde-noche','verde-oscuro'),'pizarra':('noche','gris-azul')}.get(mat,('noche','gris-azul'))
 rounded(im,(x-w/2,y-h,x+w/2,y-3),mat,shadow,2)
 line(im,[(x-w/2+2,y-h+1),(x+w/2-2,y-h+1)],light)
 rounded(im,(x-w/2-1,y-5,x+w/2+1,y),light,shadow,2)
 rect(im,(x-w/2,y,x-w/2+2,y+5),shadow);rect(im,(x+w/2-2,y,x+w/2,y+5),shadow)
def table(im,x,z,mat,chair,roundtop=False):
 xx,yy=proj(x,z);sc=95/(z+1.6);w=max(17,round(sc*1.05));h=max(8,round(sc*.43));top=round(yy-sc*.38)
 ellipse(im,(xx-w*.6,yy-2,xx+w*.6,yy+4),'noche')
 chair_sprite(im,xx,yy-sc*.23,sc,chair)
 # Chunky pedestal, visible foot and layered rounded tabletop.
 rounded(im,(xx-3,top+3,xx+3,yy),'cafe','cafe-oscuro',2)
 ellipse(im,(xx-8,yy-3,xx+8,yy+2),'cafe-oscuro')
 dark='cafe-oscuro' if mat in ['canela','cafe'] else 'noche'
 mid='canela' if mat in ['canela','cafe'] else 'gris-azul'
 light='durazno' if mat in ['canela','cafe'] else 'gris'
 rounded(im,(xx-w/2,top-h/2+3,xx+w/2,top+h/2+4),mid,dark,4)
 rounded(im,(xx-w/2,top-h/2,xx+w/2,top+h/2),mat,dark,4)
 line(im,[(xx-w/2+4,top-h/2+1),(xx+w/2-4,top-h/2+1)],light)
 # Original sauce bottle silhouette language, reduced to a few distant pixels.
 rounded(im,(xx+3,top-5,xx+6,top),'rojo-oscuro','cafe-oscuro',1);rect(im,(xx+4,top-7,xx+5,top-5),'gris')
 rect(im,(xx-5,top-1,xx,top+1),'crema')
 chair_sprite(im,xx-w*.53,yy+1,sc*.86,chair)

def door(im,x,w,night=False):
 rounded(im,(x-4,6,x+w+4,63),'cafe','cafe-oscuro',6)
 line(im,[(x-1,13),(x-1,58)],'canela',2)
 rounded(im,(x+2,10,x+w-2,58),'gris-azul','cafe-oscuro',4)
 rounded(im,(x+4,12,x+w-4,47),'azul-oscuro' if night else 'gris','noche',3)
 rect(im,(x+5,31,x+w-5,44),'noche' if night else 'pizarra')
 for xx in range(x+7,x+w-6,9):rect(im,(xx,34,xx+3,38),'ambar' if night else 'gris-azul')
 line(im,[(x+7,25),(x+w-8,16)],'gris-claro',2)
 rounded(im,(x+w-9,36,x+w-6,43),'crema','cafe-oscuro',1)
 rounded(im,(x+7,49,x+w-7,55),'canela','cafe-oscuro',2)
 poly(im,[(x-3,63),(x+w+3,63),(x+w+9,69),(x-9,69)],'cafe-oscuro')
 line(im,[(x-1,64),(x+w+1,64)],'canela')
 # Hanging open sign, no tiny decorative type.
 line(im,[(x+w/2,19),(x+w/2-6,25),(x+w/2+6,25),(x+w/2,19)],'cafe-oscuro')
 rounded(im,(x+w/2-7,25,x+w/2+7,30),'crema','cafe-oscuro',1)
 line(im,[(x+w/2-4,27),(x+w/2+4,27)],'cafe')
def window(im,x,w):
 rounded(im,(x-2,13,x+w+2,46),'cafe','cafe-oscuro',5)
 rounded(im,(x+1,15,x+w-1,42),'gris-azul','noche',4)
 rect(im,(x+3,32,x+w-3,40),'pizarra')
 line(im,[(x+6,27),(x+w-7,18)],'gris',2)
 rect(im,(x+w/2-1,16,x+w/2+1,42),'cafe-oscuro')
 rounded(im,(x-4,43,x+w+4,48),'canela','cafe-oscuro',2)
 line(im,[(x-1,44),(x+w+1,44)],'durazno')
def plant(im,x,y,s=1):
 rounded(im,(x-5,y-8,x+5,y),'canela','cafe-oscuro',3)
 line(im,[(x-3,y-7),(x+2,y-7)],'durazno')
 for dx,dy in [(-4,-15),(4,-16),(0,-20),(-6,-11),(6,-10)]:
  ellipse(im,(x+dx-4,y+dy-4,x+dx+4,y+dy+3),'verde-noche')
  ellipse(im,(x+dx-3,y+dy-4,x+dx+2,y+dy),'verde-oscuro')
  line(im,[(x+dx-1,y+dy-3),(x+dx+1,y+dy-3)],'verde')
def lamp(im,x,y):
 line(im,[(x,0),(x,y)],'cafe-oscuro',2)
 ellipse(im,(x-10,y-1,x+10,y+9),'cafe-oscuro')
 ellipse(im,(x-9,y-1,x+8,y+6),'rojo-oscuro')
 line(im,[(x-5,y),(x+1,y)],'rojo',2)
 rounded(im,(x-8,y+5,x+8,y+9),'ambar','cafe-oscuro',2)
 line(im,[(x-5,y+6),(x+4,y+6)],'crema')
def booth(im,x,z,mat):
 xx,yy=proj(x,z);sc=95/(z+1.6);w=sc*1.25
 rounded(im,(xx-w/2,yy-sc*.7,xx+w/2,yy),'rojo-oscuro' if mat=='rojo-oscuro' else 'verde-oscuro','cafe-oscuro',4)
 line(im,[(xx-w/2+3,yy-sc*.7+2),(xx+w/2-3,yy-sc*.7+2)],'rojo' if mat=='rojo-oscuro' else 'verde')
 for dx in [-.25,.25]:line(im,[(xx+w*dx,yy-sc*.6),(xx+w*dx,yy-4)],'cafe-oscuro')
 rounded(im,(xx-w/2-1,yy-5,xx+w/2+1,yy+1),mat,'cafe-oscuro',3)

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
 for xx in range(-400,721,100):line(im,[(160+(xx-160)*.23,62),(xx,121)],('cafe-oscuro' if n in [1,3,5] else 'noche'))
 for yy in [67,79,101]:line(im,[(0,yy),(319,yy)],('cafe-oscuro' if n in [1,3,5] else 'noche'))
 # Wall dado with small framed artwork; architectural lines remain above the floor.
 rect(im,(28,48,292,60),'cafe-oscuro' if n in [1,3,5] else 'noche')
 line(im,[(28,49),(292,49)],'canela' if n in [1,5] else 'gris-azul')
 for wx in range(32,291,20):line(im,[(wx,52),(wx,59)],'cafe' if n in [1,3,5] else 'pizarra')
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
 rect(im,(0,0,319,3),'cafe-oscuro' if n in [1,3,5] else 'noche')
 line(im,[(0,1),(319,1)],'canela' if n in [1,3,5] else 'gris')
 line(im,[(0,4),(319,4)],'cafe' if n in [1,3,5] else 'pizarra')
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
out=Image.new('RGB',(2048,1610),c('negro'));text(out,(40,25),'COMEDORES / DIRECCIÓN CARTOON',34,'crema');text(out,(40,74),'Formas redondeadas · muebles robustos · sombreado por material · píxel ×3',22)
for n,(name,desc,bname) in enumerate(NAMES,1):
 x=40+(n-1)%2*1000;y=128+(n-1)//2*475
 text(out,(x,y),f'F{n:02}  {name}',27,'crema');text(out,(x,y+36),desc,20)
 out.paste(interior(n).resize((960,366),Image.Resampling.NEAREST),(x,y+72))
text(out,(40,1570),'Los objetos más pequeños están al fondo; el pasillo llega hasta el mostrador. Sin interfaz superpuesta.',19)
out.save(ROOT/'interiors-six-options.png')
out=Image.new('RGB',(2048,2240),c('negro'));text(out,(40,25),'BARRAS / VOLUMEN Y CONTORNOS',34,'crema');text(out,(40,74),'Superficies de trabajo horizontales · sprites finales intactos · píxel ×3',22)
for n,(name,desc,bname) in enumerate(NAMES,1):
 x=40+(n-1)%2*1000;y=130+(n-1)//2*690
 text(out,(x,y),f'B{n:02}  {bname} + F{n:02}',27,'crema');text(out,(x,y+36),name,20)
 out.paste(scene(n).resize((960,600),Image.Resampling.NEAREST),(x,y+72))
text(out,(40,2208),'Mismas posiciones del juego. Sin comanda ni globo para comparar el espacio; su composición queda pendiente.',18)
out.save(ROOT/'bars-six-pairs.png')
allowed={tuple(bytes.fromhex(v[1:])) for v in P.values()}
for p in ROOT.glob('*-1x.png'):assert set(Image.open(p).getdata())<=allowed,p
print('18 native PNGs + 2 sheets; palette verified.')
