"""Reference-only face refinement: softer contours and native-pixel facial proportions."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageFont,ImageChops
import importlib.util,json,math
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
spec=importlib.util.spec_from_file_location('previous_cast',ROOT.parent/'customers-24-2026-10-31/generate.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
P=old.P;CAST=old.CAST
SIZE=(64,80)
def color(v):return P.get(v,v)
def draw(im):return ImageDraw.Draw(im)
def line(im,p,c,w=1):draw(im).line([(round(x),round(y)) for x,y in p],fill=color(c),width=w)
def rect(im,b,c):draw(im).rectangle(tuple(round(v) for v in b),fill=color(c))
def poly(im,p,c):draw(im).polygon([(round(x),round(y)) for x,y in p],fill=color(c))
def oval(im,b,c):draw(im).ellipse(tuple(round(v) for v in b),fill=color(c))
def rounded(im,b,c,o=None,r=2):draw(im).rounded_rectangle(tuple(round(v) for v in b),radius=r,fill=color(c),outline=color(o) if o else None)
# Hair-top y, shoulder width, waist width, face width, lean, gesture. Fixed waist baseline only.
ANATOMY=[
(11,34,27,22,-2,'chin'),(14,31,24,21,2,'hip'),(9,35,27,21,-2,'phone'),(17,34,29,22,2,'hips'),
(20,38,32,23,-3,'pocket'),(13,30,23,20,3,'wave'),(8,35,28,22,-2,'cross'),(21,31,26,21,2,'strap'),
(10,39,33,23,2,'hip'),(6,40,33,24,-2,'cross'),(23,30,25,22,-2,'wave'),(12,32,25,21,3,'goggles'),
(15,36,31,22,-1,'strap'),(18,31,24,21,2,'clasp'),(22,39,34,23,-2,'chin'),(9,33,26,21,2,'listen'),
(13,40,35,24,2,'hips'),(11,30,23,20,-2,'phone'),(7,42,35,23,-1,'cross'),(15,34,27,22,3,'hip'),
(18,32,25,21,-2,'chin'),(8,37,28,22,3,'strap'),(20,36,30,22,-2,'pocket'),(23,39,34,24,2,'clasp')]
POSE_NAMES={'chin':'Mano en la barbilla','hip':'Mano en cintura','hips':'Ambas manos en cintura','phone':'Consultando el móvil','pocket':'Mano en bolsillo','wave':'Saludo abierto','cross':'Brazos cruzados','strap':'Sujetando la correa','listen':'Ajustando audífonos','goggles':'Ajustando los goggles','clasp':'Manos entrelazadas'}

def mask_poly(points):
 m=Image.new('L',SIZE);draw(m).polygon([(round(x),round(y)) for x,y in points],fill=255);return m

def volume(im,mask,ramp,outline=None):
 """Flat cartoon ink and one deliberate shadow patch, rather than cylindrical rendering."""
 shadow,base,_=ramp;outline=outline or shadow
 edge=mask.filter(ImageFilter.MaxFilter(3));im.paste(color(outline),(0,0),edge)
 im.paste(color(base),(0,0),mask)
 box=mask.getbbox()
 if not box:return
 l,t,r,b=box;w=r-l;h=b-t
 # One graphic shadow on the lower/right plane. No specular stripe or graded cheek bands.
 area=mask_poly([(l+w*.68,t+h*.43),(r+1,t+h*.3),(r+1,b+1),(l+w*.53,b+1)])
 shade=ImageChops.multiply(mask,area);im.paste(color(shadow),(0,0),shade)

def capsule(im,a,b,width,ramp):
 m=Image.new('L',SIZE);d=draw(m);a=tuple(round(v) for v in a);b=tuple(round(v) for v in b);w=round(width)
 d.line([a,b],fill=255,width=w)
 for x,y in [a,b]:d.ellipse((x-w//2,y-w//2,x+w//2,y+w//2),fill=255)
 volume(im,m,ramp)

def hand(im,p,skin,gesture='closed',direction=1):
 x,y=p;ss,sb,sl=skin
 oval(im,(x-3,y-3,x+3,y+3),ss);oval(im,(x-2,y-3,x+2,y+2),sb)
 thumb_left,thumb_right=sorted([x+direction,x+4*direction])
 oval(im,(thumb_left,y-1,thumb_right,y+2),ss)
 light_left,light_right=sorted([x+2*direction,x+3*direction]);rect(im,(light_left,y,light_right,y+1),sb)
 if gesture in ['hip','rest']:
  rounded(im,(x-2,y-3,x+2,y+3),sb,ss,1)
  line(im,[(x-1,y+1),(x+1,y+1)],ss)
  line(im,[(x+2*direction,y-2),(x+3*direction,y)],ss)
 if gesture=='open':
  rounded(im,(x-3,y-1,x+3,y+4),sb,ss,2)
  for dx,dy in [(-3,-5),(-1,-7),(1,-6),(3,-4)]:
   line(im,[(x+dx,y),(x+dx,y+dy)],ss,1)
  line(im,[(x-3*direction,y+2),(x-5*direction,y)],ss,2)


# Gentle contour differences. All cheeks and jaws transition through diagonal steps.
# Features are drawn at native resolution AFTER placing the head, never stretched with the skin.
FACE_POINTS={
 'alargada':[(18,3),(29,3),(33,9),(33,18),(31,25),(27,30),(21,30),(17,25),(15,18),(15,9)],
 'cuadrada':[(18,3),(30,3),(34,9),(34,19),(32,25),(28,28),(20,28),(16,25),(14,19),(14,9)],
 'corazon':[(18,3),(30,3),(34,10),(33,18),(30,24),(26,29),(22,29),(18,24),(15,18),(14,10)],
 'ancha':[(18,3),(30,3),(35,10),(35,18),(32,24),(28,28),(20,28),(16,24),(13,18),(13,10)],
 'rombo':[(19,3),(29,3),(34,10),(34,17),(31,24),(27,29),(21,29),(17,24),(14,17),(14,10)],
 'estrecha':[(19,3),(29,3),(32,9),(32,19),(30,25),(26,29),(22,29),(18,25),(16,19),(16,9)],
 'triangular':[(18,3),(30,3),(34,10),(32,19),(29,25),(26,29),(22,29),(19,25),(16,19),(14,10)],
 'mandibula_ancha':[(18,3),(30,3),(34,10),(34,18),(32,24),(28,28),(20,28),(16,24),(14,18),(14,10)],
 'redonda':[(19,3),(29,3),(34,9),(35,16),(33,22),(29,27),(26,29),(22,29),(19,27),(15,22),(13,16),(14,9)]}
FACES=['alargada','corazon','cuadrada','ancha','redonda','triangular','estrecha','mandibula_ancha',
 'rombo','cuadrada','redonda','estrecha','mandibula_ancha','triangular','ancha','alargada',
 'mandibula_ancha','rombo','cuadrada','corazon','estrecha','alargada','rombo','redonda']
FACE_LABELS={'alargada':'oval suave','cuadrada':'mandíbula suave','corazon':'mentón suave',
 'ancha':'oval amplio','rombo':'pómulos suaves','estrecha':'oval estrecho',
 'triangular':'mentón estrecho','mandibula_ancha':'mandíbula amplia','redonda':'mejillas suaves'}
# Eye style, mouth style. Small expressions share the same native-pixel construction.
EXPRESSIONS=[('open','smile'),('open','smile'),('open','neutral'),('happy','grin'),
 ('open','smile'),('open','smile'),('relaxed','smile'),('open','grin'),
 ('open','neutral'),('relaxed','smile'),('open','smile'),('open','smile'),
 ('open','smile'),('happy','grin'),('open','neutral'),('open','grin'),
 ('happy','smile'),('open','neutral'),('open','neutral'),('open','smile'),
 ('open','neutral'),('happy','grin'),('open','smile'),('open','smile')]

def head_layers(i,skin,hair,facew,top,cx):
 """Native-pixel faces with fitted eyes, gentle jaws, minimal noses and small mouths."""
 ss,sb,sl=skin;hs,hb,hl=hair;kind=CAST[i][3];acc=CAST[i][8];ratio=facew/22
 headsize=(48,54);centre=24
 def xy(x,y):return (round(centre+(x-24)*ratio),round(y*ratio))
 pts=[xy(x,y) for x,y in FACE_POINTS[FACES[i]]]
 mask=Image.new('L',headsize);draw(mask).polygon(pts,fill=255)
 face=Image.new('RGBA',headsize);rear=Image.new('RGBA',headsize)
 face.paste(color(ss),(0,0),mask.filter(ImageFilter.MaxFilter(3)))
 face.paste(color(sb),(0,0),mask)
 chin=max(y for x,y in pts)
 # A small jaw shadow, no large side-of-face plane or cylindrical cheek shading.
 shade=Image.new('L',headsize);draw(shade).polygon([(centre+6,chin-5),(centre+12,chin-4),(centre+8,chin),(centre-2,chin)],fill=255)
 face.paste(color(ss),(0,0),ImageChops.multiply(mask,shade))
 eye_y=round(14*ratio)
 row=[x for x in range(48) if mask.getpixel((x,eye_y))]
 left,right=min(row),max(row)
 eye_gap=max(4,min(5,round((right-left)*.23)))
 eyes=[centre-eye_gap,centre+eye_gap]
 for xx in [left,right]:
  rounded(face,(xx-1,eye_y,xx+1,eye_y+4),ss,None,1)
  line(face,[(xx,eye_y+1),(xx,eye_y+2)],sb)
 eye_style,mouth_style=EXPRESSIONS[i]
 # Both eyes use exactly the same height and pupil construction, including under glasses.
 for ex in eyes:
  line(face,[(ex-2,eye_y-4),(ex+1,eye_y-4)],hs)
  if eye_style=='happy':line(face,[(ex-1,eye_y+1),(ex,eye_y),(ex+1,eye_y+1)],'negro')
  elif eye_style=='relaxed':line(face,[(ex-1,eye_y+1),(ex+1,eye_y+1)],'negro')
  else:rect(face,(ex-1,eye_y,ex,eye_y+2),'negro')
 # One small nose mark, with a full gap to the mouth and eyes.
 nose_y=eye_y+5;line(face,[(centre,nose_y-1),(centre+1,nose_y),(centre,nose_y)],ss)
 mouth_y=chin-6
 if acc in ['beard','glasses_beard']:
  beard=Image.new('L',headsize)
  draw(beard).polygon([(left+1,nose_y),(centre-4,mouth_y-1),(centre+4,mouth_y-1),
   (right-1,nose_y),(right+1,chin+1),(left-1,chin+1)],fill=255)
  face.paste(color(hs),(0,0),ImageChops.multiply(mask,beard))
  rounded(face,(centre-3,mouth_y-1,centre+3,mouth_y+2),sb,None,1)
 if mouth_style=='grin':
  rounded(face,(centre-3,mouth_y,centre+3,mouth_y+2),ss,None,1)
  line(face,[(centre-2,mouth_y),(centre+2,mouth_y)],'crema')
 elif mouth_style=='smile':line(face,[(centre-2,mouth_y),(centre-1,mouth_y+1),(centre+1,mouth_y+1),(centre+2,mouth_y)],ss)
 else:line(face,[(centre-2,mouth_y),(centre+2,mouth_y)],ss)
 if acc=='moustache':
  line(face,[(centre-3,mouth_y-2),(centre-1,mouth_y-3),(centre,mouth_y-2),(centre+1,mouth_y-3),(centre+3,mouth_y-2)],hs)
 if acc=='stubble':
  for dx,dy in [(-5,-1),(-4,2),(4,2),(5,-1)]:rect(face,(centre+dx,mouth_y+dy,centre+dx,mouth_y+dy),hs)
 # Fit the original hairstyle to the softened temple width, independent of facial features.
 temple_y=round(10*ratio);temple=[x for x in range(48) if mask.getpixel((x,temple_y))]
 hair_x_scale=(max(temple)-min(temple)+4)/24
 def place_hair(back):
  layer=Image.new('RGBA',(48,48))
  (old.hair_back if back else old.hair_front)(layer,kind,hs,hb,hb)
  w=round(48*hair_x_scale);h=round(48*ratio)
  scaled=layer.resize((w,h),Image.Resampling.NEAREST)
  result=Image.new('RGBA',headsize);result.paste(scaled,(centre-w//2,0),scaled)
  return result
 rear=place_hair(True)
 if kind=='bun':
  # A visible, connected topknot. The old tied-hair module hid the bun behind its own crown.
  rear=Image.new('RGBA',headsize)
  oval(rear,(centre-4,0,centre+4,8),hs)
  oval(rear,(centre-3,1,centre+2,5),hb)
  draw(face).rectangle((0,0,47,3),fill=(0,0,0,0))
  rounded(face,(left-1,4,right+1,eye_y-2),hb,hs,3)
  poly(face,[(left-1,8),(left+2,9),(left+1,eye_y+1),(left-1,eye_y)],hs)
  poly(face,[(right+1,8),(right-2,9),(right-1,eye_y+1),(right+1,eye_y)],hs)
 else:face.alpha_composite(place_hair(False))
 # Accessories are anchored to this head's eyes/ears, rather than an old fixed face template.
 if acc in ['glasses','roundglasses','glasses_beard']:
  for ex in eyes:
   box=(ex-3,eye_y-2,ex+3,eye_y+4)
   if acc=='roundglasses':draw(face).ellipse(box,outline=color('negro'))
   else:rounded(face,box,None,'negro',1)
  line(face,[(eyes[0]+3,eye_y),(eyes[1]-3,eye_y)],'negro')
  line(face,[(left,eye_y-1),(eyes[0]-3,eye_y-1)],'negro')
  line(face,[(eyes[1]+3,eye_y-1),(right,eye_y-1)],'negro')
 if acc=='earbuds':
  for xx in [left,right]:line(face,[(xx,eye_y+1),(xx,eye_y+4)],'gris-claro')
 if acc=='piercing':
  rect(face,(right+1,eye_y+3,right+1,eye_y+4),'gris')
  rect(face,(centre+2,nose_y,centre+2,nose_y),'gris')
 if acc in ['headband','bandana']:
  yy=round(7*ratio);cc='rojo' if acc=='bandana' else 'gris-claro'
  line(face,[xy(14,7),xy(34,7)],cc,2)
  if acc=='bandana':
   for dx in [-6,0,6]:rect(face,(centre+dx,yy,centre+dx,yy),'blanco')
   poly(face,[(right-1,yy),(right+4,yy+1),(right+2,yy+4)],'rojo-oscuro')
 if acc=='beanie':
  rounded(face,(*xy(12,0),*xy(35,8)),'oxido',None,4)
  rect(face,(*xy(12,6),*xy(35,10)),'tostado')
  for x in [16,21,26,31]:line(face,[xy(x,7),xy(x,9)],'canela')
 if acc=='clips':
  for xx in [left+2,right-4]:
   rect(face,(xx,eye_y-5,xx+3,eye_y-4),'cian')
 if acc=='goggles':
  yy=round(6*ratio)
  line(face,[(left,yy),(right,yy)],'noche',2)
  for ex,cc in zip(eyes,['cian','magenta']):rounded(face,(ex-3,yy-2,ex+3,yy+2),cc,'noche',1)
 if acc=='visor':
  rounded(face,(left+1,eye_y-2,right-1,eye_y+3),'azul-oscuro','noche',2)
  line(face,[(left+3,eye_y-1),(centre+2,eye_y-1)],'cian')
 if acc=='headphones':
  line(face,[(left-2,eye_y+1),(left-2,round(7*ratio)),(left+2,round(5*ratio)),(right-2,round(5*ratio)),(right+2,round(7*ratio)),(right+2,eye_y+1)],'noche',2)
  for xx in [left-1,right+1]:rounded(face,(xx-1,eye_y-1,xx+1,eye_y+6),'pizarra','negro',1)
 if acc in ['cap','capback']:
  cc='verde-oscuro' if acc=='cap' else 'azul-oscuro'
  rounded(face,(*xy(12,0),*xy(35,7)),cc,'negro',3)
  if acc=='cap':rect(face,(*xy(19,6),*xy(38,8)),'verde-noche')
  else:
   rect(face,(*xy(9,6),*xy(17,8)),cc)
   rect(face,(*xy(20,5),*xy(27,7)),'gris')
 offset=(round(cx)-centre,top)
 return (rear,offset),(face,offset)

def clothing(im,mask,cx,sy,ww,kind,ramp):
 ss,sb,sl=ramp
 details=Image.new('RGBA',SIZE);y0=sy+2;y1=78
 # Clothing is shaped by the body: a curved chest, tapered waist and asymmetrical shoulders.
 if kind in ['flannel','overshirt','hawaiian','leather','utility','blazer','cardigan','vest']:
  poly(details,[(cx-5,sy-1),(cx+5,sy),(32+7,y1),(32-7,y1)],'gris-claro' if kind!='leather' else 'noche')
  poly(details,[(cx-7,sy),(cx-2,sy+7),(cx-7,sy+13),(32-ww/2,77),(32-ww/2-3,sy+10)],sb)
  poly(details,[(cx+6,sy),(cx+3,sy+8),(cx+8,sy+13),(32+ww/2,77),(32+ww/2+2,sy+10)],ss)
  line(details,[(cx-8,sy+1),(cx-3,sy+8),(cx-7,sy+13),(27,76)],sl)
  line(details,[(cx+7,sy+2),(cx+3,sy+8),(cx+7,sy+12)],sb)
  if kind in ['leather','blazer']:
   poly(details,[(cx-8,sy),(cx-1,sy+8),(cx-7,sy+14),(cx-11,sy+4)],sb)
   line(details,[(cx-7,sy+14),(27,76)],'gris-azul')
   line(details,[(cx+9,sy+16),(cx+15,sy+18)],'gris')
  if kind=='flannel':
   for yy in range(round(sy+10),77,6):line(details,[(cx-18,yy),(cx-7,yy)],sl);line(details,[(cx+8,yy),(cx+18,yy)],sl)
   for dx in [-14,-9,10,15]:line(details,[(cx+dx,sy+5),(32+dx,78)],ss)
  if kind in ['overshirt','utility','vest']:
   for dx in [-14,9]:
    rounded(details,(cx+dx,sy+11,cx+dx+6,sy+19),sb,ss,1);line(details,[(cx+dx+1,sy+13),(cx+dx+5,sy+13)],sl)
  if kind=='hawaiian':
   for dx,dy in [(-13,12),(11,17),(-10,25),(14,29)]:
    xx=cx+dx;yy=sy+dy;rect(details,(xx-1,yy,xx+2,yy+1),'crema');rect(details,(xx,yy-1,xx+1,yy+2),'crema');rect(details,(xx,yy,xx,yy),'oxido')
 elif kind in ['jersey','retro']:
  poly(details,[(cx-7,sy-2),(cx,sy+5),(cx+7,sy-2),(cx+6,sy+3),(cx,sy+9),(cx-7,sy+3)],'gris-claro')
  if kind=='retro':
   for dx in [-10,7]:line(details,[(cx+dx,sy+10),(32+dx,77)],'crema',3)
  yy=sy+13;line(details,[(cx-4,yy),(cx,yy-2),(cx,yy+7)],'blanco',2)
  rounded(details,(cx+7,sy+8,cx+11,sy+13),'crema',ss,1)
 elif kind=='hoodie':
  poly(details,[(cx-9,sy-3),(cx-2,sy+6),(cx+2,sy+7),(cx+9,sy-3),(cx+10,sy+4),(cx+3,sy+11),(cx-5,sy+8)],ss)
  line(details,[(cx-7,sy),(cx,sy+8),(cx+8,sy)],sl)
  for dx in [-3,4]:line(details,[(cx+dx,sy+10),(cx+dx,sy+17)],'gris-claro')
  rounded(details,(24,66,40,74),sb,ss,2)
 elif kind in ['tech','rave','tracksuit']:
  rounded(details,(cx-6,sy-4,cx+6,sy+3),ss,ss,2)
  line(details,[(cx,sy),(32,77)],sl)
  if kind=='tech':
   line(details,[(cx-12,sy+2),(42,70)],'gris-azul',3)
   rounded(details,(cx-13,sy+16,cx-6,sy+24),ss,'negro',1);rect(details,(cx-11,sy+18,cx-7,sy+19),'gris')
  if kind=='tracksuit':line(details,[(cx-12,sy+14),(cx+13,sy+14)],'gris-claro',2)
  if kind=='rave':
   for dx in [-11,11]:line(details,[(cx+dx,sy+5),(32+dx,74)],'cian',2)
   line(details,[(cx-10,sy+15),(cx+10,sy+15)],'cian')
 elif kind=='varsity':
  line(details,[(cx,sy+2),(32,78)],ss,2)
  for yy in range(round(sy+11),76,7):rect(details,(31,yy,31,yy),'crema')
  line(details,[(cx-10,sy+10),(cx-10,sy+17),(cx-5,sy+17)],'crema',2)
 elif kind=='band':
  rounded(details,(cx-9,sy+10,cx+10,sy+25),'pizarra','negro',2)
  poly(details,[(cx-6,sy+21),(cx-3,sy+14),(cx,sy+18),(cx+5,sy+13),(cx+7,sy+22)],'gris-claro')
 elif kind=='sweater':
  xx=cx;yy=min(sy+11,68)
  poly(details,[(xx,yy-6),(xx+2,yy-2),(xx+6,yy-2),(xx+3,yy+1),(xx+4,yy+6),(xx,yy+3),(xx-4,yy+6),(xx-3,yy+1),(xx-6,yy-2),(xx-2,yy-2)],'crema')
 elif kind=='blouse':
  poly(details,[(cx-9,sy-1),(cx-1,sy+4),(cx-6,sy+10)],'blanco');poly(details,[(cx+9,sy-1),(cx+1,sy+4),(cx+6,sy+10)],'blanco')
  for yy in range(round(sy+12),76,7):rect(details,(31,yy,32,yy),'gris-azul')
 details.putalpha(Image.composite(details.getchannel('A'),Image.new('L',SIZE),mask))
 im.alpha_composite(details)
 # Sparse fabric folds follow the curved waist, never run down the full height.
 for dx in [-1,1]:line(im,[(32+dx*(ww/2-3),70),(32+dx*(ww/2-5),74)],ss)


def clean_isolated_pixels(im):
 # Remove stray ink pixels outside the drawing; retain all meaningful accessory clusters.
 seen=set();alpha=im.getchannel('A')
 for y in range(im.height):
  for x in range(im.width):
   if (x,y) in seen or not alpha.getpixel((x,y)):continue
   component=[];stack=[(x,y)];seen.add((x,y))
   while stack:
    xx,yy=stack.pop();component.append((xx,yy))
    for dx,dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
     nx,ny=xx+dx,yy+dy
     if 0<=nx<im.width and 0<=ny<im.height and (nx,ny) not in seen and alpha.getpixel((nx,ny)):
      seen.add((nx,ny));stack.append((nx,ny))
   if len(component)<3:
    for point in component:im.putpixel(point,(0,0,0,0))
 return im

def cuff(im,a,b,ramp,width=6):
 dx,dy=b[0]-a[0],b[1]-a[1];length=max(1,math.hypot(dx,dy));nx,ny=-dy/length,dx/length
 centre=(a[0]+dx*.89,a[1]+dy*.89)
 line(im,[(centre[0]-nx*width/2,centre[1]-ny*width/2),(centre[0]+nx*width/2,centre[1]+ny*width/2)],ramp[0])

def shoulder_bag(im,cx,sy,cloth):
 # The strap terminates in two real bag attachment points.
 bag_y=66;bx=17 if cx>=32 else 15
 rounded(im,(bx,bag_y,bx+12,78),'crema','canela',2)
 line(im,[(bx+1,bag_y+3),(bx+11,bag_y+3)],'canela')
 for xx in [bx+2,bx+10]:rect(im,(xx,bag_y,xx+1,bag_y+1),'cafe')
 line(im,[(cx-12,sy-1),(bx+2,bag_y)],'crema',3)
 line(im,[(cx-12,sy-1),(bx+10,bag_y)],'canela')

def render(i):
 entry=CAST[i];top,sw,ww,fw,lean,pose=ANATOMY[i];ps,pb,pl=old.SKINS[entry[5]];skin=(ps,pb,pl)
 hs,hb,hl=old.HAIR[entry[4]];cloth=entry[7];kind=entry[6];cx=32+lean
 jaw=max(y for x,y in FACE_POINTS[FACES[i]])
 sy=top+round(jaw*fw/22)+4;head_x=cx-1 if lean<0 else cx+1
 im=Image.new('RGBA',SIZE)
 rear,face=head_layers(i,skin,(hs,hb,hl),fw,top,head_x)
 im.paste(rear[0],rear[1],rear[0])
 shoulders=[(cx-sw/2+3,sy+3),(cx+sw/2-3,sy+4)]
 elbows=[(cx-sw/2-1,sy+17),(cx+sw/2+1,sy+18)]
 wrists=[(32-ww/2-2,72),(32+ww/2+2,72)]
 if pose in ['hip','hips']:
  elbows[1]=(min(56,cx+sw/2+8),sy+17);wrists[1]=(32+ww/2-2,68)
  if pose=='hips':elbows[0]=(max(5,cx-sw/2-8),sy+17);wrists[0]=(32-ww/2+2,68)
 if pose=='pocket':
  elbows[0]=(cx-sw/2-2,sy+16)
  wrists[0]=(27,70) if kind=='hoodie' else (round(32-ww/2+6),69)
 if pose=='wave':elbows[1]=(min(56,cx+sw/2+7),sy+9);wrists[1]=(min(56,cx+sw/2+8),sy-9)
 if pose=='phone':elbows[1]=(min(56,cx+sw/2+6),sy+18);wrists[1]=(cx+15,sy+8)
 if pose=='chin':
  elbows[1]=(min(56,cx+sw/2+4),sy+19)
  wrists[1]=(head_x+round(4*fw/22),top+round((jaw-2)*fw/22))
 if pose in ['listen','goggles']:
  elbows[1]=(min(56,cx+sw/2+8),sy+10)
  wrists[1]=(head_x+round(11*fw/22),top+round((7 if pose=='goggles' else 16)*fw/22))
 if pose=='strap':elbows[0]=(max(5,cx-sw/2-4),sy+17);wrists[0]=(cx-11,sy+9)
 if pose=='cross':
  elbows=[(cx-sw/2-1,sy+19),(cx+sw/2+1,sy+19)]
  wrists=[(cx+10,sy+10),(cx-10,sy+13)]
 if pose=='clasp':
  elbows=[(cx-sw/2-2,sy+15),(cx+sw/2+2,sy+15)];wrists=[(29,70),(35,68)]
 # The waist is a crop boundary, not permission to crop elbows: retain complete joints above it.
 elbows=[(max(6,min(56,x)),min(71,y)) for x,y in elbows]
 for x,y in elbows:assert 5<=x<=57 and y+5<=77
 sleeve=cloth
 if kind in ['varsity','vest']:sleeve=('gris-azul','gris-claro','blanco')
 bare=kind in ['jersey','retro','band','hawaiian']
 # T-shirt arms really emerge from a short sleeve. No shirt-coloured forearm before the elbow.
 for k in [0,1]:
  if bare:
   capsule(im,shoulders[k],elbows[k],6,skin)
   a,b=shoulders[k],elbows[k];hem=(a[0]+(b[0]-a[0])*.42,a[1]+(b[1]-a[1])*.42)
   capsule(im,a,hem,9 if sw>35 else 8,sleeve);cuff(im,a,hem,sleeve,7)
  else:capsule(im,shoulders[k],elbows[k],9 if sw>35 else 8,sleeve)
 torso=mask_poly([(cx-5,sy-3),(cx+5,sy-3),(cx+sw/2-4,sy+2),(cx+sw/2-1,sy+8),(cx+sw*.4,sy+18),(32+ww/2,77),(32-ww/2,77),(cx-sw*.4,sy+18),(cx-sw/2+1,sy+8),(cx-sw/2+4,sy+2)])
 volume(im,torso,cloth);clothing(im,torso,cx,sy,ww,kind,cloth)
 capsule(im,(cx,top+23),(cx,sy+1),7,skin)
 line(im,[(cx-5,sy),(cx,sy+3),(cx+5,sy)],cloth[0],2)
 acc=entry[8]
 if acc in ['chain','shells']:line(im,[(cx-6,sy),(cx-3,sy+6),(cx+3,sy+7),(cx+7,sy)],'ambar' if acc=='chain' else 'crema')
 if acc=='choker':line(im,[(cx-3,sy-5),(cx+3,sy-5)],'negro',2);rect(im,(cx,sy-5,cx+1,sy-4),'gris')
 if acc=='bow':poly(im,[(cx,sy+4),(cx-5,sy+1),(cx-5,sy+7),(cx,sy+5),(cx+5,sy+1),(cx+5,sy+7)],'rosa')
 if acc=='scarf':poly(im,[(cx-5,sy-3),(cx+5,sy-3),(cx+6,sy+2),(cx-1,sy+4),(cx-4,sy+13),(cx-7,sy+10),(cx-4,sy+2)],'ambar')
 if pose=='strap' or acc=='tote':shoulder_bag(im,cx,sy,cloth)
 im.paste(face[0],face[1],face[0])
 # Forearm order is intentional for crossed arms: the second arm is in front at the crossing.
 for k in [0,1]:
  capsule(im,elbows[k],wrists[k],6 if bare else 7,skin if bare else sleeve)
  if not bare:
   cuff(im,elbows[k],wrists[k],sleeve)
   if kind=='utility':cuff(im,elbows[k],wrists[k],('gris-claro','gris-claro','blanco'),4)
  x,y=wrists[k]
  if pose=='pocket' and k==0:
   # Wrist goes under the pocket lip; only a small skin edge remains visible.
   oval(im,(x-2,y-2,x+2,y+1),skin[1])
   line(im,[(x-4,y+1),(x+4,y-1)],cloth[0],2)
   line(im,[(x-3,y+2),(x+3,y)],cloth[1])
  elif pose=='phone' and k==1:
   # Object first; the thumb and fingertips then wrap visibly over its near edge.
   hand(im,(x,y+1),skin,'rest',-1)
   rounded(im,(x-2,y-9,x+3,y+1),'noche','negro',1);rect(im,(x-1,y-7,x+2,y-2),'gris-azul')
   line(im,[(x-3,y-1),(x,y)],skin[1],2);rect(im,(x+3,y-2,x+3,y),skin[1])
  elif pose=='clasp':
   hand(im,wrists[k],skin,'rest',1 if k==0 else -1)
  else:
   gesture='open' if pose=='wave' and k==1 else 'hip' if pose in ['hip','hips'] and (k==1 or pose=='hips') else 'rest' if pose in ['cross','chin','strap','listen','goggles'] else 'closed'
   hand(im,wrists[k],skin,gesture,1 if k==0 else -1)
 if pose=='clasp':line(im,[(31,68),(32,70),(34,70)],skin[0])
 # The earcup and goggles already belong to the head layer; no floating duplicate prop.
 return clean_isolated_pixels(im)

FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def text(im,p,t,size=22,c='gris-claro'):draw(im).text(p,t,font=ImageFont.truetype(FONT,size),fill=color(c))
def sheet(start,filename):
 out=Image.new('RGB',(1520,1510),color('negro'));text(out,(32,22),f'CLIENTES / ROSTROS SIMPLIFICADOS / {start+1:02}—{start+12:02}',32,'crema')
 text(out,(32,68),'Contornos suaves · rasgos más simples · referencias sin integrar',20,'gris')
 for j in range(12):
  i=start+j;x=32+j%4*374;y=119+j//4*451
  text(out,(x,y),f'{i+1:02} {CAST[i][0]} / {CAST[i][1]}',23,'crema')
  text(out,(x,y+31),POSE_NAMES[ANATOMY[i][5]],18)
  bg=Image.new('RGB',(320,332),color('noche'));sprite=render(i).resize((256,320),Image.Resampling.NEAREST);bg.paste(sprite,(32,6),sprite)
  # Waist baseline makes true height variation visible, without scaling each portrait to fit.
  line(bg,[(12,322),(308,322)],'pizarra')
  out.paste(bg,(x,y+62));text(out,(x,y+401),f'{CAST[i][2]} · {FACE_LABELS[FACES[i]]}',16,'gris')
 out.save(ROOT/filename)

def context_sheet():
 spec=importlib.util.spec_from_file_location('customer_env',REPO/'scripts/sprites/environment_gen.py');env=importlib.util.module_from_spec(spec);spec.loader.exec_module(env)
 definitions=json.loads((ROOT.parent/'kitchen-2026-10-31/source-sprites.json').read_text())
 def sprite(im,key,x,y):
  d=definitions['sprites'][key];piece=Image.new('RGBA',(d['width'],d['height']))
  for yy,row in enumerate(d['frames'][0]):
   for xx,k in enumerate(row):
    if k!='.':piece.putpixel((xx,yy),tuple(bytes.fromhex(P[d['colors'][k]][1:]))+(255,))
  im.paste(piece,(x,y),piece)
 out=Image.new('RGB',(1400,1580),color('negro'));text(out,(32,22),'ROSTROS SIMPLIFICADOS / PRUEBA EN EL ESCENARIO',30,'crema')
 text(out,(32,67),'Misma escala y misma cintura · cuerpo de 64 px centrado · muestra sin interfaz',20,'gris')
 for j,i in enumerate([1,4,7,14,20,23]):
  x=32+j%2*680;y=120+j//2*480;text(out,(x,y),f'{i+1:02} {CAST[i][0]} / {POSE_NAMES[ANATOMY[i][5]]}',23,'crema')
  im=Image.new('RGB',(320,200),color('noche'));im.paste(env.dining_horizontal(),(0,0));person=render(i);im.paste(person,(128,46),person);im.paste(env.red_bar(),(0,122))
  sprite(im,'plato',145,120)
  for k,xx in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:sprite(im,k,xx,103)
  for k,xx in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:sprite(im,k,xx,139)
  sprite(im,'plancha',82,165);sprite(im,'charola',244,165);sprite(im,'basura',40,170)
  for k,xx,yy in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:sprite(im,k,xx,yy)
  out.paste(im.resize((640,400),Image.Resampling.NEAREST),(x,y+42))
 out.save(ROOT/'customers-soft-faces-context.png')

def faces_sheet():
 out=Image.new('RGB',(1520,1220),color('negro'))
 text(out,(32,22),'24 CLIENTES / ROSTROS MÁS SUAVES',32,'crema')
 text(out,(32,68),'Mandíbulas moderadas · ojos alineados · nariz y boca simplificadas',20,'gris')
 for i in range(24):
  x=32+(i%6)*248;y=116+(i//6)*270
  text(out,(x,y),f'{i+1:02} {CAST[i][0]}',21,'crema')
  top,sw,ww,fw,lean,pose=ANATOMY[i]
  rear,front=head_layers(i,old.SKINS[CAST[i][5]],old.HAIR[CAST[i][4]],fw,top,32)
  head=rear[0].copy();head.alpha_composite(front[0])
  portrait=head.crop((4,0,44,38)).resize((200,190),Image.Resampling.NEAREST)
  bg=Image.new('RGB',(216,200),color('noche'));bg.paste(portrait,(8,4),portrait)
  out.paste(bg,(x,y+34));text(out,(x,y+240),CAST[i][1],16,'gris')
 out.save(ROOT/'faces-24.png')

if __name__=='__main__':
 allowed={tuple(bytes.fromhex(h[1:])) for h in P.values()};manifest=[]
 for i in range(24):
  im=render(i);im.save(ROOT/f'customer-{i+1:02}-1x.png')
  assert all(a==0 or (r,g,b) in allowed for r,g,b,a in im.getdata())
  manifest.append({'id':i+1,'name':CAST[i][0],'style':CAST[i][1],'pronouns':CAST[i][2],'pose':POSE_NAMES[ANATOMY[i][5]],'anatomy':ANATOMY[i],'face_shape':FACE_LABELS[FACES[i]],'expression':EXPRESSIONS[i]})
 sheet(0,'customers-soft-faces-01-12.png');sheet(12,'customers-soft-faces-13-24.png');context_sheet();faces_sheet()
 (ROOT/'cast.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print('24 reference faces softened; features drawn at native resolution; palette checked; no runtime writes.')
