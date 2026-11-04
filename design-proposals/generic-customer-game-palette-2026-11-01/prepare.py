"""Deterministic import of the selected image: uniform resizing and palette reduction only."""
from PIL import Image, ImageFilter
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'palette.json').read_text())
SIZE=(64,118);HEIGHT=110;WAIST=76

def rgba(name):return tuple(bytes.fromhex(P[name][1:]))+(255,)
def lum(rgb):return sum(c*w for c,w in zip(rgb,[.2126,.7152,.0722]))
def largest(mask):
 coords={(x,y) for y in range(mask.height) for x in range(mask.width) if mask.getpixel((x,y))}
 components=[]
 while coords:
  first=coords.pop();todo=[first];found={first}
  while todo:
   x,y=todo.pop()
   for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if q in coords:coords.remove(q);found.add(q);todo.append(q)
  components.append(found)
 out=Image.new('L',mask.size)
 for q in max(components,key=len):out.putpixel(q,255)
 return out

def prepare():
 source=Image.open(ROOT/'approved-source.png').convert('RGBA')
 mask=largest(source.getchannel('A').point(lambda a:255 if a>=192 else 0))
 bounds=mask.getbbox();crop=source.crop(bounds);crop.putalpha(mask.crop(bounds))
 width=round(crop.width*HEIGHT/crop.height)
 small=crop.resize((width,HEIGHT),Image.Resampling.BOX)
 alpha=largest(small.getchannel('A').point(lambda a:255 if a>=128 else 0))
 native=Image.new('RGBA',SIZE)
 native.alpha_composite(small,((SIZE[0]-width)//2,4))
 fullmask=Image.new('L',SIZE);fullmask.paste(alpha,((SIZE[0]-width)//2,4))
 native.putalpha(fullmask)
 # Keep the same white material. Warm photo lighting is reduced to the game's neutral ramp.
 ramp=['gris-azul','gris','gris-claro','blanco']
 result=Image.new('RGBA',SIZE)
 for y in range(SIZE[1]):
  for x in range(SIZE[0]):
   r,g,b,a=native.getpixel((x,y))
   if not a:continue
   brightness=min(255,lum((r,g,b))+16)
   name=min(ramp,key=lambda n:abs(lum(rgba(n)[:3])-brightness))
   result.putpixel((x,y),rgba(name))
 result.save(ROOT/'customer-full-1x.png')
 result.resize((384,708),Image.Resampling.NEAREST).save(ROOT/'customer-full-6x.png')
 counter=result.crop((0,0,SIZE[0],80));counter.save(ROOT/'customer-counter-1x.png')
 counter.resize((384,480),Image.Resampling.NEAREST).save(ROOT/'customer-counter-6x.png')
 (ROOT/'full.rgba').write_bytes(result.tobytes());(ROOT/'counter.rgba').write_bytes(counter.tobytes())
 checks={'source_bbox':bounds,'native_full_size':SIZE,'native_counter_size':[64,80],'uniform_scale':HEIGHT/crop.height,'waist_row':WAIST,'alpha_binary':True,'silhouette_components':1,'palette':ramp,'method':'uniform_downsample_of_selected_image_no_anatomy_redraw','integration':'reference_only'}
 (ROOT/'import-metadata.json').write_text(json.dumps(checks,indent=2)+'\n')

if __name__=='__main__':prepare()
