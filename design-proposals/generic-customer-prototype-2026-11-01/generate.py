"""Reference-only, native pixel prototype inspired by the user's smooth white figures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import json, math

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'scene-source.json').read_text())
P=DATA['palette'];SIZE=(80,112);CX=40;WAIST=108
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'

def color(name):return tuple(bytes.fromhex(P[name][1:]))+(255,)
def text(im,xy,label,size=22,ink='gris-claro'):
 ImageDraw.Draw(im).text(xy,label,font=ImageFont.truetype(FONT,size),fill=P[ink])

def empty():return Image.new('L',SIZE)
def outline(im,mask,ink='gris'):
 im.paste(color(ink),(0,0),mask.filter(ImageFilter.MaxFilter(3)))

def white_surface(im,mask,normal):
 for y in range(SIZE[1]):
  for x in range(SIZE[0]):
   if not mask.getpixel((x,y)):continue
   nx,ny,nz=normal(x,y)
   light=-.50*nx-.50*ny+.72*nz
   ink='blanco' if light>.62 else 'gris-claro' if light>.06 else 'gris'
   im.putpixel((x,y),color(ink))

def prototype():
 im=Image.new('RGBA',SIZE);parts=[]
 # The shoulders and wrists follow one bowed centreline: no elbow ball or segmentation.
 for side in [-1,1]:
  mask=empty()
  def centre(y):
   t=max(0,min(1,(y-53)/49));return CX+side*(22+5*math.sin(t*math.pi*.9))
  def radius(y):return 6-.9*max(0,min(1,(y-53)/49))
  for y in range(47,108):
   cy=max(53,min(102,y));r=radius(cy);xx=centre(cy)
   for x in range(80):
    if (x-xx)**2+(y-cy)**2<=r*r:mask.putpixel((x,y),255)
  def normal(x,y):
   cy=max(53,min(102,y));r=radius(cy);nx=(x-centre(cy))/r;ny=(y-cy)/r
   return nx,ny,math.sqrt(max(0,1-nx*nx-ny*ny))
  white_surface(im,mask,normal);parts.append(mask)
 # Short neck joins the smooth head and sloping shoulders.
 neck=empty();ImageDraw.Draw(neck).rounded_rectangle((34,31,46,51),radius=5,fill=255)
 im.paste(color('gris-claro'),(0,0),neck);parts.append(neck)
 torso=empty()
 profile=[(43,7),(45,13),(48,22),(52,23),(58,23),(67,23),(84,21),(100,20),(111,21)]
 widths={}
 for (y0,w0),(y1,w1) in zip(profile,profile[1:]):
  for y in range(y0,y1+1):
   half=w0+(w1-w0)*(y-y0)/(y1-y0);widths[y]=half
   ImageDraw.Draw(torso).line([(round(CX-half),y),(round(CX+half),y)],fill=255)
 def chest_normal(x,y):
  nx=(x-CX)/widths[y];ny=-.3*max(0,(58-y)/15)
  return nx,ny,math.sqrt(max(0,1-nx*nx-ny*ny))
 white_surface(im,torso,chest_normal);parts.append(torso)
 # Ovoid, featureless head. No ears, facial marks, hair, clothing or accessories.
 head=empty();ImageDraw.Draw(head).ellipse((24,4,56,39),fill=255)
 outline(im,head)
 def head_normal(x,y):
  nx=(x-CX)/16;ny=(y-21.5)/17.5
  return nx,ny,math.sqrt(max(0,1-nx*nx-ny*ny))
 white_surface(im,head,head_normal);parts.append(head)
 # A single selective outline around the complete silhouette; internal joins remain light.
 whole=empty()
 for mask in parts:whole=ImageChops.lighter(whole,mask)
 out=Image.new('RGBA',SIZE);outline(out,whole,'gris-azul');out.alpha_composite(im)
 # Keep the last row transparent; the working waist lies four rows above the frame end.
 ImageDraw.Draw(out).rectangle((0,111,79,111),fill=(0,0,0,0))
 return out

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
 person=prototype();pos=(l['w']//2-CX,l['counter'][1]-WAIST)
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

def review_board():
 out=Image.new('RGB',(1460,1048),P['negro'])
 text(out,(28,20),'PERSONAJE GENÉRICO / PRUEBA',32,'crema')
 text(out,(28,69),'Figura sin rostro · formas suaves · proporción con el local',21)
 text(out,(28,121),'SPRITE',22,'crema')
 bg=Image.new('RGB',(368,488),P['noche']);im=prototype().resize((320,448),Image.Resampling.NEAREST)
 bg.paste(im,(24,18),im);out.paste(bg,(28,160))
 text(out,(28,675),'Cabeza lisa y ovalada',21,'crema')
 text(out,(28,708),'Brazos sin cortes en el codo',20)
 text(out,(28,741),'Sin ropa ni accesorios',20)
 text(out,(430,121),'DENTRO DEL ESCENARIO',22,'crema')
 im=scene().resize((960,600),Image.Resampling.NEAREST);out.paste(im,(430,160),im)
 text(out,(430,788),'Cuerpo más ancho que el plato; cintura apoyada en la barra.',21,'crema')
 text(out,(28,855),'PROPORCIÓN / MISMA ESCALA',22,'crema')
 comparison=Image.new('RGB',(368,128),P['noche'])
 small=prototype();comparison.paste(small,(27,8),small)
 plate=sprite('plato');comparison.paste(plate,(157,81),plate)
 text(comparison,(204,28),'Figura y plato',17)
 text(comparison,(204,52),'sin ampliar',17)
 out.paste(comparison,(28,894))
 text(out,(430,858),'Referencia para revisar el estilo y la escala.',21)
 text(out,(430,893),'El juego conserva los clientes actuales.',20)
 out.save(ROOT/'prototype-review.png')

def export():
 im=prototype();allowed={color(name) for name in ['gris-azul','gris','gris-claro','blanco']}
 assert all(not p[3] or p in allowed for p in im.getdata())
 assert all(p[3] in [0,255] for p in im.getdata())
 assert im.getbbox()[0]>0 and im.getbbox()[2]<80
 opaque={(x,y) for y in range(112) for x in range(80) if im.getpixel((x,y))[3]}
 todo=[next(iter(opaque))];connected=set(todo)
 while todo:
  x,y=todo.pop()
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   q=(x+dx,y+dy)
   if q in opaque and q not in connected:connected.add(q);todo.append(q)
 assert connected==opaque
 im.save(ROOT/'generic-customer-1x.png')
 im.resize((480,672),Image.Resampling.NEAREST).save(ROOT/'generic-customer-6x.png')
 for orientation in ['horizontal','vertical']:
  scene(orientation).resize((DATA['layouts'][orientation]['w']*4,DATA['layouts'][orientation]['h']*4),Image.Resampling.NEAREST).save(ROOT/f'prototype-{orientation}.png')
 scene('horizontal',False).resize((1280,800),Image.Resampling.NEAREST).save(ROOT/'prototype-empty-plate.png')
 letters={'gris-azul':'o','gris':'s','gris-claro':'b','blanco':'h'}
 pixels=[''.join('.' if not im.getpixel((x,y))[3] else letters[next(name for name in letters if color(name)==im.getpixel((x,y)))] for x in range(80)) for y in range(112)]
 definition={'id':'cliente_generico_prueba','size':[80,112],'colors':{v:k for k,v in letters.items()},'pixels':'\n'.join(pixels),'waist':WAIST}
 (ROOT/'sprite.json').write_text(json.dumps(definition,ensure_ascii=False,indent=2)+'\n')
 body_row=[x for x in range(80) if im.getpixel((x,60))[3]]
 body_width=max(body_row)-min(body_row)+1;plate_width=sprite('plato').width
 assert body_width>=plate_width*1.8
 (ROOT/'checks.json').write_text(json.dumps({'native_size':SIZE,'palette_colors':4,'binary_alpha':True,'connected_silhouette':True,'body_width_including_arms':body_width,'plate_width':plate_width,'body_plate_ratio':round(body_width/plate_width,2),'waist_row':WAIST,'horizontal_position':[120,14],'vertical_position':[50,92],'integration':'reference_only'},indent=2)+'\n')
 review_board()
 print('Sprite genérico nativo + comparaciones con el entorno; sin cambios al juego.')

if __name__=='__main__':export()
