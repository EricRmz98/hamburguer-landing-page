"""Reference-only, native pixel prototype inspired by the user's smooth white figures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import json, math

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'scene-source.json').read_text())
P=DATA['palette'];SIZE=(80,144);CX=40;WAIST=92
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'

def color(name):return tuple(bytes.fromhex(P[name][1:]))+(255,)
def text(im,xy,label,size=22,ink='gris-claro'):
 ImageDraw.Draw(im).text(xy,label,font=ImageFont.truetype(FONT,size),fill=P[ink])

def empty():return Image.new('L',SIZE)
def outline(im,mask,ink='gris'):
 im.paste(color(ink),(0,0),mask.filter(ImageFilter.MaxFilter(3)))

def polygon(points):
 mask=empty();ImageDraw.Draw(mask).polygon(points,fill=255);return mask

def leg(start,end):
 mask=empty();draw=ImageDraw.Draw(mask)
 draw.line([start,end],fill=255,width=11)
 for x,y in [start,end]:draw.ellipse((x-5,y-5,x+5,y+5),fill=255)
 return mask

def parts(closed=False):
 # Straight, parallel leg edges. Their combined thickness stays below torso width.
 legs=[leg((33,98),(33,135)),leg((46,98),(46,135))] if closed else [leg((30,98),(24,135)),leg((49,98),(55,135))]
 left=polygon([(25,42),(19,44),(14,51),(11,85),(12,89),(15,91),(19,91),(22,88),(25,52)])
 right=polygon([(51,38),(74,57),(76,61),(74,65),(59,82),(54,81),(52,77),(65,61),(50,48)])
 # The chest, abdomen and hip share the same parallel sides: no flared pelvis.
 torso=polygon([(35,33),(43,33),(51,37),(55,43),(54,50),(54,99),(25,99),(25,50),(23,45),(26,40)])
 neck=polygon([(35,27),(44,27),(44,37),(35,37)])
 head=empty();ImageDraw.Draw(head).ellipse((27,5,51,30),fill=255)
 return legs+[left,right,torso,neck,head]

def prototype(closed=False):
 masks=parts(closed);whole=empty();paint=Image.new('RGBA',SIZE)
 for mask in masks:
  whole=ImageChops.lighter(whole,mask)
  paint.paste(color('blanco'),(0,0),mask)
  # One narrow side shade follows each straight segment; no elbow/knee bands.
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
 out=Image.new('RGB',(1460,1048),P['negro'])
 text(out,(28,20),'PERSONAJE GENÉRICO / PRUEBA',32,'crema')
 text(out,(28,69),'Torso recto · extremidades rectas · piernas más delgadas',21)
 text(out,(28,121),'SPRITE',22,'crema')
 bg=Image.new('RGB',(368,488),P['noche']);im=prototype().resize((240,432),Image.Resampling.NEAREST)
 bg.paste(im,(64,18),im);out.paste(bg,(28,160))
 text(out,(28,675),'Torso con laterales paralelos',21,'crema')
 text(out,(28,708),'Brazos y piernas sin abultamientos',20)
 text(out,(28,741),'Sin ensanchar el pecho',20)
 text(out,(430,121),'DENTRO DEL ESCENARIO',22,'crema')
 im=scene().resize((960,600),Image.Resampling.NEAREST);out.paste(im,(430,160),im)
 text(out,(430,788),'Proporción revisada frente a la barra y al plato.',21,'crema')
 text(out,(28,855),'PROPORCIÓN / MISMA ESCALA',22,'crema')
 comparison=Image.new('RGB',(368,128),P['noche'])
 small=prototype().crop((0,0,SIZE[0],WAIST+1));comparison.paste(small,(27,8),small)
 plate=sprite('plato');comparison.paste(plate,(157,81),plate)
 text(comparison,(204,28),'Figura y plato',17)
 text(comparison,(204,52),'sin ampliar',17)
 out.paste(comparison,(28,894))
 text(out,(430,858),'Referencia para revisar el estilo y la escala.',21)
 text(out,(430,893),'El juego conserva los clientes actuales.',20)
 out.save(ROOT/'prototype-review.png')

def reference_comparison():
 out=Image.new('RGB',(1400,800),P['negro'])
 text(out,(24,20),'REFERENCIA → SPRITE',30,'crema')
 text(out,(24,66),'Misma pose de referencia; construcción recta y piernas más delgadas.',21)
 text(out,(24,116),'TU REFERENCIA',20,'crema')
 photo=Image.open(ROOT/'reference.png').convert('RGB').crop((175,155,435,685))
 out.paste(photo,(24,158))
 text(out,(320,116),'SPRITE REFINADO',20,'crema')
 bg=Image.new('RGB',(320,592),P['noche'])
 person=prototype().resize((320,576),Image.Resampling.NEAREST)
 bg.paste(person,(0,0),person);out.paste(bg,(310,142))
 text(out,(700,116),'EN EL ESCENARIO',20,'crema')
 context=scene().resize((640,400),Image.Resampling.NEAREST)
 out.paste(context,(700,158),context)
 text(out,(700,590),'Torso recto, sin ensanchar la cadera.',21,'crema')
 text(out,(700,625),'Extremidades con grosor uniforme.',20)
 text(out,(700,660),'Propuesta de referencia.',20)
 out.save(ROOT/'reference-comparison.png')

def refinement_comparison():
 out=Image.new('RGB',(1400,880),P['negro'])
 text(out,(24,20),'AJUSTE DE PROPORCIONES',30,'crema')
 text(out,(24,66),'Laterales rectos y grosor uniforme; piernas juntas más angostas que el torso.',21)
 previous=Image.open(ROOT.parent/'generic-customer-refined-2026-11-01/generic-customer-1x.png').convert('RGBA')
 for x,label,person in [(24,'ANTERIOR',previous),(350,'LÍNEAS MÁS RECTAS',prototype())]:
  text(out,(x,116),label,20,'crema')
  bg=Image.new('RGB',(300,608),P['noche'])
  person=person.resize((person.width*4,person.height*4),Image.Resampling.NEAREST)
  bg.paste(person,(-10,8),person);out.paste(bg,(x,154))
 text(out,(700,116),'EN EL ESCENARIO',20,'crema')
 context=scene().resize((640,400),Image.Resampling.NEAREST)
 out.paste(context,(700,154),context)
 text(out,(700,600),'PIERNAS JUNTAS',21,'crema')
 text(out,(700,638),'Más angostas que el torso.',20)
 text(out,(700,676),'Sin aumentar la cadera.',20)
 closed=prototype(True).resize((160,288),Image.Resampling.NEAREST)
 bg=Image.new('RGB',(180,296),P['noche']);bg.paste(closed,(10,4),closed)
 out.paste(bg,(1130,570))
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
 closed_width=max(max(xs)-min(xs)+1 for y in range(106,136) for xs in [[x for x in range(SIZE[0]) if closed.getpixel((x,y))[3]]])
 assert closed_width<32
 (ROOT/'checks.json').write_text(json.dumps({'native_size':SIZE,'palette_colors':len({pixel for pixel in im.getdata() if pixel[3]}),'binary_alpha':True,'connected_silhouette':True,'geometry':'straight_parallel_sides','torso_width_with_outline':32,'closed_legs_max_width_with_outline':closed_width,'comparison_row':55,'body_width_including_arms':body_width,'plate_width':plate_width,'body_plate_ratio':round(body_width/plate_width,2),'waist_row':WAIST,'horizontal_position':[DATA['layouts']['horizontal']['w']//2-CX,DATA['layouts']['horizontal']['counter'][1]-WAIST],'vertical_position':[DATA['layouts']['vertical']['w']//2-CX,DATA['layouts']['vertical']['counter'][1]-WAIST],'integration':'reference_only'},indent=2)+'\n')
 closed.save(ROOT/'generic-customer-legs-together-1x.png')
 review_board()
 reference_comparison()
 refinement_comparison()
 print('Sprite genérico nativo + comparaciones con el entorno; sin cambios al juego.')

if __name__=='__main__':export()
