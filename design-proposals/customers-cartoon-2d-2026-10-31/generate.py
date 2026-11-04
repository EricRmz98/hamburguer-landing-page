"""Second reference cast: anatomical silhouettes and articulated poses, no runtime writes."""
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
(10,39,33,23,2,'hip'),(6,40,33,24,-2,'cross'),(23,30,25,22,-2,'wave'),(12,32,25,21,3,'listen'),
(15,36,31,22,-1,'pocket'),(18,31,24,21,2,'clasp'),(22,39,34,23,-2,'chin'),(9,33,26,21,2,'listen'),
(13,40,35,24,2,'hips'),(11,30,23,20,-2,'phone'),(7,42,35,23,-1,'cross'),(15,34,27,22,3,'hip'),
(18,32,25,21,-2,'chin'),(8,37,28,22,3,'strap'),(20,36,30,22,-2,'pocket'),(23,39,34,24,2,'clasp')]
POSE_NAMES={'chin':'Mano en la barbilla','hip':'Mano en cintura','hips':'Ambas manos en cintura','phone':'Consultando el móvil','pocket':'Mano en bolsillo','wave':'Saludo abierto','cross':'Brazos cruzados','strap':'Sujetando la correa','listen':'Ajustando audífonos','clasp':'Manos entrelazadas'}

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
 if gesture=='open':
  for dx,dy in [(-2,-5),(0,-6),(2,-5)]:line(im,[(x+dx,y-1),(x+dx,y+dy)],ss,2);line(im,[(x+dx,y-2),(x+dx,y+dy+1)],sb)

FACE_POINTS={
 'alargada':[(18,2),(29,3),(33,9),(32,24),(27,31),(20,31),(14,24),(13,10)],
 'cuadrada':[(16,3),(30,3),(35,9),(35,24),(31,28),(17,28),(12,24),(12,9)],
 'corazon':[(17,3),(30,3),(35,11),(33,20),(24,29),(15,21),(12,12)],
 'ancha':[(15,4),(31,4),(37,12),(36,23),(29,29),(18,29),(10,23),(10,12)],
 'rombo':[(19,2),(29,3),(37,14),(31,24),(24,30),(17,24),(10,14)],
 'estrecha':[(20,2),(28,3),(32,11),(31,23),(26,30),(20,28),(16,23),(15,11)],
 'triangular':[(17,3),(31,3),(35,9),(32,18),(25,30),(21,28),(14,17),(12,10)],
 'mandibula_ancha':[(18,3),(28,3),(32,10),(36,20),(33,27),(17,28),(12,22),(15,10)],
 'redonda':[(16,4),(29,3),(34,8),(36,16),(33,24),(27,28),(18,27),(12,22),(11,12)]}
FACES=['alargada','corazon','cuadrada','ancha','redonda','triangular','estrecha','mandibula_ancha',
 'rombo','cuadrada','redonda','estrecha','mandibula_ancha','triangular','ancha','alargada',
 'mandibula_ancha','rombo','cuadrada','corazon','estrecha','alargada','rombo','redonda']

def head_layers(i,skin,hair,facew,top,cx):
 """Distinct 2D cartoon head contours, eyes, noses and expressions; no spherical shading."""
 ss,sb,sl=skin;hs,hb,hl=hair;kind=CAST[i][3];family=FACES[i];pts=FACE_POINTS[family]
 rear=Image.new('RGBA',(48,48));old.hair_back(rear,kind,hs,hb,hb)
 face=Image.new('RGBA',(48,48));m=Image.new('L',(48,48));draw(m).polygon(pts,fill=255)
 face.paste(color(ss),(0,0),m.filter(ImageFilter.MaxFilter(3)));face.paste(color(sb),(0,0),m)
 shadow=Image.new('L',(48,48));draw(shadow).polygon([(31,16),(38,14),(38,33),(25,33),(29,25)],fill=255)
 face.paste(color(ss),(0,0),ImageChops.multiply(m,shadow))
 left=min(x for x,y in pts);right=max(x for x,y in pts)
 for xx in [left,right]:
  oval(face,(xx-1,14,xx+1,18),ss);rect(face,(xx,15,xx,17),sb)
 # Eyebrow attitude and eye construction vary independently of identity and wardrobe.
 expression=i%6
 for ex in [17,28]:
  if expression in [0,3]:
   line(face,[(ex-1,11),(ex+2,10 if ex==17 else 11)],hs)
   line(face,[(ex,14),(ex+3,14)],'negro');rect(face,(ex+1,15,ex+2,15),'negro')
  elif expression in [1,4]:
   line(face,[(ex,9),(ex+3,10)],hs)
   oval(face,(ex,12,ex+3,16),'negro');rect(face,(ex+1,13,ex+2,15),'blanco');rect(face,(ex+2,14,ex+2,16),'negro')
  else:
   line(face,[(ex-1,10),(ex+2,11)],hs)
   line(face,[(ex,13),(ex+3,14)],'negro');rect(face,(ex+1,14,ex+1,15),'negro')
 # Caricatured nose: long bridge, broad tip, upturned or angular, with a single ink/shadow line.
 nose=i%4
 if nose==0:line(face,[(24,14),(24,19),(27,20),(23,20)],ss)
 elif nose==1:line(face,[(24,17),(26,19),(23,19)],ss)
 elif nose==2:line(face,[(23,18),(26,18),(27,20),(23,20)],ss)
 else:line(face,[(25,15),(27,19),(24,20)],ss)
 chin=max(y for x,y in pts);my=chin-6
 if expression in [1,3]:
  poly(face,[(20,my),(27,my),(26,my+3),(23,my+4),(21,my+2)],ss)
  line(face,[(22,my+1),(26,my+1)],'crema')
 elif expression in [0,4]:line(face,[(21,my),(24,my+1),(28,my-1)],ss)
 else:line(face,[(22,my),(26,my)],ss)
 old.hair_front(face,kind,hs,hb,hb)
 # Facial hair follows the new jaw rather than reimposing the previous round chin.
 acc=CAST[i][8]
 if acc in ['beard','glasses_beard']:
  beard=Image.new('L',(48,48));draw(beard).polygon([(13,19),(19,22),(23,21),(27,21),(34,19),(38,33),(10,33)],fill=255)
  face.paste(color(hs),(0,0),ImageChops.multiply(m,beard));line(face,[(21,my),(26,my+1)],hb)
 accessory=Image.new('RGBA',(48,80))
 old.accessories(accessory,'glasses' if acc=='glasses_beard' else ('none' if acc=='beard' else acc),sb,hs,hb)
 face.alpha_composite(accessory.crop((0,0,48,30)))
 ratio=facew/22;w=round(34*ratio);h=round(46*ratio)
 def place(img):
  cropped=img.crop((7,0,41,46)).resize((w,h),Image.Resampling.NEAREST)
  return cropped,(round(cx-w/2),top)
 return place(rear),place(face)

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
  xx=cx;yy=sy+17
  poly(details,[(xx,yy-6),(xx+2,yy-2),(xx+6,yy-2),(xx+3,yy+1),(xx+4,yy+6),(xx,yy+3),(xx-4,yy+6),(xx-3,yy+1),(xx-6,yy-2),(xx-2,yy-2)],'crema')
 elif kind=='blouse':
  poly(details,[(cx-9,sy-1),(cx-1,sy+4),(cx-6,sy+10)],'blanco');poly(details,[(cx+9,sy-1),(cx+1,sy+4),(cx+6,sy+10)],'blanco')
  for yy in range(round(sy+14),77,7):rect(details,(31,yy,32,yy),'gris-azul')
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

def render(i):
 entry=CAST[i];top,sw,ww,fw,lean,pose=ANATOMY[i];ps,pb,pl=old.SKINS[entry[5]];skin=(ps,pb,pl)
 hs,hb,hl=old.HAIR[entry[4]];cloth=entry[7];kind=entry[6];cx=32+lean;sy=top+round(max(y for x,y in FACE_POINTS[FACES[i]])*fw/22)+4
 im=Image.new('RGBA',SIZE)
 rear,face=head_layers(i,skin,(hs,hb,hl),fw,top,cx-1 if lean<0 else cx+1)
 im.paste(rear[0],rear[1],rear[0])
 shoulders=[(cx-sw/2+3,sy+3),(cx+sw/2-3,sy+4)]
 elbows=[(cx-sw/2-1,sy+17),(cx+sw/2+1,sy+18)]
 wrists=[(32-ww/2-2,73),(32+ww/2+2,73)]
 if pose in ['hip','hips']:
  elbows[1]=(min(56,cx+sw/2+8),sy+18);wrists[1]=(32+ww/2-2,68)
  if pose=='hips':elbows[0]=(max(5,cx-sw/2-8),sy+18);wrists[0]=(32-ww/2+2,68)
 if pose=='pocket':elbows[0]=(cx-sw/2-2,sy+18);wrists[0]=(25,72)
 if pose=='wave':elbows[1]=(min(56,cx+sw/2+7),sy+9);wrists[1]=(min(56,cx+sw/2+8),sy-9)
 if pose=='phone':elbows[1]=(min(56,cx+sw/2+6),sy+20);wrists[1]=(cx+15,sy+9)
 if pose=='chin':elbows[1]=(min(56,cx+sw/2+4),sy+24);wrists[1]=(cx+5,sy-5)
 if pose=='listen':elbows[1]=(min(56,cx+sw/2+8),sy+11);wrists[1]=(cx+13,top+16)
 if pose=='strap':elbows[0]=(max(5,cx-sw/2-4),sy+20);wrists[0]=(cx-10,sy+10)
 if pose=='cross':
  elbows=[(cx-sw/2-1,sy+23),(cx+sw/2+1,sy+23)];wrists=[(cx+11,sy+12),(cx-11,sy+15)]
 if pose=='clasp':elbows=[(cx-sw/2-2,sy+18),(cx+sw/2+2,sy+18)];wrists=[(30,69),(35,69)]
 sleeve=cloth
 if kind in ['varsity','vest']:sleeve=('gris-azul','gris-claro','blanco')
 # Upper arms behind the torso create shoulder sockets and honest gaps at bent elbows.
 for k in [0,1]:capsule(im,shoulders[k],elbows[k],9 if sw>35 else 8,sleeve)
 torso=mask_poly([(cx-5,sy-3),(cx+5,sy-3),(cx+sw/2-4,sy+2),(cx+sw/2-1,sy+8),(cx+sw*.4,sy+18),(32+ww/2,77),(32-ww/2,77),(cx-sw*.4,sy+18),(cx-sw/2+1,sy+8),(cx-sw/2+4,sy+2)])
 volume(im,torso,cloth)
 clothing(im,torso,cx,sy,ww,kind,cloth)
 capsule(im,(cx,top+23),(cx,sy+1),7,skin)
 # The neckline sits over the lower neck, with shadow under the jaw.
 line(im,[(cx-5,sy),(cx,sy+3),(cx+5,sy)],cloth[0],2)
 # Torso accessories: body-scaled, independent of pose and gender.
 acc=entry[8]
 if acc in ['chain','shells']:line(im,[(cx-6,sy),(cx-3,sy+6),(cx+3,sy+7),(cx+7,sy)],'ambar' if acc=='chain' else 'crema')
 if acc=='choker':line(im,[(cx-3,sy-5),(cx+3,sy-5)],'negro',2);rect(im,(cx,sy-5,cx+1,sy-4),'gris')
 if acc=='bow':poly(im,[(cx,sy+4),(cx-5,sy+1),(cx-5,sy+7),(cx,sy+5),(cx+5,sy+1),(cx+5,sy+7)],'rosa')
 if acc=='scarf':poly(im,[(cx-5,sy-3),(cx+5,sy-3),(cx+6,sy+2),(cx-1,sy+4),(cx-4,sy+13),(cx-7,sy+10),(cx-4,sy+2)],'ambar')
 if pose=='strap' or acc=='tote':line(im,[(cx-12,sy-1),(24,76)],'crema',3)
 im.paste(face[0],face[1],face[0])
 # Forearms are separate articulated parts. Bare forearms vary with the actual outfit.
 bare=kind in ['jersey','retro','band','hawaiian']
 for k in [0,1]:
  capsule(im,elbows[k],wrists[k],6 if bare else 7,skin if bare else sleeve)
  if not bare:
   a,b=elbows[k],wrists[k];u=.87;cut=(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u)
   line(im,[cut,b],sleeve[0],7)
  if pose=='pocket' and k==0:
   x,y=wrists[k];oval(im,(x-2,y-3,x+2,y),skin[1])
   line(im,[(x-4,y),(x+4,y)],cloth[0],2);line(im,[(x-3,y+1),(x+3,y+1)],cloth[2])
  else:hand(im,wrists[k],skin,'open' if pose=='wave' and k==1 else 'closed',1 if k==0 else -1)
 if pose=='phone':
  x,y=wrists[1];rounded(im,(x-2,y-9,x+3,y+1),'noche','negro',1);rect(im,(x-1,y-7,x+2,y-2),'gris-azul');rect(im,(x,y,x+1,y),'gris')
 if pose=='listen':
  x,y=wrists[1];rounded(im,(x-3,y-3,x+1,y+4),'pizarra','noche',1)
 return clean_isolated_pixels(im)

FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def text(im,p,t,size=22,c='gris-claro'):draw(im).text(p,t,font=ImageFont.truetype(FONT,size),fill=color(c))
def sheet(start,filename):
 out=Image.new('RGB',(1520,1510),color('negro'));text(out,(32,22),f'CLIENTES / CARTOON 2D / {start+1:02}—{start+12:02}',32,'crema')
 text(out,(32,68),'Tinta y color plano · sombras gráficas · rostros distintos · referencias sin integrar',20,'gris')
 for j in range(12):
  i=start+j;x=32+j%4*374;y=119+j//4*451
  text(out,(x,y),f'{i+1:02} {CAST[i][0]} / {CAST[i][1]}',23,'crema')
  text(out,(x,y+31),POSE_NAMES[ANATOMY[i][5]],18)
  bg=Image.new('RGB',(320,332),color('noche'));sprite=render(i).resize((256,320),Image.Resampling.NEAREST);bg.paste(sprite,(32,6),sprite)
  # Waist baseline makes true height variation visible, without scaling each portrait to fit.
  line(bg,[(12,322),(308,322)],'pizarra')
  out.paste(bg,(x,y+62));text(out,(x,y+401),f'{CAST[i][2]} · {FACES[i].replace("mandibula_ancha","mandíbula ancha").replace("corazon","corazón")}',17,'gris')
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
 out=Image.new('RGB',(1400,1580),color('negro'));text(out,(32,22),'CARTOON 2D / PRUEBA EN EL ESCENARIO',30,'crema')
 text(out,(32,67),'Misma escala y misma cintura · cuerpo de 64 px centrado · muestra sin interfaz',20,'gris')
 for j,i in enumerate([0,1,3,4,5,18]):
  x=32+j%2*680;y=120+j//2*480;text(out,(x,y),f'{i+1:02} {CAST[i][0]} / {POSE_NAMES[ANATOMY[i][5]]}',23,'crema')
  im=Image.new('RGB',(320,200),color('noche'));im.paste(env.dining_horizontal(),(0,0));person=render(i);im.paste(person,(128,46),person);im.paste(env.red_bar(),(0,122))
  sprite(im,'plato',145,120)
  for k,xx in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:sprite(im,k,xx,103)
  for k,xx in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:sprite(im,k,xx,139)
  sprite(im,'plancha',82,165);sprite(im,'charola',244,165);sprite(im,'basura',40,170)
  for k,xx,yy in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:sprite(im,k,xx,yy)
  out.paste(im.resize((640,400),Image.Resampling.NEAREST),(x,y+42))
 out.save(ROOT/'customers-cartoon-2d-context.png')

if __name__=='__main__':
 allowed={tuple(bytes.fromhex(h[1:])) for h in P.values()};manifest=[]
 for i in range(24):
  im=render(i);im.save(ROOT/f'customer-{i+1:02}-1x.png')
  assert all(a==0 or (r,g,b) in allowed for r,g,b,a in im.getdata())
  manifest.append({'id':i+1,'name':CAST[i][0],'style':CAST[i][1],'pronouns':CAST[i][2],'pose':POSE_NAMES[ANATOMY[i][5]],'anatomy':ANATOMY[i],'face_shape':FACES[i]})
 sheet(0,'customers-cartoon-2d-01-12.png');sheet(12,'customers-cartoon-2d-13-24.png');context_sheet()
 (ROOT/'cast.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print('24 cartoon 2D references, nine facial silhouettes; palette checked; no runtime writes.')
