"""Isolated proposals; consumes exact resolved game matrices, never writes game assets.
Run after exporting source-sprites.json using the project's resolveSprite function.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'source-sprites.json').read_text()); P=DATA['palette']; S=DATA['sprites']
def rgb(c): return P.get(c,c)
def rect(im,box,c): ImageDraw.Draw(im).rectangle(box,fill=rgb(c))
def line(im,points,c,w=1): ImageDraw.Draw(im).line(points,fill=rgb(c),width=w)
def sprite(im,key,x,y):
 s=S[key]; tile=Image.new('RGBA',(s['width'],s['height']))
 for j,row in enumerate(s['frames'][0]):
  for i,c in enumerate(row):
   if c!='.': tile.putpixel((i,j),tuple(bytes.fromhex(P[s['colors'][c]][1:]))+(255,))
 im.paste(tile,(x,y),tile)
def tiles(im,y0,y1,base,seam,light,w=20,h=10):
 rect(im,(0,y0,319,y1),base)
 for y in range(y0,y1,h):
  line(im,[(0,y),(319,y)],seam)
  for x in range(-w,340,w):
   xx=x+(w//2 if ((y-y0)//h)%2 else 0)
   line(im,[(xx,y),(xx,y+h-1)],seam)
   line(im,[(xx+1,y+1),(xx+w-1,y+1)],light)
def shelf(im,x,y,w):
 rect(im,(x,y,x+w,y+3),'pizarra'); line(im,[(x,y),(x+w,y)],'gris-azul')
 for xx in [x+5,x+w-7]: rect(im,(xx,y+4,xx+2,y+10),'noche')
def jar(im,x,y,c):
 rect(im,(x,y,x+6,y+10),'noche');rect(im,(x+1,y+2,x+5,y+8),c);line(im,[(x+1,y),(x+5,y)],'gris-azul')
def hood(im,x=110,y=15):
 rect(im,(x+36,0,x+64,y+12),'noche');rect(im,(x+37,0,x+38,y+12),'pizarra')
 ImageDraw.Draw(im).polygon([(x+17,y),(x+83,y),(x+100,y+21),(x,y+21)], fill=rgb('pizarra'))
 line(im,[(x+17,y),(x+83,y)],'gris-azul'); rect(im,(x,y+22,x+100,y+28),'noche')
 for xx in range(x+9,x+93,5):line(im,[(xx,y+24),(xx,y+26)],'negro')
def kitchen(n):
 im=Image.new('RGB',(320,200),rgb('noche'))
 if n==1:
  tiles(im,0,121,'noche','negro','pizarra',24,10);hood(im)
  shelf(im,8,19,64);shelf(im,248,19,64)
  for x,c in [(13,'cafe'),(25,'verde-noche'),(255,'cafe'),(267,'pizarra'),(283,'verde-noche')]:jar(im,x,8,c)
 elif n==2:
  tiles(im,0,121,'cafe-oscuro','negro','cafe',22,9); hood(im)
  rect(im,(0,77,319,121),'noche');line(im,[(0,77),(319,77)],'pizarra')
  for x in [9,253]:
   rect(im,(x,8,x+56,25),'negro');rect(im,(x+2,10,x+54,23),'verde-noche')
   for a in range(x+8,x+49,10):line(im,[(a,14),(a+5,14)],'pizarra')
 elif n==3:
  tiles(im,0,121,'verde-noche','negro','verde-oscuro',16,16)
  rect(im,(86,5,234,34),'negro');rect(im,(89,8,231,31),'noche')
  for x in range(96,229,12):line(im,[(x,12),(x,27)],'pizarra')
  shelf(im,6,22,64);shelf(im,250,22,64)
  for x in [14,26,265,280,295]:jar(im,x,11,'cafe-oscuro')
 elif n==4:
  rect(im,(0,0,319,121),'pizarra')
  for x in range(0,320,40):
   line(im,[(x,0),(x,121)],'noche');line(im,[(x+1,0),(x+1,121)],'gris-azul')
  hood(im,110,12)
  for x in [7,252]:
   rect(im,(x,8,x+59,25),'noche');line(im,[(x+2,10),(x+57,10)],'gris-azul')
   for xx in range(x+7,x+54,8): line(im,[(xx,13),(xx,22)],'pizarra')
 elif n==5:
  tiles(im,0,121,'noche','negro','pizarra',32,16)
  rect(im,(89,0,231,36),'cafe-oscuro');rect(im,(92,0,228,33),'noche')
  for x in [94,138,182,226]:rect(im,(x,0,x+2,34),'cafe')
  for x in [96,141,186]:
   rect(im,(x,22,x+36,30),'pizarra');line(im,[(x,22),(x+36,22)],'gris-azul')
  shelf(im,7,20,61);shelf(im,252,20,61)
  for x in [14,28,263,279,294]:jar(im,x,9,'verde-noche')
 elif n==6:
  rect(im,(0,0,319,121),'noche');tiles(im,75,121,'noche','negro','pizarra',20,10)
  for x in [6,251]:
   rect(im,(x,5,x+62,28),'cafe-oscuro');rect(im,(x+2,7,x+60,26),'negro')
   line(im,[(x+8,12),(x+53,12)],'rojo-oscuro');line(im,[(x+11,16),(x+49,16)],'cafe')
  hood(im,110,12)
  line(im,[(0,73),(319,73)],'rojo-oscuro');line(im,[(0,74),(319,74)],'cafe-oscuro')
 return im

def counter(im,n):
 y=122
 bases={1:'cafe',2:'gris-azul',3:'pizarra',4:'verde-noche',5:'noche',6:'cafe-oscuro'}
 rect(im,(0,y,319,199),bases[n]);line(im,[(0,y),(319,y)],'negro')
 if n==1:
  for yy in [123,142,161,180]:
   line(im,[(0,yy),(319,yy)],'canela');line(im,[(0,yy+17),(319,yy+17)],'cafe-oscuro')
   for x in range(8,320,47): line(im,[(x,yy+7),(x+12,yy+7)],'cafe-oscuro')
 elif n==2:
  for yy in [123,125,158,195]:line(im,[(0,yy),(319,yy)],'gris')
  for x in [0,79,239,319]:line(im,[(x,126),(x,197)],'pizarra')
  for x in [7,311]:
   for yy in [129,190]:rect(im,(x,yy,x+1,yy+1),'gris-claro')
 elif n==3:
  tiles(im,123,199,'pizarra','noche','gris-azul',24,12)
  line(im,[(0,124),(319,124)],'gris')
 elif n==4:
  for x in range(0,320,32):line(im,[(x,123),(x,198)],'negro');line(im,[(x+1,124),(x+1,197)],'verde-oscuro')
  for yy in [124,197]:line(im,[(0,yy),(319,yy)],'cafe');line(im,[(0,yy+1),(319,yy+1)],'canela')
 elif n==5:
  for x in range(5,320,53):
   line(im,[(x,134),(x+7,136),(x+12,142)],'pizarra')
   line(im,[(x+24,184),(x+32,181),(x+40,181)],'pizarra')
  line(im,[(0,124),(319,124)],'gris-azul');line(im,[(0,197),(319,197)],'pizarra')
 elif n==6:
  rect(im,(0,124,319,129),'cafe');line(im,[(0,124),(319,124)],'canela')
  for x in range(0,320,16):
   rect(im,(x+2,132,x+13,197),'cafe');line(im,[(x+2,133),(x+2,196)],'canela')
   line(im,[(x+6,137),(x+6,194)],'cafe-oscuro')
 line(im,[(0,199),(319,199)],'negro')

def context(im):
 # Same final sprites, exact horizontal game positions and integer scale in every candidate.
 sprite(im,'cliente:azul',136,46)
 # Counter masks customer's waist, as in game.
 rect(im,(136,122,183,125),im.getpixel((135,123)))
 sprite(im,'plato',145,120)
 for key,x in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:sprite(im,key,x,103)
 for key,x in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:sprite(im,key,x,139)
 sprite(im,'plancha',82,165);sprite(im,'charola',244,165);sprite(im,'basura',40,170)
 for x in [97,135]:sprite(im,'carne:perfecta',x,168)
 # Fixed neutral UI silhouettes mark protected reading areas.
 rect(im,(8,30,67,118),'crema');line(im,[(10,31),(65,31)],'blanco')
 for yy,w in [(42,32),(47,42),(61,31),(66,37),(80,40),(85,26)]:rect(im,(16,yy,16+w,yy+1),'cafe')
 rect(im,(192,30,307,67),'gris-claro');rect(im,(193,31,306,66),'blanco')
 for yy,w in [(41,76),(47,88),(53,54)]:rect(im,(201,yy,201+w,yy+1),'gris-azul')
 line(im,[(140,41),(179,41)],'verde-oscuro',3)
 # Reference stack is the original sprite set.
 for key,x,y in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:sprite(im,key,x,y)
 return im

BARS=[('Roble de parrilla','Tablones anchos / cálido y familiar'),('Acero cepillado','Panel continuo / cocina profesional'),('Cerámica azul','Juntas finas / diner artesanal'),('Esmalte verde','Módulos verticales / borde de madera'),('Piedra grafito','Veta discreta / máxima calma visual'),('Nogal acanalado','Listones profundos / carácter de cantina')]
BACKS=[('Brasserie azul','Azulejo oscuro, campana y repisas'),('Ladrillo ahumado','Mampostería cálida y zócalo oscuro'),('Despensa verde','Cerámica verde y ventilación corrida'),('Cocina de acero','Paneles industriales y campana central'),('Ventana al obrador','Pasaplatos profundo y repisas laterales'),('Diner nocturno','Franja burdeos y rótulos contenidos')]
fontpath='/System/Library/Fonts/Supplemental/Arial.ttf'
def font(sz):return ImageFont.truetype(fontpath,sz)
def sheet(kind,names):
 out=Image.new('RGB',(2048,2240),rgb('negro'));d=ImageDraw.Draw(out)
 d.text((40,28),'BARRAS / 06 MATERIALES' if kind=='bars' else 'COCINAS / 06 AMBIENTES',font=font(34),fill=rgb('crema'))
 d.text((40,77),'PROPUESTAS · Endesga 32 · píxel ×3 · objetos finales sin cambios',font=font(21),fill=rgb('gris'))
 for n,(name,desc) in enumerate(names,1):
  x=40+((n-1)%2)*1000;y=132+((n-1)//2)*690
  d.text((x,y),f'{"B" if kind=="bars" else "F"}{n:02}  {name}',font=font(28),fill=rgb('crema'))
  d.text((x,y+37),desc,font=font(20),fill=rgb('gris'))
  im=kitchen(1 if kind=='bars' else n);counter(im,n if kind=='bars' else 1)
  raw=im.copy();raw.save(ROOT/f'{kind}-{n:02}-environment-1x.png')
  context(im);im.save(ROOT/f'{kind}-{n:02}-context-1x.png')
  out.paste(im.resize((960,600),Image.Resampling.NEAREST),(x,y+74))
 d.text((40,2210),'Misma escena de comparación. Comanda y globo: reservas de lectura, no interfaz final.',font=font(18),fill=rgb('gris'))
 out.save(ROOT/f'{kind}-six-options.png')
sheet('bars',BARS);sheet('backgrounds',BACKS)
# Validate palette on all logical pixels; sheet typography intentionally uses antialiasing.
allowed={tuple(bytes.fromhex(v[1:])) for v in P.values()}
for p in ROOT.glob('*-1x.png'):
 im=Image.open(p);assert set(im.getdata()) <= allowed,p
print('Created 2 sheets, 12 clean environments and 12 contextual scenes; all logical pixels are Endesga 32.')
