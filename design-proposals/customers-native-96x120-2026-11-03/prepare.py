"""Convert original approved illustrations directly onto 96 x 120 native game cells; no enlargement of the 64 x 80 draft."""
from pathlib import Path
from PIL import Image,ImageFilter
from collections import Counter
import json,math

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'customers-new-cast-12-2026-11-01'
PEOPLE=json.loads((SOURCE/'prompts.json').read_text())['characters']
P=json.loads((ROOT/'palette.json').read_text());RGB={k:tuple(bytes.fromhex(v[1:])) for k,v in P.items()}
WAISTS={'01-lia':1015,'02-bruno':1170,'03-zoe':1020,'04-ciro':1180,'05-mika':990,'06-alma':1040,'07-rafa':980,'08-dante':1210,'09-vega':1020,'10-ines':1010,'11-gael':1260,'12-sasha':1010}
SIZE=(96,120);WAIST=114
# Keep the shorter character short instead of filling the same head-to-waist height.
# The factor applies equally to both axes before quantization onto the native grid.
PROPORTION_SCALE={'10-ines':.85}
MIRRORED={'02-bruno','04-ciro','06-alma','08-dante','10-ines','12-sasha'}
FACES={
 '01-lia':(340,255,660,605),'02-bruno':(370,250,670,610),
 '03-zoe':(405,230,650,610),'04-ciro':(405,220,660,600),
 '05-mika':(400,170,690,530),'06-alma':(400,250,680,660),
 '07-rafa':(400,175,680,550),'08-dante':(380,200,650,600),
 '09-vega':(390,240,650,650),'10-ines':(420,280,680,680),
 '11-gael':(400,220,675,620),'12-sasha':(420,230,690,610),
}

def nearest(rgb,allowed):return min(allowed,key=lambda n:sum((a-b)**2 for a,b in zip(rgb,RGB[n])))
def rgba(name):return RGB[name]+(255,)

def prepare(person):
 source=Image.open(SOURCE/person['local_file']).convert('RGBA')
 alpha=source.getchannel('A').point(lambda a:255 if a>=160 else 0)
 source.putalpha(alpha)
 bounds=alpha.getbbox();waist=WAISTS[person['id']]
 upper=alpha.crop((0,bounds[1],source.width,waist+1)).getbbox()
 left,right=upper[0],upper[2];top=bounds[1]
 # The same scale in both axes; crop around the waist while keeping both shoulders/elbows.
 scale=min(106/(waist-top),94/(right-left))*PROPORTION_SCALE.get(person['id'],1)
 width=round((right-left)*scale);height=round((waist-top)*scale)
 crop_bottom=min(source.height,waist+math.ceil(6/scale))
 crop=source.crop((left,top,right,crop_bottom))
 small=crop.resize((width,round(crop.height*scale)),Image.Resampling.LANCZOS)
 # Restore deliberate edge contrast after averaging fine high-resolution detail.
 rgb=small.convert('RGB').filter(ImageFilter.UnsharpMask(radius=.55,percent=30,threshold=5))
 small=Image.merge('RGBA',(*rgb.split(),small.getchannel('A')))
 native=Image.new('RGBA',SIZE);x=(96-width)//2;y=WAIST-height
 native.alpha_composite(small,(x,y))
 raw=Image.new('RGBA',SIZE)
 for yy in range(120):
  for xx in range(96):
   r,g,b,a=native.getpixel((xx,yy))
   if a>=128:raw.putpixel((xx,yy),(r,g,b,255))
 names={}
 for yy in range(120):
  for xx in range(96):
   p=raw.getpixel((xx,yy))
   if p[3]:
    sx=left+(xx-x+.5)/scale;sy=top+(yy-y+.5)/scale
    fl,ft,fr,fb=FACES[person['id']]
    warm_skin=(p[0]>145 and p[1]>65 and p[0]>p[2]*1.35 and p[1]>p[2]*1.05)
    colors=['cafe','canela','piel','piel-clara','durazno'] if fl<=sx<fr and ft<=sy<fb and warm_skin else RGB
    # Keep the approved olive bomber in the green family despite Endesga's lack of olive.
    if person['id']=='12-sasha' and sy>470 and p[1]>=p[0]*.87 and p[1]>p[2]*1.16 and p[0]>p[2]*1.15:
     colors=['verde-noche','verde-oscuro','verde','crema']
    names[xx,yy]=nearest(p[:3],colors)
 counts=Counter(names.values())
 # At most 16 palette colors per sprite; keep the tiny white eye/highlight pixels.
 allowed=[n for n,c in counts.most_common(16)]
 if 'blanco' in counts and 'blanco' not in allowed:allowed[-1]='blanco'
 result=Image.new('RGBA',SIZE)
 for pos,name in names.items():
  if name not in allowed:name=nearest(RGB[name],allowed)
  result.putpixel(pos,rgba(name))
 # Merge isolated close-value color flecks; preserve high-contrast eyes and jewelry.
 before=result.copy()
 for yy in range(1,119):
  for xx in range(1,95):
   center=before.getpixel((xx,yy))
   if not center[3]:continue
   neighbors=[before.getpixel((xx+dx,yy+dy)) for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]]
   if neighbors.count(center)>1:continue
   winner,count=Counter(p for p in neighbors if p[3]).most_common(1)[0]
   distance=sum((a-b)**2 for a,b in zip(center[:3],winner[:3]))
   if count>=5 and distance<6500:result.putpixel((xx,yy),winner)
 # Only remove single disconnected reduction artifacts. Keep earrings/hair clips with real area.
 opaque={pos for pos in names};leftover=set(opaque);components=[]
 while leftover:
  q=leftover.pop();todo=[q];component={q}
  while todo:
   xx,yy=todo.pop()
   for other in [(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)]:
    if other in leftover:leftover.remove(other);component.add(other);todo.append(other)
  components.append(component)
 for component in components:
  if len(component)==1:
   for pos in component:result.putpixel(pos,(0,0,0,0))
 # Mirror the native cells themselves: the atlas, PNG and both layouts share the pose.
 # No fractional CSS transforms or extra resampling are introduced.
 mirrored=person['id'] in MIRRORED
 fl,ft,fr,fb=FACES[person['id']]
 face=[x+(fl-left)*scale,y+(ft-top)*scale,x+(fr-left)*scale,y+(fb-top)*scale]
 if mirrored:
  result=result.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  face=[SIZE[0]-face[2],face[1],SIZE[0]-face[0],face[3]]
 path=ROOT/'individuales'/f'{person["id"]}-96x120.png';path.parent.mkdir(exist_ok=True)
 result.save(path);(ROOT/'rgba'/f'{person["id"]}.rgba').write_bytes(result.tobytes())
 result.resize((384,480),Image.Resampling.NEAREST).save(ROOT/'ampliados'/f'{person["id"]}-4x.png')
 return {'id':person['id'],'name':person['name'],'style':person['style'],'file':str(path.relative_to(ROOT)),'source':str((SOURCE/person['local_file']).resolve()),'source_bounds':bounds,'source_crop':[left,top,right,crop_bottom],'source_face':FACES[person['id']],'source_waist':waist,'uniform_scale':scale,'proportion_scale':PROPORTION_SCALE.get(person['id'],1),'source_placement':[x,y],'placement':[SIZE[0]-x-width if mirrored else x,y],'mirrored':mirrored,'facing':'left' if mirrored else 'right','native_face_bounds':face,'native_bounds':result.getbbox(),'native_waist':114,'size':[96,120],'colors_used':len(set(p for p in result.getdata() if p[3]))}

def main():
 for folder in ['rgba','ampliados','individuales']:(ROOT/folder).mkdir(exist_ok=True)
 people=[prepare(p) for p in PEOPLE]
 (ROOT/'manifest.json').write_text(json.dumps({'native_size':SIZE,'game_size':[96,120],'game_scale':1,'waist_row':114,'status':'adapted_for_review','characters':people},ensure_ascii=False,indent=2)+'\n')
 print(json.dumps([{k:p[k] for k in ['id','placement','colors_used']} for p in people]))
if __name__=='__main__':main()
