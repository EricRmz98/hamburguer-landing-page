"""Layout only: arrange the twelve original image_gen outputs for review."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'prompts.json').read_text())
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
BG='#262b44';PAPER='#e8e9ed';INK='#262b44'
def text(im,xy,label,size=30,color=INK,bold=False):
 ImageDraw.Draw(im).text(xy,label,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color)

def sheet(people,filename,columns=4):
 cw,ch,gap,header=520,760,20,160
 rows=(len(people)+columns-1)//columns
 out=Image.new('RGB',(columns*cw+(columns+1)*gap,header+rows*ch+(rows+1)*gap),BG)
 text(out,(24,24),'12 NUEVOS CLIENTES / PROPUESTA',48,'#ffffff',True)
 text(out,(24,96),'Nueva dirección visual · referencias de personajes para el minijuego',25,'#c0cbdc')
 for i,p in enumerate(people):
  x=gap+(i%columns)*(cw+gap);y=header+gap+(i//columns)*(ch+gap)
  ImageDraw.Draw(out).rectangle((x,y,x+cw-1,y+ch-1),fill=PAPER)
  text(out,(x+20,y+10),p['id'][:2]+'  '+p['name'].upper(),32,bold=True)
  text(out,(x+20,y+50),p['style'],23)
  im=Image.open(ROOT/p['local_file']).convert('RGBA')
  # A uniform crop to visible content and uniform scaling only; preserve the generated alpha.
  bounds=im.getchannel('A').point(lambda a:255 if a>=160 else 0).getbbox()
  if bounds:im=im.crop(bounds)
  scale=min((cw-36)/im.width,(ch-102)/im.height)
  im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
  out.paste(im,(x+(cw-im.width)//2,y+88),im)
 out.save(ROOT/filename)

people=DATA['characters'];assert len(people)==12 and len({p['id'] for p in people})==12
sheet(people,'clientes-nuevos-12.png')
sheet(people[:6],'clientes-nuevos-01-06.png',3)
sheet(people[6:],'clientes-nuevos-07-12.png',3)
checks=[]
for p in people:
 im=Image.open(ROOT/p['local_file'])
 checks.append({'id':p['id'],'size':im.size,'mode':im.mode,'alpha_range':im.getchannel('A').getextrema(),'file':p['local_file']})
(ROOT/'checks.json').write_text(json.dumps({'count':12,'mode':'reference_designs','game_files_changed':False,'images':checks},indent=2)+'\n')
with zipfile.ZipFile(ROOT/'12-clientes-referencias.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in people:z.write(ROOT/p['local_file'],p['local_file'])
 for f in ['clientes-nuevos-12.png','clientes-nuevos-01-06.png','clientes-nuevos-07-12.png','prompts.json','style-reference.png','README.md']:
  if (ROOT/f).exists():z.write(ROOT/f,f)
print('12 referencias originales, lámina completa, dos hojas de detalle y ZIP preparados.')
