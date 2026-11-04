"""Phase 2: native-pixel body/wardrobe/pose revision, preserving approved heads exactly."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import importlib.util,json,math,hashlib
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
PREVIOUS=ROOT.parent/'customers-jules-chema-2026-10-31'
spec=importlib.util.spec_from_file_location('approved_hair_and_faces',PREVIOUS/'generate.py')
rev=importlib.util.module_from_spec(spec);spec.loader.exec_module(rev)
heads=rev.approved;legacy=heads.base
P=heads.P;CAST=heads.CAST;ANATOMY=heads.ANATOMY;SIZE=(64,80)
col=heads.color;draw=heads.draw;line=heads.line;rect=heads.rect;poly=heads.poly;oval=heads.oval;rounded=heads.rounded;text=heads.text

def mask_poly(points):
 m=Image.new('L',SIZE);draw(m).polygon([(round(x),round(y)) for x,y in points],fill=255);return m

def flat(im,mask,ramp):
 """Uniform material fill with a single outline; no automatic right/bottom shadow planes."""
 edge=mask.filter(ImageFilter.MaxFilter(3));im.paste(col(ramp[0]),(0,0),edge);im.paste(col(ramp[1]),(0,0),mask)

def segment_mask(a,b,wa,wb):
 ax,ay=a;bx,by=b;length=max(1,math.hypot(bx-ax,by-ay));nx,ny=-(by-ay)/length,(bx-ax)/length
 m=mask_poly([(ax+nx*wa/2,ay+ny*wa/2),(bx+nx*wb/2,by+ny*wb/2),
  (bx-nx*wb/2,by-ny*wb/2),(ax-nx*wa/2,ay-ny*wa/2)])
 for (x,y),w in [(a,wa),(b,wb)]:
  r=max(1,(w-1)/2);draw(m).ellipse(tuple(round(v) for v in (x-r,y-r,x+r,y+r)),fill=255)
 return m

def limb(im,a,b,wa,wb,ramp):flat(im,segment_mask(a,b,wa,wb),ramp)
def between(a,b,t):return (a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t)
def point_toward(a,b,distance):
 length=max(1,math.dist(a,b));return between(a,b,min(1,distance/length))

def hand(im,p,skin,gesture='rest',thumb=1):
 x,y=map(round,p);ss,sb,sl=skin
 if gesture=='wave':
  rounded(im,(x-2,y-1,x+2,y+4),sb,ss,1)
  for dx,h in [(-3,3),(-1,5),(1,5),(3,3)]:
   line(im,[(x+dx,y),(x+dx,y-h)],sb)
   rect(im,(x+dx,y-h,x+dx,y-h),ss)
  line(im,[(x+2,y+2),(x+4,y)],ss,2);rect(im,(x+3,y+1,x+3,y+2),sb)
 elif gesture=='hip':
  poly(im,[(x-2,y-3),(x+2,y-3),(x+2,y+3),(x-2,y+3),(x-3*thumb,y)],ss)
  rect(im,(x-1,y-2,x+1,y+2),sb)
  line(im,[(x-1,y+1),(x+1,y+1)],ss)
 elif gesture=='chin':
  rounded(im,(x-2,y-2,x+2,y+2),sb,ss,1)
  line(im,[(x-4,y-2),(x,y-2)],ss,2)
  line(im,[(x-3,y-2),(x,y-2)],sb)
  line(im,[(x,y),(x+1,y)],ss)
 else:
  rounded(im,(x-2,y-2,x+2,y+3),sb,ss,1)
  tx=x+thumb*3;line(im,[(tx,y-1),(tx,y+1)],ss);rect(im,(x+thumb*2,y,x+thumb*2,y+1),sb)
  if gesture in ['grip','cross']:line(im,[(x-1,y+1),(x+1,y+1)],ss)
  elif gesture=='rest':line(im,[(x,y+1),(x,y+2)],ss)

def torso_mask(cx,sy,sw,ww):
 points=[(cx-4,sy-1),(cx+4,sy-1),(cx+sw/2-5,sy+2),(cx+sw/2-2,sy+7),
  (cx+sw/2-3,sy+13),(32+ww/2,77),(32-ww/2,77),
  (cx-sw/2+3,sy+13),(cx-sw/2+2,sy+7),(cx-sw/2+5,sy+2)]
 return mask_poly(points)

def garment(im,mask,cx,sy,ww,kind,ramp):
 shadow,base,light=ramp;d=Image.new('RGBA',SIZE);bottom=77
 if kind in ['flannel','overshirt','hawaiian','leather','cardigan','vest','blazer']:
  inner='noche' if kind=='leather' else 'gris-claro'
  poly(d,[(cx-4,sy+2),(cx+4,sy+2),(38,bottom),(26,bottom)],inner)
  # Matching plackets/collar rather than differently scaled panels on each side.
  for direction in [-1,1]:
   line(d,[(cx+direction*5,sy+3),(32+direction*6,bottom)],shadow)
  if kind in ['leather','blazer']:
   for sign in [-1,1]:
    poly(d,[(cx+sign*8,sy+2),(cx+sign*3,sy+8),(cx+sign*7,sy+12)],light if kind=='blazer' else 'pizarra')
   for sign in [-1,1]:line(d,[(cx+sign*9,sy+16),(cx+sign*13,sy+15)],shadow)
  elif kind in ['flannel','overshirt','hawaiian','cardigan']:
   for sign in [-1,1]:line(d,[(cx+sign*7,sy+2),(cx+sign*4,sy+6)],light)
  if kind=='flannel':
   plaid=Image.new('RGBA',SIZE)
   for yy in range(sy+10,78,7):line(plaid,[(cx-20,yy),(cx+20,yy)],light)
   for dx in [-13,13]:line(plaid,[(cx+dx,sy+6),(32+dx,77)],shadow)
   panel=mask_poly([(cx-20,sy),(cx-6,sy),(26,78),(8,78)])
   right=mask_poly([(cx+6,sy),(cx+20,sy),(56,78),(38,78)])
   panel=ImageChops.lighter(panel,right);plaid.putalpha(ImageChops.multiply(plaid.getchannel('A'),panel));d.alpha_composite(plaid)
  if kind in ['overshirt','vest']:
   for sign in [-1,1]:
    xx=cx+sign*10;yy=sy+12
    line(d,[(xx-2,yy),(xx+2,yy)],shadow)
    if kind=='overshirt':line(d,[(xx+2,yy),(xx+2,yy+4),(xx-2,yy+4),(xx-2,yy)],shadow)
  if kind=='hawaiian':
   for dx,dy in [(-11,12),(11,12),(-12,23),(12,23)]:
    x,y=cx+dx,sy+dy;line(d,[(x-1,y),(x+1,y)],'crema');line(d,[(x,y-1),(x,y+1)],'crema');rect(d,(x,y,x,y),'oxido')
 elif kind=='utility':
  line(d,[(cx,sy+5),(32,77)],shadow)
  for sign in [-1,1]:
   xx=cx+sign*10;yy=sy+11
   rounded(d,(xx-3,yy,xx+3,yy+5),None,shadow,1);line(d,[(xx-2,yy+1),(xx+2,yy+1)],light)
 elif kind in ['jersey','retro']:
  poly(d,[(cx-6,sy),(cx,sy+5),(cx+6,sy),(cx+5,sy+3),(cx,sy+7),(cx-5,sy+3)],'gris-claro')
  if kind=='retro':
   for sign in [-1,1]:line(d,[(cx+sign*9,sy+9),(32+sign*9,77)],'crema',2)
   for dx in [-2,2]:line(d,[(cx+dx,sy+11),(cx+dx,sy+17)],'crema')
  else:line(d,[(cx-2,sy+11),(cx+2,sy+11),(cx-1,sy+17)],'blanco')
  rounded(d,(cx+7,sy+8,cx+10,sy+12),'crema',shadow,1)
 elif kind=='hoodie':
  line(d,[(cx-7,sy),(cx,sy+6),(cx+7,sy)],shadow,2)
  line(d,[(cx-6,sy),(cx,sy+4),(cx+6,sy)],light)
  for sign in [-1,1]:line(d,[(cx+sign*3,sy+6),(cx+sign*3,sy+11)],'gris-claro')
  rounded(d,(24,67,40,75),base,shadow,2)
  line(d,[(27,69),(25,72)],light);line(d,[(37,69),(39,72)],light)
 elif kind in ['tech','rave','tracksuit']:
  line(d,[(cx,sy+2),(32,77)],light)
  if kind=='tech':
   for sign in [-1,1]:line(d,[(cx+sign*7,sy+10),(cx+sign*12,sy+8)],'gris-azul')
   rounded(d,(cx-12,sy+15,cx-7,sy+20),None,shadow,1)
  elif kind=='rave':
   for sign in [-1,1]:line(d,[(cx+sign*9,sy+6),(32+sign*10,77)],'cian')
   line(d,[(cx-10,sy+12),(cx+10,sy+12)],'cian')
  else:line(d,[(cx-14,sy+12),(cx+14,sy+12)],'gris-claro',2)
 elif kind=='varsity':
  line(d,[(cx,sy+4),(32,77)],shadow)
  for yy in range(sy+9,77,6):rect(d,(cx,yy,cx,yy),'crema')
  line(d,[(cx-10,sy+10),(cx-10,sy+15),(cx-6,sy+15)],'crema')
  line(d,[(cx-11,sy+2),(cx-3,sy+6)],'gris-claro');line(d,[(cx+11,sy+2),(cx+3,sy+6)],'gris-claro')
 elif kind=='band':
  yy=sy+11;rounded(d,(cx-7,yy,cx+7,yy+9),'pizarra',shadow,1)
  poly(d,[(cx-5,yy+7),(cx-2,yy+2),(cx,yy+5),(cx+3,yy+2),(cx+5,yy+7)],'gris-claro')
 elif kind=='sweater':
  yy=min(67,sy+11)
  poly(d,[(cx,yy-4),(cx+1,yy-1),(cx+4,yy-1),(cx+2,yy+1),(cx+3,yy+4),(cx,yy+2),(cx-3,yy+4),(cx-2,yy+1),(cx-4,yy-1),(cx-1,yy-1)],'crema')
 elif kind=='blouse':
  for sign in [-1,1]:poly(d,[(cx+sign*6,sy+1),(cx,sy+4),(cx+sign*4,sy+7)],'blanco')
  for yy in range(sy+10,77,5):rect(d,(cx,yy,cx,yy),'gris-azul')
 d.putalpha(ImageChops.multiply(d.getchannel('A'),mask));im.alpha_composite(d)

def geometry(i):
 top,sw,ww,fw,lean,pose=ANATOMY[i];cx=32+lean
 parts=heads.face_parts(i);chin=parts['chin'];sy=top+chin+4;head_x=cx-1 if lean<0 else cx+1
 shoulders=[(round(cx-sw/2+5),sy+5),(round(cx+sw/2-5),sy+5)]
 palms=[(round(32-ww/2-2),73),(round(32+ww/2+2),73)]
 elbows=[between(shoulders[k],palms[k],.5) for k in [0,1]]
 elbows=[(x+(-2 if k==0 else 2),y) for k,(x,y) in enumerate(elbows)]
 if pose in ['hip','hips']:
  palms[1]=(round(32+ww/2-2),69);elbows[1]=(min(57,cx+sw/2+4),min(70,sy+15))
  if pose=='hips':palms[0]=(round(32-ww/2+2),69);elbows[0]=(max(6,cx-sw/2-4),min(70,sy+15))
 if pose=='pocket':
  palms[0]=(27,70) if CAST[i][6]=='hoodie' else (round(32-ww/2+6),70)
  elbows[0]=(max(7,cx-sw/2-1),min(70,sy+13))
 if pose=='wave':elbows[1]=(min(56,cx+sw/2+5),sy+9);palms[1]=(min(56,cx+sw/2+5),sy-6)
 if pose=='phone':elbows[1]=(min(56,cx+sw/2+4),min(70,sy+17));palms[1]=(cx+15,sy+3)
 if pose=='chin':elbows[1]=(cx+10,min(71,sy+20));palms[1]=(head_x+5,top+chin+3)
 if pose in ['listen','goggles']:
  elbows[1]=(min(56,cx+22),top+round((27 if pose=='listen' else 22)*fw/22))
  palms[1]=(head_x+(13 if pose=='listen' else 10),top+(parts['eye_y']+3 if pose=='listen' else round(6*fw/22)))
 if pose=='strap':
  bx=cx-18;bag_y=66;start=(cx-11,sy+1);end=(bx+2,bag_y)
  py=min(sy+6,63);t=(py-start[1])/max(1,end[1]-start[1]);palms[0]=(round(start[0]+(end[0]-start[0])*t),py)
  elbows[0]=(max(7,cx-sw/2-1),min(71,sy+17))
 if pose=='cross':
  yy=min(71,sy+23);elbows=[(round(cx-sw/2),yy),(round(cx+sw/2),yy)]
  palms=[(cx+7,yy-12),(cx-7,yy-7)]
 if pose=='clasp':
  yy=min(70,sy+14);elbows=[(round(cx-sw/2),yy),(round(cx+sw/2),yy)]
  palms=[(cx-2,71),(cx+3,69)]
 elbows=[(round(max(6,min(57,x))),round(max(12,min(71,y)))) for x,y in elbows]
 palms=[tuple(map(round,p)) for p in palms]
 return {'top':top,'sw':sw,'ww':ww,'fw':fw,'pose':pose,'cx':cx,'sy':sy,'head_x':head_x,'shoulders':shoulders,'elbows':elbows,'palms':palms}

def render(i,without_head=False):
 g=geometry(i);cx,sy,sw,ww,pose=[g[k] for k in ['cx','sy','sw','ww','pose']]
 entry=CAST[i];skin=legacy.old.SKINS[entry[5]];cloth=entry[7];kind=entry[6];acc=entry[8]
 if i==18:cloth=('cafe-oscuro','canela','piel') # Distinguish workwear from Ros's darker skin.
 sleeve=('gris-azul','gris-claro','blanco') if kind in ['varsity','vest'] else cloth
 bare=kind in ['jersey','retro','band','hawaiian']
 shoulders,elbows,palms=g['shoulders'],g['elbows'],g['palms']
 im=Image.new('RGBA',SIZE)
 rear,face=heads.head_layers(i,skin,legacy.old.HAIR[entry[4]],g['fw'],g['top'],g['head_x'])
 if not without_head:im.paste(rear[0],rear[1],rear[0])
 for k in [0,1]:
  limb(im,shoulders[k],elbows[k],6,5,skin if bare else sleeve)
  if bare:limb(im,shoulders[k],between(shoulders[k],elbows[k],.45),7,6,sleeve)
 torso=torso_mask(cx,sy,sw,ww);flat(im,torso,cloth);garment(im,torso,cx,sy,ww,kind,cloth)
 # Neck is short, centred under the approved head, and flat-coloured.
 neck_x=g['head_x'];jaw_y=g['top']+heads.face_parts(i)['chin']
 neck=mask_poly([(neck_x-3,jaw_y),(neck_x+3,jaw_y),(cx+3,sy+1),(cx-3,sy+1)])
 flat(im,neck,skin)
 line(im,[(cx-4,sy-1),(cx-3,sy+2),(cx+3,sy+2),(cx+4,sy-1)],cloth[0])
 if acc in ['chain','shells']:
  line(im,[(cx-5,sy),(cx-3,sy+4),(cx,sy+5),(cx+3,sy+4),(cx+5,sy)],'ambar' if acc=='chain' else 'crema')
 if acc=='choker':line(im,[(neck_x-3,sy-2),(neck_x+3,sy-2)],'negro');rect(im,(neck_x,sy-2,neck_x,sy-2),'gris')
 if acc=='bow':poly(im,[(cx,sy+5),(cx-4,sy+3),(cx-4,sy+7),(cx,sy+5),(cx+4,sy+3),(cx+4,sy+7)],'rosa')
 if acc=='scarf':
  poly(im,[(cx-4,sy-1),(cx+4,sy-1),(cx+4,sy+3),(cx,sy+5),(cx-4,sy+2)],'ambar')
  poly(im,[(cx-1,sy+3),(cx+1,sy+4),(cx-2,sy+12),(cx-4,sy+10)],'tostado')
 if pose=='strap':
  bx=cx-18;by=66
  rounded(im,(bx,by,bx+11,77),'crema','canela',1)
  line(im,[(bx+2,75),(bx+9,75)],'canela')
  line(im,[(cx-11,sy+1),(bx+2,by)],'canela',3)
  line(im,[(cx-11,sy+1),(bx+2,by)],'crema')
  line(im,[(cx-11,sy+1),(bx+9,by)],'canela')
 if not without_head:im.paste(face[0],face[1],face[0])
 # Forearms taper into cuffs. The hand begins AFTER the sleeve, not as a block on top of it.
 for k in [0,1]:
  elbow,palm=elbows[k],palms[k]
  cuff=point_toward(palm,elbow,3)
  limb(im,elbow,cuff,5 if bare else 6,4,skin if bare else sleeve)
  if not bare:
   # A small transverse cuff seam, rather than a second ring around the entire hand.
   dx,dy=palm[0]-elbow[0],palm[1]-elbow[1];length=max(1,math.hypot(dx,dy));nx,ny=-dy/length,dx/length
   line(im,[(cuff[0]-nx*2,cuff[1]-ny*2),(cuff[0]+nx*2,cuff[1]+ny*2)],cloth[2] if kind=='utility' else sleeve[0])
  if pose=='pocket' and k==0:
   x,y=palm;rect(im,(x-1,y-1,x+1,y+1),skin[1])
   line(im,[(x-3,y+2),(x+3,y)],cloth[0]);line(im,[(x-2,y+3),(x+3,y+1)],cloth[1])
  elif pose=='phone' and k==1:
   x,y=palm;hand(im,palm,skin,'grip',-1)
   rounded(im,(x-2,y-9,x+3,y+1),'noche','negro',1)
   rect(im,(x-1,y-7,x+2,y-2),'gris-azul')
   line(im,[(x-3,y),(x,y)],skin[1],2);rect(im,(x+3,y-1,x+3,y),skin[1])
  elif pose=='wave' and k==1:hand(im,palm,skin,'wave')
  elif pose=='chin' and k==1:hand(im,palm,skin,'chin',-1)
  elif pose in ['hip','hips'] and (k==1 or pose=='hips'):hand(im,palm,skin,'hip',-1 if k==1 else 1)
  else:hand(im,palm,skin,'cross' if pose=='cross' else 'grip' if pose in ['strap','chin','clasp','listen','goggles'] else 'rest',1 if k==0 else -1)
 if pose=='clasp':line(im,[(cx,69),(cx+1,71)],skin[0])
 return im


def sheet(start):
 out=Image.new('RGB',(1520,1510),col('negro'))
 text(out,(32,22),f'FASE 2 / CUERPOS REVISADOS / {start+1:02}—{start+12:02}',31,'crema')
 text(out,(32,68),'Color plano · brazos y manos más claros · cabezas aprobadas conservadas',20,'gris')
 for j in range(12):
  i=start+j;x=32+j%4*374;y=119+j//4*451
  text(out,(x,y),f'{i+1:02} {CAST[i][0]} / {CAST[i][1]}',23,'crema')
  text(out,(x,y+31),legacy.POSE_NAMES[ANATOMY[i][5]].replace('entrelazadas','juntas'),18)
  bg=Image.new('RGB',(320,332),col('noche'));piece=render(i).resize((256,320),Image.Resampling.NEAREST)
  bg.paste(piece,(32,6),piece);line(bg,[(12,322),(308,322)],'pizarra');out.paste(bg,(x,y+62))
  text(out,(x,y+401),f'{CAST[i][2]} · {heads.base.FACE_LABELS[heads.base.FACES[i]]}',16,'gris')
 out.save(ROOT/f'customers-body-review-{start+1:02}-{start+12:02}.png')

def comparison_sheet():
 out=Image.new('RGB',(1520,850),col('negro'))
 text(out,(32,22),'CUERPOS / ANTES Y REVISADOS',31,'crema')
 text(out,(32,68),'Mismas cabezas y escala · cambios en anatomía, ropa, manos y apoyos',20,'gris')
 for j,i in enumerate([0,3,11,14,15,18,22,23]):
  x=32+j%4*374;y=116+j//4*355
  text(out,(x,y),f'{i+1:02} {CAST[i][0]}',24,'crema')
  for k,(label,piece) in enumerate([('ANTES',Image.open(PREVIOUS/f'customer-{i+1:02}-1x.png')),('REVISADO',render(i))]):
   xx=x+k*164;text(out,(xx,y+38),label,16,'gris')
   bg=Image.new('RGB',(152,172),col('noche'));piece=piece.resize((128,160),Image.Resampling.NEAREST)
   bg.paste(piece,(12,4),piece);out.paste(bg,(xx,y+66))
 out.save(ROOT/'bodies-before-after.png')

def context_sheet():
 spec=importlib.util.spec_from_file_location('approved_dining_room',REPO/'scripts/sprites/environment_gen.py')
 env=importlib.util.module_from_spec(spec);spec.loader.exec_module(env)
 definitions=json.loads((ROOT.parent/'kitchen-2026-10-31/source-sprites.json').read_text())
 def sprite(im,key,x,y):
  d=definitions['sprites'][key];piece=Image.new('RGBA',(d['width'],d['height']))
  for yy,row in enumerate(d['frames'][0]):
   for xx,k in enumerate(row):
    if k!='.':piece.putpixel((xx,yy),tuple(bytes.fromhex(P[d['colors'][k]][1:]))+(255,))
  im.paste(piece,(x,y),piece)
 out=Image.new('RGB',(1400,1580),col('negro'))
 text(out,(32,22),'CUERPOS REVISADOS / PRUEBA EN EL ESCENARIO',30,'crema')
 text(out,(32,67),'Misma escala y misma cintura · seis poses · referencias sin integrar',20,'gris')
 for j,i in enumerate([0,3,11,14,15,18]):
  x=32+j%2*680;y=120+j//2*480;text(out,(x,y),f'{i+1:02} {CAST[i][0]}',23,'crema')
  im=Image.new('RGB',(320,200),col('noche'));im.paste(env.dining_horizontal(),(0,0))
  person=render(i);im.paste(person,(128,46),person);im.paste(env.red_bar(),(0,122))
  sprite(im,'plato',145,120)
  for k,xx in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:sprite(im,k,xx,103)
  for k,xx in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:sprite(im,k,xx,139)
  sprite(im,'plancha',82,165);sprite(im,'charola',244,165);sprite(im,'basura',40,170)
  for k,xx,yy in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:sprite(im,k,xx,yy)
  out.paste(im.resize((640,400),Image.Resampling.NEAREST),(x,y+42))
 out.save(ROOT/'customers-body-review-context.png')

def validate_artifacts():
 allowed={tuple(bytes.fromhex(h[1:])) for h in P.values()};rows=[];digests=set()
 for i in range(24):
  im=render(i);g=geometry(i);parts=heads.face_parts(i)
  old_head=Image.open(PREVIOUS/f'face-{i+1:02}-1x.png').convert('RGBA')
  assert heads.portrait(i).tobytes()==old_head.tobytes(),f'{i+1}: approved head changed'
  assert im.size==(64,80)
  assert all(a in (0,255) and (not a or (r,gg,b) in allowed) for r,gg,b,a in im.getdata())
  l,t,r,b=im.getbbox();assert l>0 and t>0 and r<64 and b<80,f'{i+1}: clipped silhouette'
  digest=hashlib.sha256(im.tobytes()).hexdigest();assert digest not in digests;digests.add(digest)
  # The body cannot paint over central facial features, even when a hand touches a head accessory.
  for y in range(parts['eye_y']-2,parts['chin']+1):
   for x in range(17,32):
    px=old_head.getpixel((x,y))
    if not px[3]:continue
    gx=g['head_x']-24+x;gy=g['top']+y
    assert im.getpixel((gx,gy))==px,f'{i+1}: body covered face at {(x,y)}'
  # No disconnected sleeve, finger, collar or prop fragments.
  opaque={(x,y) for y in range(80) for x in range(64) if im.getpixel((x,y))[3]}
  todo=[next(iter(opaque))];seen=set(todo)
  while todo:
   x,y=todo.pop()
   for dx in [-1,0,1]:
    for dy in [-1,0,1]:
     q=x+dx,y+dy
     if q in opaque and q not in seen:seen.add(q);todo.append(q)
  assert seen==opaque,f'{i+1}: floating pixels/components'
  assert im.tobytes()!=Image.open(PREVIOUS/f'customer-{i+1:02}-1x.png').convert('RGBA').tobytes()
  rows.append({'id':i+1,'name':CAST[i][0],'pose':g['pose'],'head_unchanged':True,'central_face_unobscured':True,
   'palette_size_transparency':True,'no_clipping':True,'one_connected_silhouette':True,'body_revised':True})
 return rows

if __name__=='__main__':
 checks=validate_artifacts()
 for i in range(24):
  render(i).save(ROOT/f'customer-{i+1:02}-1x.png')
  heads.portrait(i).save(ROOT/f'face-{i+1:02}-1x.png')
 sheet(0);sheet(12);comparison_sheet();context_sheet()
 (ROOT/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 print('24/24 cuerpos revisados: cabezas idénticas, facciones sin tapar, paleta y márgenes correctos, siluetas conectadas.')
