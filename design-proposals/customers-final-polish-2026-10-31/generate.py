"""Phase 2: native-pixel body/wardrobe/pose revision, preserving approved heads exactly."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import importlib.util,json,math,hashlib
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
PREVIOUS=ROOT.parent/'customers-jules-chema-2026-10-31'
spec=importlib.util.spec_from_file_location('approved_hair_and_faces',PREVIOUS/'generate.py')
rev=importlib.util.module_from_spec(spec);spec.loader.exec_module(rev)
heads=rev.approved;legacy=heads.base
P=heads.P;CAST=heads.CAST;SIZE=(64,80)
# Keep a subtle weight shift: at most one native pixel between chest centre and waist.
# The approved head shape is unchanged and now sits directly above the neck/shoulder axis.
ANATOMY=[(top,sw,ww,fw,1 if lean>0 else -1 if lean<0 else 0,pose)
 for top,sw,ww,fw,lean,pose in heads.ANATOMY]
col=heads.color;draw=heads.draw;line=heads.line;rect=heads.rect;poly=heads.poly;oval=heads.oval;rounded=heads.rounded;text=heads.text
BASELINE=ROOT.parent/'customers-natural-gestures-2026-10-31'
CROWN_IDS={0,1,2,6,7,9,11,17,19,20,23}
OLD_PARTS=heads.face_parts

def refined_head_parts(i):
 parts=OLD_PARTS(i)
 if i==5:
  # A pink crest with a clear swept silhouette, without the old square temple patches.
  front=Image.new('RGBA',heads.HEAD_SIZE);m=Image.new('L',heads.HEAD_SIZE)
  draw(m).polygon([(19,6),(19,4),(21,3),(21,1),(24,2),(25,0),
   (28,3),(30,4),(31,6),(28,7),(24,7)],fill=255)
  front.paste(col('ciruela'),(0,0),m.filter(ImageFilter.MaxFilter(3)))
  front.paste(col('magenta'),(0,0),m)
  line(front,[(21,5),(23,4),(24,5),(27,5),(29,6)],'rosa')
  parts['hair']=front;parts['rear']=Image.new('RGBA',heads.HEAD_SIZE)
 if i in CROWN_IDS or i==5:
  covered=ImageChops.lighter(parts['rear'].getchannel('A'),parts['hair'].getchannel('A'))
  covered=ImageChops.lighter(covered,parts['accessories'].getchannel('A'))
  core=parts['core'].copy()
  for y in range(5 if i==5 else 7):
   for x in range(48):
    if not covered.getpixel((x,y)):core.putpixel((x,y),(0,0,0,0))
  parts['core']=core
 return parts

heads.face_parts=refined_head_parts

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
  # A small open palm: grouped fingers share one compact silhouette at native scale.
  shape=Image.new('L',SIZE)
  draw(shape).polygon([(x-2,y+1),(x-2,y-3),(x-1,y-4),(x,y-5),
   (x+1,y-4),(x+2,y-3),(x+2,y-1),(x+3,y-2),(x+3,y),
   (x+1,y+2),(x-1,y+2)],fill=255)
  flat(im,shape,skin)
  rect(im,(x-1,y-4,x-1,y-2),ss)
  rect(im,(x+1,y-3,x+1,y-2),ss)
  rect(im,(x+1,y,x+1,y),ss)
 elif gesture=='hip':
  poly(im,[(x-2,y-3),(x+2,y-3),(x+2,y+3),(x-2,y+3),(x-3*thumb,y)],ss)
  rect(im,(x-1,y-2,x+1,y+2),sb)
  line(im,[(x-1,y+1),(x+1,y+1)],ss)
 elif gesture=='chin':
  # Folded fingers support the underside of the chin; no finger climbs up the cheek.
  shape=mask_poly([(x-3,y-2),(x,y-2),(x+2,y-1),(x+2,y+1),
   (x+1,y+2),(x-1,y+2),(x-2,y)])
  flat(im,shape,skin)
  line(im,[(x-2,y-1),(x,y-1)],sl)
  line(im,[(x-2,y),(x,y)],ss)
  rect(im,(x+1,y+1,x+1,y+1),ss)

 else:
  rounded(im,(x-2,y-2,x+2,y+3),sb,ss,1)
  tx=x+thumb*3;line(im,[(tx,y-1),(tx,y+1)],ss);rect(im,(x+thumb*2,y,x+thumb*2,y+1),sb)
  if gesture in ['grip','cross']:line(im,[(x-1,y+1),(x+1,y+1)],ss)
  elif gesture=='rest':line(im,[(x,y+1),(x,y+2)],ss)

def unified_arm(shoulder,elbow,cuff,width=6,relaxed=False):
 if relaxed:
  # Fuller elbow and a softly bowed forearm, narrowing only near the wrist.
  upper=segment_mask(shoulder,elbow,width,width)
  fore=Image.new('L',SIZE)
  for j in range(8):
   t0=j/8;t1=(j+1)/8
   def curve(t):
    x,y=between(elbow,cuff,t);return (x,y+1.5*4*t*(1-t))
   fore=ImageChops.lighter(fore,segment_mask(curve(t0),curve(t1),
    width-(width-4.5)*t0,width-(width-4.5)*t1))
  return ImageChops.lighter(upper,fore),fore
 upper=segment_mask(shoulder,elbow,width,width-1)
 middle=between(elbow,cuff,.5)
 middle=(middle[0],middle[1]+(.7 if relaxed else 0))
 taper=3 if width==5 else 4
 fore=ImageChops.lighter(segment_mask(elbow,middle,width-1,width-1.3),
  segment_mask(middle,cuff,width-1.3,taper))
 return ImageChops.lighter(upper,fore),fore

def wave_arm(shoulder,elbow,cuff):
 # Replace the circular elbow cap with a slim, continuous rounded bend.
 start=point_toward(elbow,shoulder,3);end=point_toward(elbow,cuff,3)
 upper=segment_mask(shoulder,start,6,4.5);fore=Image.new('L',SIZE)
 def curve(t):return tuple((1-t)**2*start[k]+2*(1-t)*t*elbow[k]+t*t*end[k] for k in [0,1])
 for j in range(6):fore=ImageChops.lighter(fore,segment_mask(curve(j/6),curve((j+1)/6),4.5,4.5))
 fore=ImageChops.lighter(fore,segment_mask(end,cuff,4.5,4))
 return ImageChops.lighter(upper,fore),fore

def overlay_continuous(im,whole,region,ramp):
 # Only the OUTSIDE edge of the whole arm may be inked. Never outline the elbow cap.
 visible=region.filter(ImageFilter.MaxFilter(3))
 outer=ImageChops.multiply(whole.filter(ImageFilter.MaxFilter(3)),visible)
 fill=ImageChops.multiply(whole,visible)
 im.paste(col(ramp[0]),(0,0),outer);im.paste(col(ramp[1]),(0,0),fill)

def hand_shape(p,elbow,gesture,thumb):
 x,y=p;length=max(1,math.dist(elbow,p));tx,ty=(x-elbow[0])/length,(y-elbow[1])/length
 nx,ny=-ty,tx
 def point(across,along):return (x+nx*across+tx*along,y+ny*across+ty*along)
 m=Image.new('L',SIZE);details=Image.new('L',SIZE)
 if gesture=='cross_rest':
  # Visible palm lying on the opposite upper arm, with four grouped relaxed fingers.
  m=mask_poly([(x-3,y-1),(x,y-2),(x+2,y-1),(x+3,y+1),(x+2,y+2),(x-1,y+2),(x-3,y)])
  draw(details).line([(round(x),round(y+1)),(round(x+2),round(y+1))],fill=255)
 elif gesture=='cross_tucked':
  # Only the curled fingertips remain visible under the opposite arm.
  m=mask_poly([(x-2,y-1),(x+1,y-1),(x+1,y+1),(x-1,y+2),(x-2,y+1)])
  draw(details).point((round(x),round(y)),fill=255)
 elif gesture in ['rest','grip','clasp']:
  # The wrist and fingers follow the forearm; horizontal arms no longer end in vertical blocks.
  points=[point(-1,-2),point(1,-2),point(1.5,0),point(1,2),point(-1,2),point(-1.5,0)]
  m=mask_poly(points)
  bump=tuple(map(round,point(2*thumb,0)));draw(m).point(bump,fill=255)
  if gesture!='rest':draw(details).point(tuple(map(round,point(0,1))),fill=255)
 else:
  # Specialized gestures retain their readable finger silhouettes.
  temp=Image.new('RGBA',SIZE);hand(temp,p,('negro','blanco','gris'),gesture,thumb)
  m=Image.new('L',SIZE)
  # Convert the pre-existing contour into a native mask; details remain separate from the arm.
  for yy in range(80):
   for xx in range(64):
    r,g,b,a=temp.getpixel((xx,yy))
    if a and (r,g,b)==(255,255,255):m.putpixel((xx,yy),255)
  if gesture=='hip':draw(details).line([(round(x-1),round(y+1)),(round(x+1),round(y+1))],fill=255)
 return m,details

def rebalance_elbow(s,p,e,cx,side,raised=False):
 # Keep the intended pose while rejecting excessively short forearms and stretched upper arms.
 best=None
 for dx in range(-6,7):
  for dy in range(-6,7):
   q=(e[0]+dx,e[1]+dy)
   if not (6<=q[0]<=57 and 8<=q[1]<=71):continue
   if side==0 and q[0]>cx-6:continue
   if side==1 and q[0]<cx+6:continue
   if not raised and q[1]<s[1]:continue
   upper=math.dist(s,q);fore=math.dist(q,p)-3
   if upper<5 or fore<4:continue
   ratio=fore/upper
   penalty=180*(max(0,.65-ratio)**2+max(0,ratio-1.35)**2)
   penalty+=.12*(dx*dx+dy*dy)
   penalty+=max(0,upper-23)**2+max(0,fore-25)**2
   if best is None or penalty<best[0]:best=(penalty,q)
 return best[1] if best else e

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
  if kind=='retro':
   for sign in [-1,1]:line(d,[(cx+sign*9,sy+9),(32+sign*9,77)],'crema',2)
   for dx in [-2,2]:line(d,[(cx+dx,sy+11),(cx+dx,sy+17)],'crema')
  else:line(d,[(cx-2,sy+11),(cx+2,sy+11),(cx-1,sy+17)],'blanco')
  rounded(d,(cx+7,sy+8,cx+10,sy+12),'crema',shadow,1)
 elif kind=='hoodie':
  rounded(d,(24,67,40,75),base,shadow,2)
  line(d,[(27,69),(25,72)],light);line(d,[(37,69),(39,72)],light)
 elif kind in ['tech','rave','tracksuit']:
  line(d,[(cx,sy+2),(32,77)],light)
  if kind=='tech':
   # The former low chest pocket overlapped the upper arm, leaving a detached bracket line.
   # Keep only short chest tabs inside the torso, well away from both sleeves.
   for sign in [-1,1]:line(d,[(cx+sign*4,sy+10),(cx+sign*6,sy+10)],'gris-azul')
  elif kind=='rave':
   for sign in [-1,1]:line(d,[(cx+sign*9,sy+6),(32+sign*10,77)],'cian')
   line(d,[(cx-10,sy+12),(cx+10,sy+12)],'cian')
  else:line(d,[(cx-14,sy+12),(cx+14,sy+12)],'gris-claro',2)
 elif kind=='varsity':
  line(d,[(cx,sy+4),(32,77)],shadow)
  for yy in range(sy+9,77,6):rect(d,(cx,yy,cx,yy),'crema')
  line(d,[(cx-10,sy+10),(cx-10,sy+15),(cx-6,sy+15)],'crema')
 elif kind=='band':
  yy=sy+11;rounded(d,(cx-7,yy,cx+7,yy+9),'pizarra',shadow,1)
  poly(d,[(cx-5,yy+7),(cx-2,yy+2),(cx,yy+5),(cx+3,yy+2),(cx+5,yy+7)],'gris-claro')
 elif kind=='sweater':
  yy=min(67,sy+11)
  poly(d,[(cx,yy-4),(cx+1,yy-1),(cx+4,yy-1),(cx+2,yy+1),(cx+3,yy+4),(cx,yy+2),(cx-3,yy+4),(cx-2,yy+1),(cx-4,yy-1),(cx-1,yy-1)],'crema')
 elif kind=='blouse':
  for yy in range(sy+10,77,5):rect(d,(cx,yy,cx,yy),'gris-azul')
 d.putalpha(ImageChops.multiply(d.getchannel('A'),mask));im.alpha_composite(d)

def neckline(im,cx,sy,jaw_y,kind,skin,cloth):
 """One coherent neck opening per garment; no generic collar painted over a specific one."""
 ss,sb,_=skin;shadow,base,light=cloth
 # The approved head covers the upper end; there is no horizontal skin-outline cap below it.
 poly(im,[(cx-3,jaw_y),(cx+3,jaw_y),(cx+3,sy),(cx+2,sy+2),
  (cx-2,sy+2),(cx-3,sy)],sb)
 line(im,[(cx-3,jaw_y+1),(cx-3,sy)],ss)
 line(im,[(cx+3,jaw_y+1),(cx+3,sy)],ss)
 def crew(edge):
  line(im,[(cx-4,sy-1),(cx-4,sy+1),(cx-2,sy+3),(cx+2,sy+3),
   (cx+4,sy+1),(cx+4,sy-1)],edge)
 if kind in ['jersey','retro']:
  poly(im,[(cx-3,sy-1),(cx+3,sy-1),(cx,sy+3)],sb)
  line(im,[(cx-4,sy-1),(cx,sy+4),(cx+4,sy-1)],'gris-claro')
 elif kind in ['tech','tracksuit','rave']:
  rounded(im,(cx-5,sy-2,cx+5,sy+3),base,shadow,1)
  rect(im,(cx-2,sy-2,cx+2,sy),sb)
  line(im,[(cx,sy+1),(cx,sy+4)],light)
 elif kind=='varsity':
  crew(shadow)
  line(im,[(cx-4,sy),(cx-2,sy+2),(cx+2,sy+2),(cx+4,sy)],'gris-claro')
 elif kind=='hoodie':
  # A connected hood follows both shoulders and joins at the same central opening.
  line(im,[(cx-6,sy-2),(cx-8,sy+1),(cx-6,sy+5),(cx-3,sy+5)],shadow)
  line(im,[(cx+6,sy-2),(cx+8,sy+1),(cx+6,sy+5),(cx+3,sy+5)],shadow)
  crew(shadow)
  for sign in [-1,1]:line(im,[(cx+sign*3,sy+5),(cx+sign*3,sy+10)],'gris-claro')
 elif kind in ['leather','blazer']:
  crew('pizarra' if kind=='leather' else 'gris-azul')
  for sign in [-1,1]:
   lapel=[(cx+sign*4,sy-1),(cx+sign*8,sy+2),(cx+sign*5,sy+6),
    (cx+sign*7,sy+9),(cx+sign*5,sy+12),(cx+sign*2,sy+5)]
   poly(im,lapel,'pizarra' if kind=='leather' else shadow)
   line(im,[(cx+sign*4,sy-1),(cx+sign*2,sy+5),(cx+sign*5,sy+12)],shadow)
 elif kind in ['flannel','overshirt','hawaiian','utility']:
  if kind!='utility':crew('gris-azul')
  else:
   poly(im,[(cx-3,sy-1),(cx+3,sy-1),(cx,sy+3)],sb)
   line(im,[(cx-3,sy),(cx,sy+3),(cx+3,sy)],shadow)
  for sign in [-1,1]:
   # The collar begins at the neck and continues into the shirt placket.
   poly(im,[(cx+sign*3,sy-1),(cx+sign*7,sy+2),(cx+sign*5,sy+6),(cx+sign*2,sy+2)],base)
   line(im,[(cx+sign*3,sy-1),(cx+sign*2,sy+2),(cx+sign*5,sy+6),(cx+sign*7,sy+2)],shadow)
 elif kind=='cardigan':
  crew('gris-azul')
  for sign in [-1,1]:line(im,[(cx+sign*5,sy-1),(cx+sign*6,sy+5),(cx+sign*6,sy+10)],shadow)
 elif kind=='vest':
  crew('gris-azul')
  for sign in [-1,1]:line(im,[(cx+sign*6,sy),(cx+sign*3,sy+6),(cx+sign*3,sy+10)],shadow)
 elif kind=='blouse':
  crew('gris-azul')
  for sign in [-1,1]:
   poly(im,[(cx+sign*3,sy),(cx+sign*6,sy+2),(cx+sign*4,sy+5),(cx+sign,sy+3)],'blanco')
   line(im,[(cx+sign*6,sy+2),(cx+sign*4,sy+5),(cx+sign,sy+3)],'gris-azul')
 else:crew(shadow)

def geometry(i):
 top,sw,ww,fw,lean,pose=ANATOMY[i];cx=32+lean
 if i==9:sw,ww=36,30
 if i==23:sw,ww=35,30 # Shorter, broader character: arms must fit the available torso height.
 parts=heads.face_parts(i);chin=parts['chin'];sy=top+chin+4;head_x=cx
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
 if pose=='chin':
  elbows[1]=(cx+12,min(70,sy+20));palms[1]=(head_x+6,top+chin+2)
  # The other hand supports the raised elbow, making the thoughtful gesture legible.
  elbows[0]=(round(cx-sw/2+4),min(71,sy+23))
  palms[0]=(cx+9,min(71,sy+22))
 if pose in ['listen','goggles']:
  elbows[1]=(min(56,cx+22),top+round((27 if pose=='listen' else 22)*fw/22))
  palms[1]=(head_x+(13 if pose=='listen' else 10),top+(parts['eye_y']+3 if pose=='listen' else round(6*fw/22)))
 if pose=='strap':
  bx=cx-18;bag_y=66;start=(cx-11,sy+1);end=(bx+2,bag_y)
  py=min(sy+6,63);t=(py-start[1])/max(1,end[1]-start[1]);palms[0]=(round(start[0]+(end[0]-start[0])*t),py)
  elbows[0]=(max(7,cx-sw/2-1),min(71,sy+17))
 if pose=='cross':
  # Fold low across the torso: broad, nearly horizontal forearms instead of a thin X.
  elbows=[(round(cx-sw/2+4),sy+24),(round(cx+sw/2-4),sy+25)]
  palms=[(round(cx+sw/2-5),sy+17),(round(cx-sw/2+6),sy+22)]
 if pose=='clasp':
  yy=min(70,sy+14);elbows=[(round(cx-sw/2),yy),(round(cx+sw/2),yy)]
  palms=[(cx-2,71),(cx+3,69)]
 elbows=[(round(max(6,min(57,x))),round(max(12,min(71,y)))) for x,y in elbows]
 palms=[tuple(map(round,p)) for p in palms]
 if pose not in ['cross','chin']:
  elbows=[rebalance_elbow(shoulders[k],palms[k],elbows[k],cx,k,pose in ['listen','goggles'] and k==1) for k in [0,1]]
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
 arms=[]
 for k in [0,1]:
  gesture=('wave' if pose=='wave' and k==1 else 'chin' if pose=='chin' and k==1 else
   'hip' if pose in ['hip','hips'] and (k==1 or pose=='hips') else
   ('cross_rest' if k==0 else 'cross_tucked') if pose=='cross' else 'clasp' if pose=='clasp' else
   'grip' if pose in ['strap','listen','goggles','phone'] and (k==0 if pose=='strap' else k==1) else 'rest')
  cuff=point_toward(palms[k],elbows[k],3)
  width=7 if pose=='cross' else 5 if bare else 6
  whole,fore=unified_arm(shoulders[k],elbows[k],cuff,width,relaxed=pose=='cross')
  if pose=='wave' and k==1:whole,fore=wave_arm(shoulders[k],elbows[k],cuff)
  hm,hd=hand_shape(palms[k],elbows[k],gesture,1 if k==0 else -1)
  if pose=='pocket' and k==0:
   hm=Image.new('L',SIZE);hd=Image.new('L',SIZE)
   xx,yy=palms[k];draw(hm).rectangle((xx-1,yy-1,xx+1,yy+1),fill=255)
  if bare:whole=ImageChops.lighter(whole,hm)
  arms.append({'whole':whole,'fore':fore,'hand':hm,'detail':hd,'gesture':gesture})
  flat(im,whole,skin if bare else sleeve)
  if bare:limb(im,shoulders[k],between(shoulders[k],elbows[k],.40 if pose=='cross' else .45),9 if pose=='cross' else 7,8 if pose=='cross' else 6,sleeve)
 torso=torso_mask(cx,sy,sw,ww)
 if i==9:
  # Separate the fitted chest from the short sleeves; the arms supply the sleeve caps.
  torso=mask_poly([(cx-4,sy-1),(cx+4,sy-1),(cx+10,sy+2),
   (cx+12,sy+7),(cx+11,sy+14),(32+ww/2-1,77),
   (32-ww/2+1,77),(cx-11,sy+14),(cx-12,sy+7),(cx-10,sy+2)])
 flat(im,torso,cloth);garment(im,torso,cx,sy,ww,kind,cloth)
 if i==9:
  for sign in [-1,1]:
   s=shoulders[0 if sign==-1 else 1];e=elbows[0 if sign==-1 else 1]
   x,y=between(s,e,.40)
   line(im,[(x-3,y),(x+3,y+1)],cloth[0])
 # Collar/neck is drawn once, in front of the garment, and before accessories/head.
 neck_x=g['head_x'];jaw_y=g['top']+heads.face_parts(i)['chin']
 neckline(im,cx,sy,jaw_y,kind,skin,cloth)
 if acc in ['chain','shells']:
  line(im,[(cx-5,sy),(cx-3,sy+4),(cx,sy+5),(cx+3,sy+4),(cx+5,sy)],'ambar' if acc=='chain' else 'crema')
 if acc=='choker':line(im,[(neck_x-3,sy-2),(neck_x+3,sy-2)],'negro');rect(im,(neck_x,sy-2,neck_x,sy-2),'gris')
 if acc=='bow':poly(im,[(cx,sy+5),(cx-4,sy+3),(cx-4,sy+7),(cx,sy+5),(cx+4,sy+3),(cx+4,sy+7)],'rosa')
 if acc=='scarf':
  # A rust neckerchief with a pointed fold, side knot and two short tapered tails.
  poly(im,[(cx-4,sy-1),(cx+3,sy-1),(cx+4,sy+2),(cx,sy+6),
   (cx-4,sy+2)],'oxido')
  line(im,[(cx-4,sy-1),(cx-2,sy+2),(cx,sy+3),(cx+3,sy)],'rojo')
  poly(im,[(cx-4,sy+2),(cx-2,sy+3),(cx-3,sy+10),(cx-5,sy+8)],'oxido')
  poly(im,[(cx-3,sy+3),(cx-1,sy+4),(cx,sy+9),(cx-2,sy+8)],'rojo')
  rounded(im,(cx-5,sy+1,cx-2,sy+4),'rojo','oxido',1)
 if pose=='strap':
  bx=cx-18;by=66
  rounded(im,(bx,by,bx+11,77),'crema','canela',1)
  line(im,[(bx+2,75),(bx+9,75)],'canela')
  line(im,[(cx-11,sy+1),(bx+2,by)],'canela',3)
  line(im,[(cx-11,sy+1),(bx+2,by)],'crema')
  line(im,[(cx-11,sy+1),(bx+9,by)],'canela')
 if not without_head:im.paste(face[0],face[1],face[0])
 if pose=='cross':
  # Tucked fingertips are behind the opposite arm, rather than stamped on top of it.
  flat(im,arms[1]['hand'],skin)
  im.paste(col(skin[0]),(0,0),arms[1]['detail'])
 # Repaint the visible front of each continuous arm using its full silhouette's boundary.
 # There is no per-segment elbow contour and no transverse cuff stripe.
 for k in [0,1]:
  arm=arms[k]
  tucked=pose=='cross' and k==1
  region=ImageChops.lighter(arm['fore'],arm['hand']) if bare and not tucked else arm['fore']
  overlay_continuous(im,arm['whole'],region,skin if bare else sleeve)
  if not bare and not tucked:
   if arm['gesture'] in ['wave','chin','hip']:hand(im,palms[k],skin,arm['gesture'],1 if k==0 else -1)
   else:flat(im,arm['hand'],skin)
  if not tucked and (bare or arm['gesture'] not in ['wave','chin','hip']):im.paste(col(skin[0]),(0,0),arm['detail'])
  x,y=palms[k]
  if pose=='pocket' and k==0:
   line(im,[(x-3,y+2),(x+3,y)],cloth[0]);line(im,[(x-2,y+3),(x+3,y+1)],cloth[1])
  elif pose=='phone' and k==1:
   rounded(im,(x-2,y-9,x+3,y+1),'noche','negro',1)
   rect(im,(x-1,y-7,x+2,y-2),'gris-azul')
   line(im,[(x-3,y),(x,y)],skin[1],2);rect(im,(x+3,y-1,x+3,y),skin[1])
 if pose=='clasp':line(im,[(cx,69),(cx+1,71)],skin[0])
 # The chin occludes the top knuckles. Keep the approved jaw/beard silhouette intact.
 if pose=='chin' and not without_head:im.paste(face[0],face[1],face[0])
 return im


def sheet(start):
 out=Image.new('RGB',(1520,1510),col('negro'))
 text(out,(32,22),f'CLIENTES / AJUSTES DE CONSISTENCIA / {start+1:02}—{start+12:02}',31,'crema')
 text(out,(32,68),'Pelo limpio · codos suaves · brazos más ligeros · hombros definidos',20,'gris')
 for j in range(12):
  i=start+j;x=32+j%4*374;y=119+j//4*451
  text(out,(x,y),f'{i+1:02} {CAST[i][0]} / {CAST[i][1]}',23,'crema')
  text(out,(x,y+31),legacy.POSE_NAMES[ANATOMY[i][5]].replace('entrelazadas','juntas'),18)
  bg=Image.new('RGB',(320,332),col('noche'));piece=render(i).resize((256,320),Image.Resampling.NEAREST)
  bg.paste(piece,(32,6),piece);line(bg,[(12,322),(308,322)],'pizarra');out.paste(bg,(x,y+62))
  text(out,(x,y+401),f'{CAST[i][2]} · {heads.base.FACE_LABELS[heads.base.FACES[i]]}',16,'gris')
 out.save(ROOT/f'customers-final-polish-{start+1:02}-{start+12:02}.png')

def comparison_sheet():
 out=Image.new('RGB',(1520,850),col('negro'))
 text(out,(32,22),'GESTOS / ANTES Y CORREGIDOS',31,'crema')
 text(out,(32,68),'Codos sin bultos · menos grosor · hombros visibles · pelo sin píxeles sueltos',20,'gris')
 for j,i in enumerate([5,10,9,6,18,1,2,23]):
  x=32+j%4*374;y=116+j//4*355
  text(out,(x,y),f'{i+1:02} {CAST[i][0]}',24,'crema')
  for k,(label,piece) in enumerate([('ANTES',Image.open(BASELINE/f'customer-{i+1:02}-1x.png')),('REVISADO',render(i))]):
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
 for j,i in enumerate([0,5,9,10,14,18]):
  x=32+j%2*680;y=120+j//2*480;text(out,(x,y),f'{i+1:02} {CAST[i][0]}',23,'crema')
  im=Image.new('RGB',(320,200),col('noche'));im.paste(env.dining_horizontal(),(0,0))
  person=render(i);im.paste(person,(128,46),person);im.paste(env.red_bar(),(0,122))
  sprite(im,'plato',145,120)
  for k,xx in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:sprite(im,k,xx,103)
  for k,xx in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:sprite(im,k,xx,139)
  sprite(im,'plancha',82,165);sprite(im,'charola',244,165);sprite(im,'basura',40,170)
  for k,xx,yy in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:sprite(im,k,xx,yy)
  out.paste(im.resize((640,400),Image.Resampling.NEAREST),(x,y+42))
 out.save(ROOT/'customers-final-polish-context.png')

def validate_artifacts():
 allowed={tuple(bytes.fromhex(h[1:])) for h in P.values()};rows=[];digests=set()
 for i in range(24):
  im=render(i);g=geometry(i);parts=heads.face_parts(i)
  assert abs(g['cx']-32)<=1 and g['head_x']==g['cx'],f'{i+1}: exaggerated lean/head offset'
  assert g['shoulders'][0][1]==g['shoulders'][1][1],f'{i+1}: tilted shoulders'
  old_head=Image.open(BASELINE/f'face-{i+1:02}-1x.png').convert('RGBA')
  head_changed=heads.portrait(i).tobytes()!=old_head.tobytes()
  assert head_changed==(i in CROWN_IDS or i==5),f'{i+1}: unexpected head change'
  original=OLD_PARTS(i)
  assert parts['core'].crop((0,7,48,54)).tobytes()==original['core'].crop((0,7,48,54)).tobytes(),f'{i+1}: facial features changed'
  for key in ['eyewear','accessories']:assert parts[key].tobytes()==original[key].tobytes()
  if i!=5:assert parts['hair'].tobytes()==original['hair'].tobytes()
  if i in CROWN_IDS:
   covered=ImageChops.lighter(parts['rear'].getchannel('A'),parts['hair'].getchannel('A'))
   covered=ImageChops.lighter(covered,parts['accessories'].getchannel('A'))
   assert all(not parts['core'].getpixel((x,y))[3] or covered.getpixel((x,y)) for y in range(7) for x in range(48))
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
  changed=im.tobytes()!=Image.open(BASELINE/f'customer-{i+1:02}-1x.png').convert('RGBA').tobytes()
  assert changed==(i in CROWN_IDS or i in [5,10,18]),f'{i+1}: unexpected scope change'
  rows.append({'id':i+1,'name':CAST[i][0],'pose':g['pose'],'head_unchanged':not head_changed,'facial_features_unchanged':True,'central_face_unobscured':True,
   'palette_size_transparency':True,'no_clipping':True,'one_connected_silhouette':True,'body_revised':changed,'subtle_torso_offset':g['cx']-32,'head_neck_aligned':True,'shoulders_level':True})
 return rows

def detail_sheets():
 out=Image.new('RGB',(1520,1020),col('negro'));text(out,(32,22),'REVISIÓN / 24 CUELLOS Y ABERTURAS',31,'crema')
 for i in range(24):
  x=32+(i%6)*248;y=94+(i//6)*224;g=geometry(i)
  text(out,(x,y),f'{i+1:02} {CAST[i][0]}',20,'crema')
  piece=render(i).crop((g['cx']-13,g['sy']-7,g['cx']+14,g['sy']+17)).resize((189,168),Image.Resampling.NEAREST)
  bg=Image.new('RGB',(216,176),col('noche'));bg.paste(piece,(13,4),piece);out.paste(bg,(x,y+31))
 out.save(ROOT/'collars-24.png')
 out=Image.new('RGB',(1200,770),col('negro'));text(out,(24,18),'GESTOS / REVISIÓN AMPLIADA',28,'crema')
 for j,i in enumerate([0,14,20,5,10,6,9,18]):
  x=24+j%4*298;y=82+j//4*338;text(out,(x,y),f'{i+1:02} {CAST[i][0]}',21,'crema')
  im=render(i);g=geometry(i)
  if j<3:crop=im.crop((20,g['top']+heads.face_parts(i)['chin']-8,51,min(80,g['top']+heads.face_parts(i)['chin']+22)))
  elif i in [5,10]:crop=im.crop((38,g['sy']-16,63,g['sy']+15))
  else:crop=im.crop((8,g['sy']+2,56,min(80,g['sy']+30)))
  scale=min(256//crop.width,260//crop.height);crop=crop.resize((crop.width*scale,crop.height*scale),Image.Resampling.NEAREST)
  bg=Image.new('RGB',(274,272),col('noche'));bg.paste(crop,((274-crop.width)//2,4),crop);out.paste(bg,(x,y+34))
 out.save(ROOT/'gestures-closeup.png')

def hair_comparison_sheet():
 out=Image.new('RGB',(1520,1060),col('negro'))
 text(out,(32,18),'PEINADOS / ANTES Y AJUSTADOS',30,'crema')
 text(out,(32,61),'Sin restos de piel sobre el pelo · Vale conserva su cresta rosa',20,'gris')
 for j,i in enumerate(sorted(CROWN_IDS|{5})):
  x=32+j%4*374;y=106+j//4*310
  text(out,(x,y),f'{i+1:02} {CAST[i][0]}',23,'crema')
  for k,(label,head) in enumerate([('ANTES',Image.open(BASELINE/f'face-{i+1:02}-1x.png').convert('RGBA')),('AJUSTADO',heads.portrait(i))]):
   xx=x+k*172;text(out,(xx,y+34),label,16,'gris')
   piece=head.crop((6,0,42,22)).resize((144,88),Image.Resampling.NEAREST)
   bg=Image.new('RGB',(164,108),col('noche'));bg.paste(piece,(10,8),piece);out.paste(bg,(xx,y+62))
   native=head.crop((6,0,42,36)).resize((72,72),Image.Resampling.NEAREST)
   bg=Image.new('RGB',(164,96),col('noche'));bg.paste(native,(46,8),native);out.paste(bg,(xx,y+174))
 out.save(ROOT/'hair-before-after.png')

def validate_contacts_and_arms():
 results=[]
 for i in [0,14,20]:
  g=geometry(i);skin=legacy.old.SKINS[CAST[i][5]]
  palm=Image.new('RGBA',SIZE);hand(palm,g['palms'][1],skin,'chin')
  mask=Image.new('L',SIZE);mask.paste(heads.face_parts(i)['mask'],(g['head_x']-24,g['top']))
  count=sum(a>0 for a in ImageChops.multiply(mask,palm.getchannel('A')).getdata());assert count>0
  results.append({'id':i+1,'gesture':'chin','face_contact_pixels':count})
 for i in [6,9,18]:
  g=geometry(i);s,e,p=g['shoulders'],g['elbows'],g['palms'];width=7
  hm0,_=hand_shape(p[0],e[0],'cross_rest',1);hm1,_=hand_shape(p[1],e[1],'cross_tucked',-1)
  opposite=segment_mask(s[1],e[1],width,width-1)
  whole,fore=unified_arm(s[0],e[0],point_toward(p[0],e[0],3),width,relaxed=True)
  rest_count=sum(a>0 for a in ImageChops.multiply(hm0,opposite.filter(ImageFilter.MaxFilter(3))).getdata())
  tuck_count=sum(a>0 for a in ImageChops.multiply(hm1,fore.filter(ImageFilter.MaxFilter(3))).getdata())
  assert rest_count>=4 and tuck_count>=4,(i+1,rest_count,tuck_count)
  results.append({'id':i+1,'gesture':'cross','resting_hand_contact':rest_count,'tucked_hand_overlap':tuck_count})
 arms=[]
 for i in range(24):
  g=geometry(i);width=7 if g['pose']=='cross' else 5 if CAST[i][6] in ['jersey','retro','band','hawaiian'] else 6
  for k in [0,1]:
   s,e,p=g['shoulders'][k],g['elbows'][k],g['palms'][k]
   whole,fore=unified_arm(s,e,point_toward(p,e,3),width,relaxed=g['pose']=='cross')
   if g['pose']=='wave' and k==1:whole,fore=wave_arm(s,e,point_toward(p,e,3))
   im=Image.new('RGBA',SIZE);flat(im,whole,('negro','blanco','gris'));overlay_continuous(im,whole,fore,('negro','blanco','gris'))
   ink=sum(1 for y in range(80) for x in range(64) if whole.getpixel((x,y)) and im.getpixel((x,y))[:3]!=(255,255,255))
   assert ink==0,(i+1,k)
   arms.append({'id':i+1,'side':k,'internal_elbow_ink_pixels':ink})
 return {'gesture_contacts':results,'continuous_arms':arms}

if __name__=='__main__':
 checks=validate_artifacts();contacts=validate_contacts_and_arms()
 for i in range(24):
  render(i).save(ROOT/f'customer-{i+1:02}-1x.png')
  heads.portrait(i).save(ROOT/f'face-{i+1:02}-1x.png')
 sheet(0);sheet(12);comparison_sheet();context_sheet();detail_sheets();hair_comparison_sheet()
 (ROOT/'gesture-contact-checks.json').write_text(json.dumps(contacts,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 print('24 clientes verificados: 12 cabezas refinadas sin cambios en facciones; codos y brazos revisados; 10 sprites intactos.')
