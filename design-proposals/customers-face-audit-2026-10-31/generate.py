"""Face-only reference revision. Body/pose functions and all hair modules stay frozen."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops
import importlib.util, json, hashlib
ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'customers-soft-faces-2026-10-31'
spec=importlib.util.spec_from_file_location('frozen_customer_cast',PREVIOUS/'generate.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
P=base.P;CAST=base.CAST;ANATOMY=base.ANATOMY
color=base.color;draw=base.draw;line=base.line;rect=base.rect;poly=base.poly;oval=base.oval;rounded=base.rounded;text=base.text
CENTRE=24;HEAD_SIZE=(48,54)
# Half widths per row. Whole rows are mirrored about the SAME integer face axis.
# Chin heights intentionally match the previous version, leaving shoulders/poses unchanged.
PROFILES={
 'alargada':[(3,5),(9,9),(18,9),(25,7),(30,3)],
 'cuadrada':[(3,6),(9,10),(19,10),(25,8),(28,4)],
 'corazon':[(3,6),(10,10),(18,9),(24,6),(29,2)],
 'ancha':[(3,6),(10,11),(18,11),(24,8),(28,4)],
 'rombo':[(3,5),(10,10),(17,10),(24,7),(29,3)],
 'estrecha':[(3,5),(9,8),(19,8),(25,6),(29,2)],
 'triangular':[(3,6),(10,10),(19,8),(25,5),(29,2)],
 'mandibula_ancha':[(3,6),(10,10),(18,10),(24,8),(28,4)],
 'redonda':[(3,5),(9,10),(16,11),(22,9),(27,5),(29,2)]}

def mirror(im):
 """Pixel reflection x -> 48-x, about x=24 (not PIL's half-pixel canvas centre)."""
 out=Image.new(im.mode,im.size)
 out.paste(im.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(1,0))
 return out

def paired(im,paint):
 left=Image.new('RGBA',HEAD_SIZE);paint(left)
 im.alpha_composite(left);im.alpha_composite(mirror(left))

def face_geometry(i):
 ratio=ANATOMY[i][3]/22
 profile=[(round(y*ratio),round(w*ratio)) for y,w in PROFILES[base.FACES[i]]]
 mask=Image.new('L',HEAD_SIZE)
 for (y0,w0),(y1,w1) in zip(profile,profile[1:]):
  for y in range(y0,y1+1):
   half=round(w0+(w1-w0)*(y-y0)/max(1,y1-y0))
   draw(mask).line([(CENTRE-half,y),(CENTRE+half,y)],fill=255)
 eye_y=round(14*ratio);row=[x for x in range(48) if mask.getpixel((x,eye_y))]
 left,right=min(row),max(row)
 gap=max(4,min(5,round((right-left)*.23)))
 return mask,profile[-1][0],eye_y,left,right,gap

def frozen_hair(i):
 """Exact previous hair geometry, including intentionally asymmetric styling."""
 ratio=ANATOMY[i][3]/22;kind=CAST[i][3];hs,hb,hl=base.old.HAIR[CAST[i][4]]
 old_mask=Image.new('L',HEAD_SIZE)
 draw(old_mask).polygon([(round(CENTRE+(x-24)*ratio),round(y*ratio)) for x,y in base.FACE_POINTS[base.FACES[i]]],fill=255)
 temple=[x for x in range(48) if old_mask.getpixel((x,round(10*ratio)))]
 scale=(max(temple)-min(temple)+4)/24
 def layer(back):
  source=Image.new('RGBA',(48,48))
  (base.old.hair_back if back else base.old.hair_front)(source,kind,hs,hb,hb)
  w=round(48*scale);h=round(48*ratio)
  resized=source.resize((w,h),Image.Resampling.NEAREST)
  result=Image.new('RGBA',HEAD_SIZE);result.paste(resized,(CENTRE-w//2,0),resized)
  return result
 rear,front=layer(True),layer(False)
 if kind=='bun':
  yy=round(14*ratio);row=[x for x in range(48) if old_mask.getpixel((x,yy))];left,right=min(row),max(row)
  rear=Image.new('RGBA',HEAD_SIZE);front=Image.new('RGBA',HEAD_SIZE)
  oval(rear,(CENTRE-4,0,CENTRE+4,8),hs);oval(rear,(CENTRE-3,1,CENTRE+2,5),hb)
  rounded(front,(left-1,4,right+1,yy-2),hb,hs,3)
  poly(front,[(left-1,8),(left+2,9),(left+1,yy+1),(left-1,yy)],hs)
  poly(front,[(right+1,8),(right-2,9),(right-1,yy+1),(right+1,yy)],hs)
 return rear,front

def face_parts(i):
 ss,sb,sl=base.old.SKINS[CAST[i][5]];hs,hb,hl=base.old.HAIR[CAST[i][4]]
 acc=CAST[i][8];kind=CAST[i][3];ratio=ANATOMY[i][3]/22
 mask,chin,eye_y,left,right,gap=face_geometry(i)
 outline=mask.filter(base.ImageFilter.MaxFilter(3))
 core=Image.new('RGBA',HEAD_SIZE)
 core.paste(color(ss),(0,0),outline);core.paste(color(sb),(0,0),mask)
 # No cheek/jaw shade patch: every unmarked interior skin pixel is the same base colour.
 paired(core,lambda im:rounded(im,(left-1,eye_y,left+1,eye_y+4),ss,None,1))
 paired(core,lambda im:line(im,[(left,eye_y+1),(left,eye_y+2)],sb))
 left_eye=CENTRE-gap
 paired(core,lambda im:line(im,[(left_eye-2,eye_y-4),(left_eye+1,eye_y-4)],hs))
 eye_style,mouth_style=base.EXPRESSIONS[i]
 if eye_style=='happy':
  paired(core,lambda im:line(im,[(left_eye-1,eye_y+1),(left_eye,eye_y),(left_eye+1,eye_y+1)],'negro'))
 elif eye_style=='relaxed':
  paired(core,lambda im:line(im,[(left_eye-1,eye_y+1),(left_eye+1,eye_y+1)],'negro'))
 else:paired(core,lambda im:rect(im,(left_eye-1,eye_y,left_eye,eye_y+2),'negro'))
 nose_y=eye_y+5
 line(core,[(CENTRE,nose_y-1),(CENTRE,nose_y)],ss)
 mouth_y=chin-6
 beard=Image.new('L',HEAD_SIZE)
 if acc in ['beard','glasses_beard']:
  # Facial hair replaces BOTH skin fill and the outer skin outline down to the chin.
  # Its edge is the actual jaw edge. There is no skin rim and no skin-coloured mouth island.
  for y in range(nose_y-1,chin+2):
   for x in range(48):
    if not outline.getpixel((x,y)):continue
    distance=abs(x-CENTRE)
    start=nose_y+2 if distance<=4 else nose_y if distance<=7 else nose_y-1
    if y>=start:beard.putpixel((x,y),255)
  core.paste(color(hs),(0,0),beard)
  inner=ImageChops.multiply(beard,mask)
  core.paste(color(hb),(0,0),inner)
  mouth_ink=hs
 else:mouth_ink=ss
 if mouth_style=='grin':
  rounded(core,(CENTRE-3,mouth_y,CENTRE+3,mouth_y+2),mouth_ink,None,1)
  line(core,[(CENTRE-2,mouth_y),(CENTRE+2,mouth_y)],'crema')
 elif mouth_style=='smile':
  line(core,[(CENTRE-2,mouth_y),(CENTRE-1,mouth_y+1),(CENTRE+1,mouth_y+1),(CENTRE+2,mouth_y)],mouth_ink)
 else:line(core,[(CENTRE-2,mouth_y),(CENTRE+2,mouth_y)],mouth_ink)
 if acc=='moustache':
  paired(core,lambda im:line(im,[(CENTRE-3,mouth_y-2),(CENTRE-1,mouth_y-3),(CENTRE,mouth_y-2)],hs))
 if acc=='stubble':
  paired(core,lambda im:rect(im,(CENTRE-5,mouth_y-1,CENTRE-5,mouth_y-1),hs))
  paired(core,lambda im:rect(im,(CENTRE-4,mouth_y+2,CENTRE-4,mouth_y+2),hs))
 if kind=='bun':draw(core).rectangle((0,0,47,3),fill=(0,0,0,0))
 rear,hair_front=frozen_hair(i)
 eyewear=Image.new('RGBA',HEAD_SIZE)
 if acc in ['glasses','roundglasses','glasses_beard']:
  # The right frame is reflected from the left frame, including its pupil alignment.
  def lens(im):
   box=(left_eye-4,eye_y-2,left_eye+3,eye_y+4)
   if acc=='roundglasses':draw(im).ellipse(box,outline=color('negro'))
   else:rounded(im,box,None,'negro',1)
  paired(eyewear,lens)
  line(eyewear,[(left_eye+3,eye_y),(48-(left_eye+3),eye_y)],'negro')
  paired(eyewear,lambda im:line(im,[(left,eye_y-1),(left_eye-4,eye_y-1)],'negro'))
 accessories=Image.new('RGBA',HEAD_SIZE)
 if acc=='earbuds':paired(accessories,lambda im:line(im,[(left,eye_y+1),(left,eye_y+4)],'gris-claro'))
 if acc=='piercing':
  paired(accessories,lambda im:rect(im,(left-1,eye_y+3,left-1,eye_y+4),'gris'))
  rect(accessories,(CENTRE,nose_y+1,CENTRE,nose_y+1),'gris')
 def xy(x,y):return (round(CENTRE+(x-24)*ratio),round(y*ratio))
 # Hair/head accessories keep their previous character and placement.
 if acc in ['headband','bandana']:
  yy=round(7*ratio);cc='rojo' if acc=='bandana' else 'gris-claro'
  line(accessories,[xy(14,7),xy(34,7)],cc,2)
  if acc=='bandana':
   for dx in [-6,0,6]:rect(accessories,(CENTRE+dx,yy,CENTRE+dx,yy),'blanco')
   poly(accessories,[(right-1,yy),(right+4,yy+1),(right+2,yy+4)],'rojo-oscuro')
 if acc=='beanie':
  rounded(accessories,(*xy(12,0),*xy(35,8)),'oxido',None,4)
  rect(accessories,(*xy(12,6),*xy(35,10)),'tostado')
  for x in [16,21,26,31]:line(accessories,[xy(x,7),xy(x,9)],'canela')
 if acc=='clips':
  for xx in [left+2,right-4]:rect(accessories,(xx,eye_y-5,xx+3,eye_y-4),'cian')
 if acc=='goggles':
  yy=round(6*ratio);line(accessories,[(left,yy),(right,yy)],'noche',2)
  for ex,cc in zip([CENTRE-gap,CENTRE+gap],['cian','magenta']):rounded(accessories,(ex-3,yy-2,ex+3,yy+2),cc,'noche',1)
 if acc=='visor':
  rounded(accessories,(left+1,eye_y-2,right-1,eye_y+3),'azul-oscuro','noche',2)
  line(accessories,[(left+3,eye_y-1),(right-3,eye_y-1)],'cian')
 if acc=='headphones':
  line(accessories,[(left-2,eye_y+1),(left-2,round(7*ratio)),(left+2,round(5*ratio)),(right-2,round(5*ratio)),(right+2,round(7*ratio)),(right+2,eye_y+1)],'noche',2)
  paired(accessories,lambda im:rounded(im,(left-2,eye_y-1,left,eye_y+6),'pizarra','negro',1))
 if acc in ['cap','capback']:
  cc='verde-oscuro' if acc=='cap' else 'azul-oscuro'
  rounded(accessories,(*xy(12,0),*xy(35,7)),cc,'negro',3)
  if acc=='cap':rect(accessories,(*xy(19,6),*xy(38,8)),'verde-noche')
  else:rect(accessories,(*xy(9,6),*xy(17,8)),cc);rect(accessories,(*xy(20,5),*xy(27,7)),'gris')
 return {'core':core,'rear':rear,'hair':hair_front,'eyewear':eyewear,'accessories':accessories,'mask':mask,'outline':outline,'beard_mask':beard,'chin':chin,'eye_y':eye_y}

def head_layers(i,skin,hair,facew,top,cx):
 parts=face_parts(i);front=parts['core'].copy()
 for key in ['hair','eyewear','accessories']:front.alpha_composite(parts[key])
 offset=(round(cx)-CENTRE,top)
 return (parts['rear'],offset),(front,offset)

# The body and poses execute the previous generator's exact functions and constants.
base.head_layers=head_layers
render=base.render

def portrait(i,old=False):
 top,sw,ww,fw,lean,pose=ANATOMY[i]
 if old:
  r,f=old_head(i,base.old.SKINS[CAST[i][5]],base.old.HAIR[CAST[i][4]],fw,top,32)
 else:r,f=head_layers(i,None,None,fw,top,32)
 head=r[0].copy();head.alpha_composite(f[0]);return head

# Re-import a separate copy solely for before/after and frozen-body verification.
old_spec=importlib.util.spec_from_file_location('prior_faces_unmodified',PREVIOUS/'generate.py')
prior=importlib.util.module_from_spec(old_spec);old_spec.loader.exec_module(prior)
old_head=prior.head_layers

def faces_sheet():
 out=Image.new('RGB',(1520,1220),color('negro'))
 text(out,(32,22),'24 CLIENTES / REVISIÓN SOLO DE ROSTROS',32,'crema')
 text(out,(32,68),'Piel plana · facciones simétricas · barbas sin borde de piel',20,'gris')
 for i in range(24):
  x=32+(i%6)*248;y=116+(i//6)*270
  text(out,(x,y),f'{i+1:02} {CAST[i][0]}',21,'crema')
  piece=portrait(i).crop((4,0,44,38)).resize((200,190),Image.Resampling.NEAREST)
  bg=Image.new('RGB',(216,200),color('noche'));bg.paste(piece,(8,4),piece)
  out.paste(bg,(x,y+34));text(out,(x,y+240),CAST[i][1],16,'gris')
 out.save(ROOT/'faces-24.png')

def comparison_sheet():
 out=Image.new('RGB',(1520,1400),color('negro'))
 text(out,(32,22),'ROSTROS / ANTES Y CORREGIDO',32,'crema')
 text(out,(32,68),'01 y 10: barbas · resto: sombra, contorno, ojos, nariz y gafas',20,'gris')
 for j,i in enumerate([0,9,7,20,4,14,2,23]):
  x=32+j%4*374;y=116+j//4*630
  text(out,(x,y),f'{i+1:02} {CAST[i][0]}',24,'crema')
  for k,old in enumerate([True,False]):
   yy=y+44+k*275;text(out,(x,yy),'ANTES' if old else 'CORREGIDO',17,'gris')
   piece=portrait(i,old).crop((4,0,44,38)).resize((240,228),Image.Resampling.NEAREST)
   bg=Image.new('RGB',(320,236),color('noche'));bg.paste(piece,(40,4),piece)
   out.paste(bg,(x,yy+26))
 out.save(ROOT/'faces-before-after.png')

def full_sheet(start):
 out=Image.new('RGB',(1520,1510),color('negro'))
 text(out,(32,22),f'ROSTROS CORREGIDOS / {start+1:02}—{start+12:02}',32,'crema')
 text(out,(32,68),'Cuerpos y poses conservados · fase 1: solo rostros · referencias sin integrar',20,'gris')
 for j in range(12):
  i=start+j;x=32+j%4*374;y=119+j//4*451
  text(out,(x,y),f'{i+1:02} {CAST[i][0]} / {CAST[i][1]}',23,'crema')
  text(out,(x,y+31),base.POSE_NAMES[ANATOMY[i][5]],18)
  sprite=render(i).resize((256,320),Image.Resampling.NEAREST)
  bg=Image.new('RGB',(320,332),color('noche'));bg.paste(sprite,(32,6),sprite)
  line(bg,[(12,322),(308,322)],'pizarra');out.paste(bg,(x,y+62))
  text(out,(x,y+401),f'{CAST[i][2]} · {base.FACE_LABELS[base.FACES[i]]}',16,'gris')
 out.save(ROOT/f'customers-face-audit-{start+1:02}-{start+12:02}.png')

def check_faces():
 allowed={tuple(bytes.fromhex(h[1:])) for h in P.values()};rows=[];hashes=set()
 def no_head(i,skin,hair,facew,top,cx):
  blank=Image.new('RGBA',HEAD_SIZE);offset=(round(cx)-CENTRE,top)
  return (blank,offset),(blank,offset)
 # Compare bodies without either old or new head present. This includes arms/hands at head height.
 old_current,old_prior=base.head_layers,prior.head_layers
 try:
  base.head_layers=prior.head_layers=no_head
  for i in range(24):
   assert base.render(i).tobytes()==prior.render(i).tobytes(),f'{i+1}: body/pose pixels changed'
 finally:base.head_layers,prior.head_layers=old_current,old_prior
 for i in range(24):
  parts=face_parts(i);core=parts['core'];mask=parts['mask'];beard=parts['beard_mask']
  # Exact RGB+alpha symmetry of skin, facial contours and all facial marks. Hair is separate.
  assert core.tobytes()==mirror(core).tobytes(),f'{i+1}: asymmetric facial core'
  assert parts['eyewear'].tobytes()==mirror(parts['eyewear']).tobytes(),f'{i+1}: asymmetric glasses'
  if CAST[i][8] not in ['beard','glasses_beard']:
   # Equal flat skin on both cheeks, below the eye line, away from the nose and mouth.
   skin_base=tuple(bytes.fromhex(color(base.old.SKINS[CAST[i][5]][1])[1:]))
   for xx in [CENTRE-5,CENTRE+5]:
    assert core.getpixel((xx,parts['eye_y']+4))[:3]==skin_base,f'{i+1}: cheek shading remains'
  if beard.getbbox():
   ss,sb,sl=base.old.SKINS[CAST[i][5]];hs,hb,hl=base.old.HAIR[CAST[i][4]]
   beard_colors={tuple(bytes.fromhex(color(c)[1:])) for c in [hs,hb]}
   for y in range(54):
    for x in range(48):
     if beard.getpixel((x,y)):assert core.getpixel((x,y))[:3] in beard_colors,f'{i+1}: skin rim in beard'
  im=render(i);assert im.size==(64,80)
  assert all(a in [0,255] and (not a or (r,g,b) in allowed) for r,g,b,a in im.getdata())
  digest=hashlib.sha256(im.tobytes()).hexdigest();assert digest not in hashes;hashes.add(digest)
  # All changes must end with the face. Every body row below its jaw is pixel-identical.
  last_face_row=ANATOMY[i][0]+parts['chin']+2
  old_im=prior.render(i)
  assert im.crop((0,last_face_row,64,80)).tobytes()==old_im.crop((0,last_face_row,64,80)).tobytes(),f'{i+1}: body changed'
  rows.append({'id':i+1,'name':CAST[i][0],'face_symmetry':True,'eyewear_symmetry':True,'flat_cheeks':True,'no_skin_beard_rim':True if beard.getbbox() else None,'entire_body_and_pose_unchanged':True,'body_below_face_unchanged':True,'palette_and_size':True})
 return rows

if __name__=='__main__':
 checks=check_faces()
 for i in range(24):
  render(i).save(ROOT/f'customer-{i+1:02}-1x.png')
  portrait(i).save(ROOT/f'face-{i+1:02}-1x.png')
 faces_sheet();comparison_sheet();full_sheet(0);full_sheet(12)
 (ROOT/'checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 print('24/24: cara y gafas simétricas, sin halo de piel en barbas, cuerpos conservados, paleta y transparencia correctas.')
