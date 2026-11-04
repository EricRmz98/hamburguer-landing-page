"""Reference-only, native pixel prototype inspired by the user's smooth white figures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import json, math

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'scene-source.json').read_text())
P=DATA['palette'];SIZE=(80,136);CX=40;WAIST=85
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'

def color(name):return tuple(bytes.fromhex(P[name][1:]))+(255,)
def text(im,xy,label,size=22,ink='gris-claro'):
 ImageDraw.Draw(im).text(xy,label,font=ImageFont.truetype(FONT,size),fill=P[ink])

def empty():return Image.new('L',SIZE)
def outline(im,mask,ink='gris'):
 im.paste(color(ink),(0,0),mask.filter(ImageFilter.MaxFilter(3)))

def polygon(points):
 mask=empty();ImageDraw.Draw(mask).polygon(points,fill=255);return mask

def capsule(points,radius):
 mask=empty();draw=ImageDraw.Draw(mask)
 draw.line(points,fill=255,width=radius*2+1,joint='curve')
 for x,y in [points[0],points[-1]]:
  draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=255)
 return mask

def parts(closed=False):
 # Reference: about 4.4 heads tall; head almost as wide as the straight torso.
 # Neutral standing pose is the clearest proportion reference in the new image.
 legs=[capsule([(33 if closed else 32,84),(33 if closed else 32,124)],6),capsule([(46 if closed else 47,84),(46 if closed else 47,124)],6)]
 left=capsule([(26,43),(18,56),(17,79)],6)
 right=left.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 torso=polygon([(35,34),(44,34),(52,37),(56,42),(54,49),(54,87),(25,87),(25,49),(23,42),(27,37)])
 neck=polygon([(35,28),(44,28),(44,38),(35,38)])
 head=empty();ImageDraw.Draw(head).ellipse((26,5,53,31),fill=255)
 return legs+[left,right,torso,neck,head]

def prototype(closed=False):
 masks=parts(closed);whole=empty();paint=Image.new('RGBA',SIZE)
 for mask in masks:
  whole=ImageChops.lighter(whole,mask)
  paint.paste(color('blanco'),(0,0),mask)
  shade=ImageChops.subtract(mask,ImageChops.offset(mask,-2,0))
  paint.paste(color('gris-claro'),(0,0),shade)
 out=Image.new('RGBA',SIZE);outline(out,whole,'gris-azul');out.alpha_composite(paint)
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
 person=prototype().crop((0,0,SIZE[0],WAIST+1));pos=(l['w']//2-CX,l['counter'][1]-WAIST)
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
 out=Image.new('RGB',(1400,820),P['negro'])
 text(out,(24,20),'PROPORCIONES DE LA NUEVA REFERENCIA',30,'crema')
 text(out,(24,66),'Cabeza casi del ancho del torso · cuerpo compacto · brazos relajados',21)
 text(out,(24,116),'TU REFERENCIA',20,'crema')
 # Isolate the neutral standing figure; no stretching of either axis.
 photo=Image.open(ROOT/'reference.png').convert('RGB').crop((109,226,180,359))
 photo=photo.resize((284,532),Image.Resampling.NEAREST)
 out.paste(photo,(24,154))
 text(out,(350,116),'NUEVA BASE',20,'crema')
 bg=Image.new('RGB',(300,560),P['noche']);person=prototype().resize((320,544),Image.Resampling.NEAREST)
 bg.paste(person,(-10,0),person);out.paste(bg,(350,154))
 text(out,(700,116),'EN EL ESCENARIO',20,'crema')
 context=scene().resize((640,400),Image.Resampling.NEAREST);out.paste(context,(700,154),context)
 text(out,(700,595),'Cabeza y torso de anchura similar.',21,'crema')
 text(out,(700,632),'Torso más corto que en la versión anterior.',20)
 text(out,(700,669),'Piernas casi paralelas, dentro del ancho del torso.',20)
 text(out,(24,751),'Propuesta de referencia · sin reemplazar los clientes actuales',20)
 out.save(ROOT/'prototype-review.png')

def refinement_comparison():
 out=Image.new('RGB',(1400,820),P['negro'])
 text(out,(24,20),'COMPARACIÓN DE PROPORCIONES',30,'crema')
 text(out,(24,66),'El cambio está en la relación entre cabeza, torso y extremidades.',21)
 previous=Image.open(ROOT.parent/'generic-customer-straight-2026-11-01/generic-customer-1x.png').convert('RGBA')
 for x,label,person in [(24,'ANTERIOR',previous),(350,'NUEVA BASE',prototype())]:
  text(out,(x,116),label,20,'crema')
  bg=Image.new('RGB',(300,608),P['noche']);person=person.resize((person.width*4,person.height*4),Image.Resampling.NEAREST)
  bg.paste(person,(-10,0),person);out.paste(bg,(x,154))
 text(out,(700,116),'EN EL ESCENARIO',20,'crema')
 context=scene().resize((640,400),Image.Resampling.NEAREST);out.paste(context,(700,154),context)
 text(out,(700,595),'Cabeza más ancha respecto al cuerpo.',21,'crema')
 text(out,(700,632),'Menos distancia de los hombros a la cadera.',20)
 text(out,(700,669),'Apoyo y separación de piernas más naturales.',20)
 out.save(ROOT/'refinement-comparison.png')

def export():
 im=prototype();allowed={color(name) for name in ['gris-azul','gris','gris-claro','blanco']}
 assert all(not p[3] or p in allowed for p in im.getdata())
 assert all(p[3] in [0,255] for p in im.getdata())
 assert im.getbbox()[0]>0 and im.getbbox()[2]<SIZE[0]
 opaque={(x,y) for y in range(SIZE[1]) for x in range(SIZE[0]) if im.getpixel((x,y))[3]}
 todo=[next(iter(opaque))];connected=set(todo)
 while todo:
  x,y=todo.pop()
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   q=(x+dx,y+dy)
   if q in opaque and q not in connected:connected.add(q);todo.append(q)
 assert connected==opaque
 im.save(ROOT/'generic-customer-1x.png')
 im.resize((SIZE[0]*6,SIZE[1]*6),Image.Resampling.NEAREST).save(ROOT/'generic-customer-6x.png')
 for orientation in ['horizontal','vertical']:
  scene(orientation).resize((DATA['layouts'][orientation]['w']*4,DATA['layouts'][orientation]['h']*4),Image.Resampling.NEAREST).save(ROOT/f'prototype-{orientation}.png')
 scene('horizontal',False).resize((1280,800),Image.Resampling.NEAREST).save(ROOT/'prototype-empty-plate.png')
 letters={'gris-azul':'o','gris-claro':'b','blanco':'h'}
 pixels=[''.join('.' if not im.getpixel((x,y))[3] else letters[next(name for name in letters if color(name)==im.getpixel((x,y)))] for x in range(SIZE[0])) for y in range(SIZE[1])]
 definition={'id':'cliente_generico_prueba','size':list(SIZE),'colors':{v:k for k,v in letters.items()},'pixels':'\n'.join(pixels),'waist':WAIST}
 (ROOT/'sprite.json').write_text(json.dumps(definition,ensure_ascii=False,indent=2)+'\n')
 body_row=[x for x in range(SIZE[0]) if im.getpixel((x,55))[3]]
 body_width=max(body_row)-min(body_row)+1;plate_width=sprite('plato').width
 assert body_width>=plate_width*1.8
 closed=prototype(True)
 closed_width=max(max(xs)-min(xs)+1 for y in range(96,125) for xs in [[x for x in range(SIZE[0]) if closed.getpixel((x,y))[3]]])
 assert closed_width<32
 (ROOT/'checks.json').write_text(json.dumps({'native_size':SIZE,'palette_colors':len({pixel for pixel in im.getdata() if pixel[3]}),'binary_alpha':True,'connected_silhouette':True,'geometry':'compact_neutral_standing','head_fill_size':[28,27],'head_to_torso_width_ratio':round(28/30,2),'height_in_head_units':round((im.getbbox()[3]-im.getbbox()[1])/29,2),'torso_width_with_outline':32,'closed_legs_max_width_with_outline':closed_width,'comparison_row':55,'body_width_including_arms':body_width,'plate_width':plate_width,'body_plate_ratio':round(body_width/plate_width,2),'waist_row':WAIST,'horizontal_position':[DATA['layouts']['horizontal']['w']//2-CX,DATA['layouts']['horizontal']['counter'][1]-WAIST],'vertical_position':[DATA['layouts']['vertical']['w']//2-CX,DATA['layouts']['vertical']['counter'][1]-WAIST],'integration':'reference_only'},indent=2)+'\n')
 closed.save(ROOT/'generic-customer-legs-together-1x.png')
 review_board()
 refinement_comparison()
 print('Sprite genérico nativo + comparaciones con el entorno; sin cambios al juego.')

if __name__=='__main__':export()
