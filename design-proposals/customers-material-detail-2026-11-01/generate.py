"""Reference-only material detailing of the 24 approved native customer matrices."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,copy,hashlib,importlib.util

ROOT=Path(__file__).resolve().parent
CAST=json.loads((ROOT/'source-cast.json').read_text())
ENV=json.loads((ROOT/'scene-source.json').read_text());P=ENV['palette']
COLORS=CAST['colors']|{'d':'durazno','j':'naranja','l':'amarillo','m':'verde-claro'}
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
# main fill, one-step material light, material shadow, finish
CONFIG={
 'nico':('o','n','p','twill'), 'ren':('y','x','z','leather'),
 'alex':('y','x','z','technical'),'dani':('i','D','h','jersey'),
 'beto':('o','n','p','fleece'),'vale':('y','x','z','leather'),
 'mar':('f','e','g','flannel'),'sol':('b','d','a','canvas'),
 'sam':('C','D','B','varsity'),'ivo':('y','x','z','cotton'),
 'luz':('C','D','B','knit'),'noa':('C','D','B','technical'),
 'teo':('v','u','w','oxford'),'mai':('u','t','v','oxford'),
 'jules':('e','b','f','canvas'),'moren':('r','s','q','technical'),
 'chema':('o','n','p','jersey'),'ari':('x','w','y','technical'),
 'ros':('e','b','f','canvas'),'andy':('y','x','z','leather'),
 'fer':('f','e','g','twill'),'leo':('o','n','p','twill'),
 'pao':('r','s','q','varsity'),'cris':('C','D','B','knit'),
}

def rgba(name):return tuple(bytes.fromhex(P[name][1:]))+(255,)
def render(rows):
 im=Image.new('RGBA',(64,80))
 for y,row in enumerate(rows):
  for x,letter in enumerate(row):
   if letter!='.':im.putpixel((x,y),rgba(COLORS[letter]))
 return im

def enhance(person):
 src=person['pixels'];out=[list(row) for row in src]
 left,top,right,bottom=person['expression_bounds'];base,light,shade,finish=CONFIG[person['id']]
 start=max(43,bottom+2)
 # Preserve facial features and original bare-skin pixels around hands/neck.
 skin={(x,y) for y,row in enumerate(src) for x,c in enumerate(row) if c in 'EF'}
 protected=set(skin)
 for x,y in skin:
  for dx in range(-2,3):
   for dy in range(-2,3):protected.add((x+dx,y+dy))
 def face(x,y):return left<=x<right and top<=y<bottom
 def put(x,y,letter,allowed=None):
  if not(1<=x<63 and 1<=y<79) or face(x,y) or (x,y) in protected:return
  if src[y][x]=='.':return
  if allowed is not None and src[y][x] not in allowed:return
  out[y][x]=letter
 def stroke(points,letter,allowed):
  mask=Image.new('1',(64,80));ImageDraw.Draw(mask).line(points,fill=1,width=1)
  for y in range(80):
   for x in range(64):
    if mask.getpixel((x,y)):put(x,y,letter,allowed)
 # Broad flat blocks describe the fabric's lit edge and shadow under the sleeve.
 for y in range(start,77):
  xs=[x for x in range(2,62) if src[y][x]==base]
  runs=[]
  for x in xs:
   if not runs or x>runs[-1][-1]+1:runs.append([x])
   else:runs[-1].append(x)
  for run in runs:
   if len(run)<7:continue
   a,b=run[0],run[-1]
   if y<start+12:
    for x in range(a+1,min(a+3,b)):put(x,y,light,{base})
   if y>=start+8:
    for x in range(max(a+2,b-1),b+1):put(x,y,shade,{base})
 # A small set of intentional folds, clipped to the garment so poses remain unchanged.
 folds=[([(18,start+10),(21,start+11),(23,start+11)],shade),
        ([(44,start+11),(41,start+13),(40,start+13)],shade),
        ([(23,70),(26,71),(28,71)],shade),
        ([(38,74),(41,73),(43,73)],light)]
 for pts,ink in folds:stroke(pts,ink,{base})
 if finish in ['twill','canvas','oxford','flannel']:
  # Short stitching along existing garment panels; not a uniform noise overlay.
  for x in [21,43]:
   for y in range(start+9,75,5):
    stroke([(x,y),(x,y+1)],light,{base})
  for x,y in [(19,61),(24,65),(45,58),(47,69),(26,74)]:
   stroke([(x,y),(x+1,y)],light,{base})
 if finish=='flannel':
  for x in [19,24,42,47]:stroke([(x,start+4),(x,76)],'h',{base})
  for y in [start+9,start+20,74]:stroke([(14,y),(49,y)],'h',{base})
 elif finish=='leather':
  # Broken reflective planes on leather lapels and sleeves.
  for points in [[(20,start+4),(18,start+7),(18,start+12)],[(44,start+8),(46,start+11),(45,start+14)],[(21,65),(23,66)]]:
   stroke(points,light,{base})
  for x,y in [(24,start+8),(41,start+9),(25,75)]:put(x,y,'w',{base,light})
 elif finish=='technical':
  for pts in [[(22,start+8),(27,start+8),(27,start+12)],[(39,start+9),(44,start+9)],[(21,65),(22,68)]]:
   stroke(pts,light,{base})
  for x,y in [(24,start+8),(41,start+9),(31,74)]:put(x,y,'w' if base=='y' else 'u',{base,light})
 elif finish=='jersey':
  # Sparse paired eyelets and side ribbing preserve the shirt number/crest.
  for x,y in [(23,start+7),(39,start+8),(26,start+16),(40,start+20),(30,73),(37,70)]:
   stroke([(x,y),(x+1,y)],shade,{base})
  for x in [21,44]:stroke([(x,65),(x,74)],shade,{base})
 elif finish in ['fleece','cotton','varsity','knit']:
  for x,y in [(24,start+8),(39,start+13),(26,70),(42,73)]:
   stroke([(x,y),(x+2,y+1)],shade,{base})
  if finish=='knit':
   for x,y in [(23,63),(31,67),(40,63),(27,73)]:
    stroke([(x,y),(x+1,y+1),(x+2,y)],light,{base})
  if finish=='varsity':
   for y in [70,73]:stroke([(19,y),(24,y)],light,{base})
 # Light cotton inner shirts: small folds, rather than a completely blank rectangle.
 if person['id'] in ['nico','mar','sol','fer','leo']:
  for pts,ink in [([(29,57),(31,58),(33,58)],'v'), ([(37,66),(36,69)],'v'), ([(29,73),(31,74)],'v')]:
   stroke(pts,ink,{'u'})
 # Existing bags get a seam and a little canvas grain. Never touch skin nearby.
 if person['id'] in ['sol','teo','leo']:
  for x,y in [(19,69),(20,72),(21,75),(24,73)]:put(x,y,'d',{'c'})
 # Material detail on existing headwear, with no change to its contour.
 if person['id']=='beto':
  for x in range(20,45,4):
   stroke([(x,21),(x,29)],'a',{'b'})
   stroke([(x+1,24),(x+1,26)],'d',{'b'})
 if person['id'] in ['ros','pao']:
  cap='o' if person['id']=='ros' else 'q';shine='n' if cap=='o' else 'r'
  cap_pixels=[(x,y) for y in range(top) for x in range(8,56) if src[y][x]==cap]
  if cap_pixels:
   yy=min(y for x,y in cap_pixels)+2
   xs=[x for x,y in cap_pixels if y==yy]
   if xs:stroke([(min(xs)+3,yy),(min(xs)+8,yy)],shine,{cap})
 # A few directional strands follow the crown instead of scattered bright speckles.
 hair_colors={'g':'f','f':'g','z':'g','B':'C','C':'B','b':'a','k':'b','w':'v','v':'w','u':'v'}
 eligible=[]
 for y in range(5,min(top,40)):
  for x in range(8,56):
   if src[y][x] not in hair_colors or (x,y) in protected:continue
   if all(src[y+dy][x+dx]!='.' for dx in [-1,0,1] for dy in [-1,0,1]):eligible.append((x,y))
 if eligible:
  crown_top=min(y for x,y in eligible)
  for offset in [3,7]:
   yy=crown_top+offset
   xs=[x for x,y in eligible if y==yy]
   if not xs:continue
   xx=min(xs)+2
   pts=[(xx,yy+1),(xx+2,yy),(xx+5,yy)]
   mask=Image.new('1',(64,80));ImageDraw.Draw(mask).line(pts,fill=1)
   for y in range(max(1,yy-1),min(top,yy+3)):
    for x in range(max(1,xx),min(63,xx+6)):
     c=src[y][x]
     if mask.getpixel((x,y)) and (x,y) in eligible:put(x,y,hair_colors[c],{c})
 result=[''.join(row) for row in out]
 assert all((a=='.')==(b=='.') for rowa,rowb in zip(src,result) for a,b in zip(rowa,rowb))
 assert all(result[y][x]==src[y][x] for y in range(top,bottom) for x in range(left,right))
 assert all(result[y][x]==src[y][x] for x,y in skin)
 changes=sum(a!=b for ra,rb in zip(src,result) for a,b in zip(ra,rb))
 return result,changes


def text(im,xy,label,size=30,ink='noche',bold=False):
 ImageDraw.Draw(im).text(xy,label,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=P[ink])

def sheet(people,filename,columns=6):
 cw,ch,gap,header=432,560,16,180
 rows=(len(people)+columns-1)//columns
 out=Image.new('RGB',(columns*cw+(columns+1)*gap,header+rows*ch+(rows+1)*gap),P['noche'])
 text(out,(24,24),'CLIENTES / DETALLE DE MATERIALES',50,'blanco',True)
 text(out,(24,98),'Prueba de acabado · ropa, cabello y accesorios · caras y siluetas conservadas',27,'gris-claro')
 for i,p in enumerate(people):
  x=gap+(i%columns)*(cw+gap);y=header+gap+(i//columns)*(ch+gap)
  ImageDraw.Draw(out).rectangle((x,y,x+cw-1,y+ch-1),fill='#e8e9ed')
  text(out,(x+20,y+12),f'{p["number"]:02d}  {p["name"].upper()}',32,bold=True)
  im=render(p['pixels']).resize((384,480),Image.Resampling.NEAREST)
  out.paste(im,(x+24,y+64),im)
 out.save(ROOT/filename)

def comparison(people):
 # Six different fabrics, original vs proposed, at matching native scale.
 chosen=['nico','ren','dani','mar','jules','ari']
 out=Image.new('RGB',(2400,1260),P['noche'])
 text(out,(24,20),'ANTES / PROPUESTA CON MÁS DETALLE',44,'blanco',True)
 text(out,(24,80),'Mismos personajes y proporciones · acabado distinto según el material',25,'gris-claro')
 for index,key in enumerate(chosen):
  p=next(p for p in people if p['id']==key);original=next(p for p in CAST['customers'] if p['id']==key)
  x=24+(index%3)*792;y=146+(index//3)*550
  ImageDraw.Draw(out).rectangle((x,y,x+768,y+526),fill='#e8e9ed')
  text(out,(x+20,y+12),p['name'].upper()+' / '+p['style'],26,bold=True)
  for bx,title,rows in [(x+40,'ANTES',original['pixels']),(x+416,'PROPUESTA',p['pixels'])]:
   text(out,(bx,y+53),title,20)
   im=render(rows).resize((320,400),Image.Resampling.NEAREST);out.paste(im,(bx,y+94),im)
 out.save(ROOT/'antes-despues.png')

def main():
 output=copy.deepcopy(CAST);output['colors']=COLORS
 checks=[]
 for i,p in enumerate(output['customers']):
  p['pixels'],changes=enhance(p);p['number']=i+1
  assert changes>20
  p['proposal_sha256']=hashlib.sha256(render(p['pixels']).tobytes()).hexdigest()
  render(p['pixels']).save(ROOT/f'{i+1:02d}-{p["id"]}-1x.png')
  checks.append({'id':p['id'],'changed_pixels':changes,'silhouette_preserved':True,'face_preserved':True,'bare_skin_base_preserved':True})
 used=set(''.join(''.join(p['pixels']) for p in output['customers']))-{'.'}
 output['colors']={k:v for k,v in COLORS.items() if k in used}
 output['status']='reference_only';(ROOT/'proposal-cast.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
 sheet(output['customers'],'clientes-detalle-todos.png')
 sheet(output['customers'][:12],'clientes-detalle-01-12.png',4)
 sheet(output['customers'][12:],'clientes-detalle-13-24.png',4)
 comparison(output['customers'])
 (ROOT/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
 print(json.dumps(checks))

if __name__=='__main__':main()
