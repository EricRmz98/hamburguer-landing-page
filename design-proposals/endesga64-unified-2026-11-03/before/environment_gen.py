"""Generate the Resurrect 64 diner: native cells, warm enamel, upholstery and polished concrete.
Requires Pillow. Run from any directory: python3 scripts/sprites/environment_gen.py
"""
from pathlib import Path
from PIL import Image, ImageDraw
import re, json
ROOT=Path(__file__).resolve().parents[2]
P={}
for a,b,h in re.findall(r"(?:'([^']+)'|([\w-]+)):\s*'(#[0-9a-f]{6})'",(ROOT/'src/game/sprites/palette.ts').read_text()):P[a or b]=h
def c(v):return P.get(v,v)

def rect(im,b,col):ImageDraw.Draw(im).rectangle(tuple(round(v) for v in b),fill=c(col))

def poly(im,pts,col):ImageDraw.Draw(im).polygon([(round(x),round(y)) for x,y in pts],fill=c(col))

def line(im,pts,col,w=1):ImageDraw.Draw(im).line([(round(x),round(y)) for x,y in pts],fill=c(col),width=w)

def rounded(im,box,fill,outline,r=3):
 box=tuple(round(v) for v in box)
 ImageDraw.Draw(im).rounded_rectangle(box,radius=r,fill=c(fill),outline=c(outline),width=1)

def ellipse(im,box,fill):ImageDraw.Draw(im).ellipse(tuple(round(v) for v in box),fill=c(fill))

def grain(im,box,base,shade,light,salt=0,density=26):
 # Sparse two-pixel clusters on a material mask, not uniform dithering over the scene.
 before=im.copy();rgb=tuple(bytes.fromhex(c(base)[1:]))
 l,t,r,b=map(round,box)
 for y in range(max(0,t),min(b,im.height)):
  for x in range(max(0,l),min(r,im.width)):
   h=((x*73856093)^(y*19349663)^(salt*83492791))%1000
   if h<density and before.getpixel((x,y))==rgb:
    color=light if (x+y+salt)%3 else shade
    rect(im,(x,y,x+1,y),color)

def door(im,x,w,night=False):
 # Taller doorway brings the wall toward the player without scaling its pixel language.
 rounded(im,(x-4,6,x+w+4,89),'cafe','cafe-oscuro',6)
 line(im,[(x-1,13),(x-1,83)],'canela',2)
 rounded(im,(x+2,10,x+w-2,84),'gris-azul','cafe-oscuro',4)
 rounded(im,(x+4,12,x+w-4,69),'azul-oscuro' if night else 'gris','noche',3)
 rect(im,(x+5,45,x+w-5,66),'noche' if night else 'pizarra')
 for xx in range(x+7,x+w-6,9):rect(im,(xx,51,xx+3,56),'ambar' if night else 'gris-azul')
 line(im,[(x+7,34),(x+w-8,19)],'gris-claro',2)
 rounded(im,(x+w-9,53,x+w-6,62),'crema','cafe-oscuro',1)
 rounded(im,(x+7,74,x+w-7,81),'canela','cafe-oscuro',2)
 poly(im,[(x-3,89),(x+w+3,89),(x+w+7,94),(x-7,94)],'cafe-oscuro')
 line(im,[(x-1,90),(x+w+1,90)],'canela')
 line(im,[(x+w/2,26),(x+w/2-6,32),(x+w/2+6,32),(x+w/2,26)],'cafe-oscuro')
 rounded(im,(x+w/2-7,32,x+w/2+7,37),'crema','cafe-oscuro',1)
 line(im,[(x+w/2-4,34),(x+w/2+4,34)],'cafe')

def window(im,x,w):
 rounded(im,(x-2,13,x+w+2,46),'cafe','cafe-oscuro',5)
 rounded(im,(x+1,15,x+w-1,42),'gris-azul','noche',4)
 rect(im,(x+3,32,x+w-3,40),'pizarra')
 line(im,[(x+6,27),(x+w-7,18)],'gris',2)
 rect(im,(x+w/2-1,16,x+w/2+1,42),'cafe-oscuro')
 rounded(im,(x-4,43,x+w+4,48),'canela','cafe-oscuro',2)
 line(im,[(x-1,44),(x+w+1,44)],'durazno')
 # Reflected light sits in short patches instead of a single hard staircase.
 line(im,[(x+6,20),(x+6,31)],'gris')
 line(im,[(x+8,19),(x+w/2-5,19)],'gris-claro')
 line(im,[(x+w/2+5,37),(x+w-8,37)],'gris-azul')

def plant(im,x,y,s=1):
 rounded(im,(x-5,y-8,x+5,y),'canela','cafe-oscuro',3)
 line(im,[(x-3,y-7),(x+2,y-7)],'durazno')
 for dx,dy in [(-4,-15),(4,-16),(0,-20),(-6,-11),(6,-10)]:
  ellipse(im,(x+dx-4,y+dy-4,x+dx+4,y+dy+3),'verde-noche')
  ellipse(im,(x+dx-3,y+dy-4,x+dx+2,y+dy),'verde-oscuro')
  line(im,[(x+dx-1,y+dy-3),(x+dx+1,y+dy-3)],'lima')
  line(im,[(x+dx,y+dy-2),(x+dx+2,y+dy-1)],'salvia-oscura')
 line(im,[(x-3,y-5),(x-3,y-1)],'piel')
 line(im,[(x-2,y),(x+3,y)],'oxido')

def lamp(im,x,y):
 line(im,[(x,0),(x,y)],'cafe-oscuro',2)
 ellipse(im,(x-10,y-1,x+10,y+9),'cafe-oscuro')
 ellipse(im,(x-9,y-1,x+8,y+6),'rojo-oscuro')
 line(im,[(x-5,y),(x+1,y)],'rojo',2)
 rounded(im,(x-8,y+5,x+8,y+9),'ambar','cafe-oscuro',2)
 line(im,[(x-5,y+6),(x+4,y+6)],'crema')

def red_architecture(im,fn,*args,offset=0):
 layer=Image.new('RGB',im.size,c('alerta'));fn(layer,*args)
 mapping={c('cafe'):c('rojo-ladrillo'),c('canela'):c('rojo'),c('durazno'):c('coral'),c('cafe-oscuro'):c('rojo-oscuro')}
 for y in range(im.height-offset):
  for x in range(im.width):
   col=layer.getpixel((x,y));hx='#%02x%02x%02x'%col
   if hx!=c('alerta'):im.putpixel((x,y+offset),tuple(bytes.fromhex(mapping.get(hx,hx)[1:])))

def wall_counter(im,left,right,y,floor):
 # Both depth edges converge toward the screen centre; the front edge stays horizontal.
 centre=im.width/2
 back_left=left+(centre-left)*.05
 back_right=right+(centre-right)*.05
 # Load-bearing legs reach the floor, with a small foot and a contact shadow.
 for x in [left+10,right-10]:
  ellipse(im,(x-4,floor,x+4,floor+3),'pizarra')
  rect(im,(x-1,y+3,x+2,floor+1),'pizarra')
  line(im,[(x,y+5),(x,floor)],'gris-azul')
  line(im,[(x-2,floor+1),(x+3,floor+1)],'noche')
 poly(im,[(left,y),(right,y),(right,y+4),(left,y+4)],'gris-claro')
 poly(im,[(left,y),(back_left,y-5),(back_right,y-5),(right,y)],'blanco')
 # Both end faces show their own shaded thickness.
 poly(im,[(left,y),(back_left,y-5),(back_left,y-1),(left,y+4)],'gris')
 poly(im,[(right,y),(back_right,y-5),(back_right,y-1),(right,y+4)],'gris')
 line(im,[(left,y),(back_left,y-5),(back_right,y-5),(right,y),(right,y+4),(left,y+4),(left,y)],'gris-azul')
 line(im,[(left+2,y+1),(right-1,y+1)],'blanco')
 line(im,[(left+6,y+3),(right-6,y+3)],'arena')

def rear_chair(im,x,top):
 # Opposite views on either side of the screen centre, preserving the rounded chair model.
 direction=1 if x<im.width/2 else -1
 def point(dx,dz,height):return (x+dx+direction*.5*dz,top+35-.96*height-.43*dz)
 def sidepoint(dx,dy):return (x+direction*dx,top+dy)
 def prism(x0,x1,z0,z1,h0,h1,top_color,front,side):
  a,b,cc,dd=[point(dx,dz,h1) for dx,dz in [(x0,z1),(x1,z1),(x1,z0),(x0,z0)]]
  ba,bb,bc,bd=[point(dx,dz,h0) for dx,dz in [(x0,z1),(x1,z1),(x1,z0),(x0,z0)]]
  poly(im,[a,dd,bd,ba] if direction>0 else [b,cc,bc,bb],side)
  poly(im,[dd,cc,bc,bd],front);poly(im,[a,b,cc,dd],top_color)
  line(im,[a,b,cc,bc,bd,dd,a],'cafe-oscuro' if front=='rojo-oscuro' else 'noche')
  line(im,[dd,cc],'rojo' if top_color=='rojo' else 'gris-azul')
 # Derive shadow bounds from the four actual ground contacts, not the chair's nominal x.
 feet=[point(dx,depth,0) for dx in [-5,5] for depth in [1,9]]
 cx=sum(pt[0] for pt in feet)/4;cy=sum(pt[1] for pt in feet)/4
 half_w=max(abs(pt[0]-cx) for pt in feet)+3
 half_h=max(abs(pt[1]-cy) for pt in feet)+1.5
 ellipse(im,(cx-half_w,cy-half_h,cx+half_w,cy+half_h),'pizarra')
 for fx,fy in feet:ellipse(im,(fx-1,fy-1,fx+1,fy+1),'noche')
 # Far pair first, near pair last, so no invented crossing of legs.
 for depth in [9,1]:
  for dx in [-5,5]:
   prism(dx-1,dx+1,depth-.8,depth+.8,0,17,'gris-azul','noche','pizarra')
   line(im,[point(dx,depth,1),point(dx,depth,14)],'gris-azul')
 line(im,[point(-5,1,7),point(5,1,7)],'gris')
 line(im,[point(-5*direction,1,7),point(-5*direction,9,7)],'gris-azul')
 # Recover the approved soft, rounded upholstery instead of a new box-shaped model.
 # Only the far edge adds depth; the visible padded face retains its original silhouette.
 poly(im,[sidepoint(dx,dy) for dx,dy in [(-7,14),(-2,10),(12,10),(8,18)]],'rojo')
 poly(im,[sidepoint(dx,dy) for dx,dy in [(8,14),(12,10),(12,15),(8,19)]],'cafe-oscuro')
 rounded(im,(x-8,top+14,x+8,top+19),'rojo-oscuro','cafe-oscuro',2)
 line(im,[(x-6,top+15),(x+6,top+15)],'rojo')
 # Narrow rounded side, then the same face, corner radius, seam and highlights as before.
 side_left,side_right=sorted([x-direction*5,x+direction*9])
 rounded(im,(side_left,top-1,side_right,top+15),'cafe-oscuro','cafe-oscuro',3)
 line(im,[sidepoint(-2,0),sidepoint(6,0)],'rojo')
 rounded(im,(x-7,top,x+7,top+16),'rojo-oscuro','cafe-oscuro',3)
 line(im,[(x-4,top+1),(x+3,top+1)],'rojo')
 line(im,[(x-6,top+4),(x-6,top+11)],'rojo')
 line(im,[(x-4,top+13),(x+4,top+13)],'cafe')
 # Padded inset, a fine seam and a broad top-left highlight, at the same pixel size as the cast.
 line(im,[(x-4,top+3),(x+3,top+3)],'rojo-ladrillo')
 line(im,[(x-4,top+4),(x-4,top+10)],'rojo-ladrillo')
 line(im,[(x-3,top+11),(x+3,top+11)],'rojo-ladrillo')

def dining_horizontal():
 im=Image.new('RGB',(320,122),c('gris-azul'))
 rect(im,(0,0,319,101),'gris-claro')
 for x in [119,211]:
  rect(im,(x,0,x+2,101),'pizarra');line(im,[(x,0),(x,100)],'gris-azul')
 rect(im,(0,0,319,4),'noche');line(im,[(0,5),(319,5)],'gris')
 line(im,[(24,9),(288,9),(288,24)],'gris-azul',2)
 rect(im,(0,53,319,101),'rojo-oscuro');line(im,[(0,53),(319,53)],'blanco',2)
 rect(im,(0,102,319,121),'gris-azul')
 line(im,[(0,102),(319,102)],'pizarra')
 line(im,[(0,114),(319,114)],'pizarra')
 line(im,[(42,105),(64,105)],'gris');line(im,[(270,103),(288,103)],'gris')
 grain(im,(0,6,320,52),'gris-claro','gris','gris-claro',12,3)
 grain(im,(0,56,320,101),'rojo-oscuro','cafe-oscuro','rojo-ladrillo',19,3)
 grain(im,(0,103,320,122),'gris-azul','pizarra','gris',24,3)
 red_architecture(im,door,241,40,offset=11)
 red_architecture(im,window,45,69,offset=5);red_architecture(im,window,135,68,offset=5)
 lamp(im,75,18);lamp(im,174,18)
 wall_counter(im,35,217,69,102)
 for x in [79,137,195]:rear_chair(im,x,73)
 plant(im,301,104)
 return im

def red_bar():
 im=Image.new('RGB',(320,78),c('carmesi'))
 # Equal aligned tiles; only horizontal and vertical joints, matching equipment axes.
 for y in range(4,72,17):
  for x in range(0,320,32):
   rect(im,(x,y,x+31,min(y+16,72)),'cafe-oscuro')
   rect(im,(x+1,y+1,x+30,min(y+15,71)),'carmesi')
   line(im,[(x+2,y+1),(x+29,y+1)],'alerta')
   line(im,[(x+1,y+2),(x+1,min(y+13,70))],'rojo-ladrillo')
   line(im,[(x+3,min(y+14,70)),(x+29,min(y+14,70))],'rojo-oscuro')
   line(im,[(x+29,y+3),(x+29,min(y+13,70))],'rojo-oscuro')
   if y<65 and (x//32+y//17)%3!=1:
    line(im,[(x+4,y+3),(x+8,y+3)],'rojo-ladrillo')
 rect(im,(0,0,319,3),'cafe-oscuro');line(im,[(0,1),(319,1)],'rojo')
 rect(im,(0,73,319,77),'cafe-oscuro');line(im,[(0,73),(319,73)],'rojo')
 return im

def dining_vertical():
 im=Image.new('RGB',(180,200),c('gris-azul'))
 rect(im,(0,0,179,159),'gris-claro')
 for x in [99]:
  rect(im,(x,0,x+2,159),'pizarra');line(im,[(x,0),(x,158)],'gris-azul')
 rect(im,(0,0,179,4),'noche');line(im,[(15,26),(163,26),(163,47)],'gris-azul',2)
 rect(im,(0,109,179,159),'rojo-oscuro');line(im,[(0,109),(179,109)],'blanco',2)
 rect(im,(0,160,179,199),'gris-azul');line(im,[(0,160),(179,160)],'pizarra')
 line(im,[(0,184),(179,184)],'pizarra')
 line(im,[(16,168),(35,168)],'gris');line(im,[(142,175),(159,175)],'gris')
 grain(im,(0,6,180,108),'gris-claro','gris','gris-claro',12,3)
 grain(im,(0,112,180,159),'rojo-oscuro','cafe-oscuro','rojo-ladrillo',19,3)
 grain(im,(0,161,180,200),'gris-azul','pizarra','gris',24,3)
 red_architecture(im,door,129,30,offset=68)
 red_architecture(im,window,21,66,offset=60)
 architecture=Image.new('RGB',(180,200),c('alerta'));lamp(architecture,52,10)
 # Lamp translated with the window while retaining its suspension from the ceiling.
 line(im,[(52,0),(52,71)],'cafe-oscuro',2)
 for y in range(9,21):
  for x in range(41,64):
   color=architecture.getpixel((x,y))
   if color!=tuple(bytes.fromhex(c('alerta')[1:])):im.putpixel((x,y+60),color)
 wall_counter(im,17,112,121,160)
 for x in [58,100]:rear_chair(im,x,125)
 return im

def write_sprite(name,id,im,materials,reason):
 reverse={tuple(bytes.fromhex(h[1:])):name for name,h in P.items()}
 letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#'
 used=sorted(set(im.getdata()));colors={letters[i]:reverse[rgb] for i,rgb in enumerate(used)}
 lookup={rgb:letters[i] for i,rgb in enumerate(used)}
 rows=[''.join(lookup[im.getpixel((x,y))] for x in range(im.width)) for y in range(im.height)]
 return f"export const {name} = defineSprite({{\n  id: '{id}',\n  size: [{im.width}, {im.height}],\n  materials: {json.dumps(materials)},\n  lint: {{ light: false, reason: {json.dumps(reason,ensure_ascii=False)} }},\n  colors: {json.dumps(colors,ensure_ascii=False)},\n  pixels: `\n"+'\n'.join('    '+row for row in rows)+"\n  `,\n});\n"

if __name__=='__main__':
 horizontal=dining_horizontal();vertical=dining_vertical();counter=red_bar()
 # The vertical counter gets two extra rows of its dark front lip, not stretched pixels.
 counter_v=Image.new('RGB',(180,80),c('cafe-oscuro'));counter_v.paste(counter.crop((0,0,180,78)),(0,0))
 materials=['metal','ceramica','pared','ropa-roja','madera','acento','etiqueta','lechuga','mayonesa']
 reason='Escena con múltiples objetos a distintas profundidades; la luz se evalúa en cada mueble, no por el centroide global del color.'
 text="// Generated by scripts/sprites/environment_gen.py. Edit the generator, not these matrices.\nimport { defineSprite } from './define.ts';\n\n"
 for name,id,im in [('comedor','comedor',horizontal),('comedorVertical','comedor_v',vertical)]:text+=write_sprite(name,id,im,materials,reason)+'\n'
 for name,id,im in [('barraRoja','barra_roja',counter),('barraRojaVertical','barra_roja_v',counter_v)]:text+=write_sprite(name,id,im,['azulejo-rojo'],'Superficie modular repetida: cada baldosa recibe luz arriba y a la izquierda.')+'\n'
 (ROOT/'src/game/sprites/environment.ts').write_text(text)
 preview=ROOT/'design-proposals/applied-environment';preview.mkdir(exist_ok=True)
 horizontal.resize((1280,488),Image.Resampling.NEAREST).save(preview/'horizontal.png')
 vertical.resize((540,600),Image.Resampling.NEAREST).save(preview/'vertical.png')
 print('Generated 4 native scene sprites and horizontal/vertical previews.')
