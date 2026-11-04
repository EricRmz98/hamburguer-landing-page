"""Approved cast with exactly two hair corrections: Jules (15) and Chema (17)."""
from pathlib import Path
from PIL import Image, ImageChops
import importlib.util,json
ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'customers-face-audit-2026-10-31'
spec=importlib.util.spec_from_file_location('approved_faces',PREVIOUS/'generate.py')
approved=importlib.util.module_from_spec(spec);spec.loader.exec_module(approved)
TARGETS=(14,16)
old_hair=approved.frozen_hair
old_heads={i:approved.portrait(i) for i in TARGETS}
old_parts={i:approved.face_parts(i) for i in TARGETS}

# Draw the rounded fringe as one connected silhouette; its two halves share every pixel.
def symmetric_curls(i):
 hs,hb,_=approved.base.old.HAIR[approved.CAST[i][4]]
 c=approved.CENTRE;size=approved.HEAD_SIZE
 mask=Image.new('L',size)
 # A continuous scalp under the curls covers the old exposed skin at the upper-right edge.
 approved.draw(mask).polygon([(c-9,3),(c+9,3),(c+13,6),(c+14,9),(c+13,12),
  (c+11,10),(c+6,9),(c,8),(c-6,9),(c-11,10),(c-13,12),(c-14,9),(c-13,6)],fill=255)
 approved.draw(mask).ellipse((c-6,1,c+6,9),fill=255)
 for box in [(c-12,3,c-3,10),(c-15,6,c-9,12)]:
  stamp=Image.new('L',size);approved.draw(stamp).ellipse(box,fill=255)
  mask=ImageChops.lighter(mask,stamp);mask=ImageChops.lighter(mask,approved.mirror(stamp))
 # Rasterization of diagonal edges is normalized too, not just the control points.
 mask=ImageChops.lighter(mask,approved.mirror(mask))
 front=Image.new('RGBA',size)
 front.paste(approved.color(hs),(0,0),mask.filter(approved.base.ImageFilter.MaxFilter(3)))
 front.paste(approved.color(hb),(0,0),mask)
 # Sparse matching curl seams; no skin-coloured highlights.
 approved.paired(front,lambda im:approved.line(im,[(c-11,7),(c-11,5),(c-9,4)],hs))
 approved.paired(front,lambda im:approved.line(im,[(c-4,5),(c-3,3),(c-1,3)],hs))
 return Image.new('RGBA',size),front

def corrected_hair(i):return symmetric_curls(i) if i in TARGETS else old_hair(i)
approved.frozen_hair=corrected_hair


def detail_sheet():
 out=Image.new('RGB',(1120,860),approved.color('negro'))
 approved.text(out,(32,22),'JULES Y CHEMA / PELO SIMÉTRICO',32,'crema')
 approved.text(out,(32,69),'Rizos más ordenados · sin piel asomando sobre el pelo',20,'gris')
 for j,i in enumerate(TARGETS):
  x=32+j*550
  approved.text(out,(x,114),f'{i+1:02} {approved.CAST[i][0]}',25,'crema')
  for k,(label,head) in enumerate([('ANTES',old_heads[i]),('CORREGIDO',approved.portrait(i))]):
   xx=x+k*254;approved.text(out,(xx,158),label,17,'gris')
   crop=head.crop((4,0,44,38)).resize((200,190),Image.Resampling.NEAREST)
   bg=Image.new('RGB',(224,200),approved.color('noche'));bg.paste(crop,(12,4),crop)
   out.paste(bg,(xx,188))
  sprite=approved.render(i).resize((256,320),Image.Resampling.NEAREST)
  bg=Image.new('RGB',(480,344),approved.color('noche'));bg.paste(sprite,(112,8),sprite)
  out.paste(bg,(x,412))
  approved.text(out,(x,782),'Rostro y cuerpo aprobados conservados',18,'gris')
 out.save(ROOT/'jules-chema.png')


def verify():
 checks=approved.check_faces()
 for i in range(24):
  new=approved.render(i)
  previous=Image.open(PREVIOUS/f'customer-{i+1:02}-1x.png').convert('RGBA')
  if i not in TARGETS:
   assert new.tobytes()==previous.tobytes(),f'{i+1}: approved customer changed'
   continue
  parts=approved.face_parts(i)
  for key in ['core','eyewear','accessories']:
   assert parts[key].tobytes()==old_parts[i][key].tobytes(),f'{i+1}: approved face changed'
  assert parts['hair'].tobytes()==approved.mirror(parts['hair']).tobytes(),f'{i+1}: asymmetric hair'
  head=approved.portrait(i)
  assert head.tobytes()==approved.mirror(head).tobytes(),f'{i+1}: asymmetric complete head'
  # The top of the scalp must be hidden by hair: no exposed skin or bright halo.
  for y in range(8):
   for x in range(48):
    if parts['core'].getpixel((x,y))[3]:
     assert parts['hair'].getpixel((x,y))[3]==255,f'{i+1}: exposed skin above curls at {(x,y)}'
  hs,hb,_=approved.base.old.HAIR[approved.CAST[i][4]]
  allowed={tuple(bytes.fromhex(approved.color(c)[1:])) for c in [hs,hb]}
  assert all(not a or (r,g,b) in allowed for r,g,b,a in parts['hair'].getdata())
  # Keep every body pixel below the crown, including the hair-to-forehead transition's limit.
  boundary=approved.ANATOMY[i][0]+15
  assert new.crop((0,boundary,64,80)).tobytes()==previous.crop((0,boundary,64,80)).tobytes(),f'{i+1}: changes below hair'
 return checks

if __name__=='__main__':
 checks=verify()
 for i in range(24):
  approved.render(i).save(ROOT/f'customer-{i+1:02}-1x.png')
  approved.portrait(i).save(ROOT/f'face-{i+1:02}-1x.png')
 approved.ROOT=ROOT;approved.faces_sheet();approved.full_sheet(0);approved.full_sheet(12)
 detail_sheet()
 (ROOT/'checks.json').write_text(json.dumps({'unchanged_customers':22,'hair_symmetry':[15,17],
  'complete_head_symmetry':[15,17],'no_exposed_skin_above_curls':[15,17],
  'approved_faces_unchanged':[15,17],'body_and_pose_unchanged':True,'face_checks':checks},ensure_ascii=False,indent=2)+'\n')
 print('Jules y Chema: pelo y cabeza simétricos; sin piel expuesta sobre el pelo. Rostros/cuerpos conservados; otros 22 clientes idénticos.')
