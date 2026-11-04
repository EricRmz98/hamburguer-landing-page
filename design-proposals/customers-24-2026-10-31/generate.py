"""Reference-only cast. Reuses native people proportions; never writes runtime sprites."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys,json,re,importlib.util
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
sys.path.insert(0,str(REPO/'scripts/sprites'))
import people_gen as people
P={a or b:h for a,b,h in re.findall(r"(?:'([^']+)'|([\w-]+)):\s*'(#[0-9a-f]{6})'",(REPO/'src/game/sprites/palette.ts').read_text())}
def col(v):return P.get(v,v)
def rect(im,b,c):ImageDraw.Draw(im).rectangle(b,fill=col(c))
def line(im,pts,c,w=1):ImageDraw.Draw(im).line(pts,fill=col(c),width=w)
def poly(im,pts,c):ImageDraw.Draw(im).polygon(pts,fill=col(c))
def oval(im,b,c):ImageDraw.Draw(im).ellipse(b,fill=col(c))
def rr(im,b,c,outline='negro',r=2):ImageDraw.Draw(im).rounded_rectangle(b,radius=r,fill=col(c),outline=col(outline))
SKINS=[('canela','piel','piel-clara'),('piel','piel-clara','crema'),('cafe-oscuro','cafe','canela'),('cafe','canela','piel'),('canela','piel-clara','crema'),('cafe','piel','piel-clara')]
HAIR=[('negro','cafe-oscuro','cafe'),('cafe-oscuro','cafe','canela'),('cafe','oxido','tostado'),('tostado','ambar','amarillo'),('ciruela','magenta','rosa'),('noche','pizarra','gris-azul'),('verde-noche','verde-oscuro','verde'),('pizarra','gris','gris-claro')]
# name, style, pronouns, hair form, hair ramp, skin ramp, garment, cloth shadow/base/light, accessory
CAST=[
('Nico','Hipster','él','quiff',1,0,'flannel',('verde-noche','verde-oscuro','verde'),'glasses_beard'),
('Ren','Gótica','ella','long',0,1,'leather',('negro','noche','pizarra'),'choker'),
('Alex','Techwear','elle','undercut',5,3,'tech',('negro','noche','pizarra'),'earbuds'),
('Dani','Fútbol','ella','ponytail',1,2,'jersey',('rojo-oscuro','rojo','rosa'),'headband'),
('Beto','Skater','él','shag',2,4,'hoodie',('verde-noche','verde-oscuro','verde'),'beanie'),
('Vale','Punk','elle','mohawk',4,0,'leather',('negro','noche','pizarra'),'piercing'),
('Mar','Grunge','él','long',0,3,'flannel',('rojo-oscuro','cafe','canela'),'stubble'),
('Sol','Indie','ella','bob',1,5,'cardigan',('oxido','tostado','durazno'),'roundglasses'),
('Sam','Streetwear','elle','braids',0,2,'varsity',('ciruela','magenta','rosa'),'chain'),
('Ivo','Metal','él','long',0,4,'band',('negro','noche','pizarra'),'beard'),
('Luz','Kawaii','ella','buns',4,1,'sweater',('ciruela','magenta','rosa'),'clips'),
('Noa','Rave','elle','undercut',6,3,'rave',('ciruela','magenta','rosa'),'goggles'),
('Teo','Normcore','él','crop',1,0,'overshirt',('gris-azul','gris','gris-claro'),'tote'),
('Mai','Coquette','ella','wavy',2,5,'blouse',('gris','gris-claro','blanco'),'bow'),
('Jules','Art school','elle','curly',1,2,'utility',('cafe','canela','piel'),'scarf'),
('Moren','Athleisure','ella','bun',0,3,'tracksuit',('azul-oscuro','azul','gris-claro'),'headphones'),
('Chema','Fútbol retro','él','curly',0,4,'retro',('verde-noche','verde-oscuro','verde'),'moustache'),
('Ari','Cyber','elle','asym',5,1,'tech',('noche','pizarra','gris-azul'),'visor'),
('Ros','Workwear','él','crop',0,2,'utility',('cafe-oscuro','cafe','canela'),'cap'),
('Andy','Rockabilly','ella','quiff',0,5,'leather',('negro','noche','pizarra'),'bandana'),
('Fer','Dark academia','elle','bob',1,3,'blazer',('cafe-oscuro','cafe','canela'),'roundglasses'),
('Leo','Surf','él','wavy',3,0,'hawaiian',('verde-noche','verde-oscuro','verde'),'shells'),
('Pao','Sneakerhead','ella','braids',1,2,'varsity',('azul-oscuro','azul','gris-claro'),'capback'),
('Cris','Vintage','elle','curly',7,4,'vest',('ciruela','magenta','rosa'),'glasses'),
]

def hair_back(im,kind,hs,hb,hl):
 if kind in ['long','wavy','braids']:
  rr(im,(10,4,37,45),hs,r=8);rect(im,(12,17,15,40),hb);line(im,[(13,11),(13,31)],hl)
 if kind=='ponytail':rr(im,(31,10,40,39),hs,r=4);line(im,[(35,15),(35,33)],hb)
 if kind in ['buns','bun']:
  for x in ([10,30] if kind=='buns' else [20]):oval(im,(x,0,x+9,9),hs);oval(im,(x+1,1,x+6,5),hb)

def hair_front(im,kind,hs,hb,hl):
 if kind=='curly':
  for x,y,r in [(12,5,7),(17,1,8),(24,0,9),(30,3,8),(34,7,6)]:
   oval(im,(x-r//2,y,x+r//2,y+r),hs);oval(im,(x-r//2+1,y+1,x+r//2-2,y+r-2),hb)
  for x,y in [(16,5),(22,3),(28,4),(32,7)]:line(im,[(x,y),(x+2,y)],hl)
 elif kind=='mohawk':
  poly(im,[(18,8),(19,2),(22,3),(24,0),(27,2),(29,8)],hs)
  poly(im,[(20,7),(21,3),(24,2),(27,4),(27,8)],hb);line(im,[(22,3),(24,2)],hl)
  rect(im,(13,8,15,11),hs);rect(im,(33,8,34,11),hs)
 elif kind=='quiff':
  poly(im,[(12,12),(13,5),(17,3),(18,0),(24,1),(27,0),(32,3),(35,9),(32,11),(29,7),(18,7),(15,13)],hs)
  poly(im,[(15,5),(19,2),(25,2),(30,4),(22,6),(16,8)],hb);line(im,[(18,3),(24,3)],hl)
 elif kind in ['undercut','asym']:
  poly(im,[(13,10),(14,4),(21,0),(30,1),(35,6),(32,9),(22,8),(17,14)],hs)
  poly(im,[(15,6),(21,2),(29,2),(32,5),(23,7),(17,11)],hb);line(im,[(20,3),(27,3)],hl)
  if kind=='asym':poly(im,[(13,9),(20,6),(17,19),(13,23)],hb);line(im,[(15,13),(15,19)],hl)
  else:line(im,[(32,10),(34,10)],'gris-azul')
 elif kind in ['long','wavy','braids']:
  poly(im,[(12,14),(12,7),(16,2),(24,0),(32,3),(36,8),(35,18),(32,12),(29,7),(24,6),(16,9),(15,19)],hs)
  line(im,[(14,8),(17,4),(22,2)],hb,2)
  if kind=='braids':
   for x in [13,33]:
    for y in range(11,43,5):rr(im,(x-2,y,x+2,y+5),hb,hs,1);rect(im,(x-1,y+1,x,y+2),hl)
  else:
   for x in [12,33]:
    line(im,[(x,12),(x-1,25),(x+1,36)],hb,2)
    if kind=='wavy':line(im,[(x+1,16),(x-1,22),(x+1,28)],hl)
 elif kind=='bob':
  poly(im,[(11,24),(11,10),(14,4),(20,1),(29,1),(35,6),(37,24),(32,25),(32,9),(24,7),(17,9),(16,25)],hs)
  line(im,[(14,9),(15,6),(20,3),(27,3)],hb,2);line(im,[(13,13),(13,22)],hl)
 elif kind=='shag':
  poly(im,[(11,16),(12,7),(16,3),(23,1),(31,3),(36,8),(37,16),(33,13),(31,9),(27,12),(24,8),(19,12),(16,9),(14,16)],hs)
  line(im,[(15,6),(23,3),(30,5)],hb,2);line(im,[(18,5),(23,4)],hl)
 else:
  # Cropped, tied or bun style: keep the original face proportions and hairline.
  poly(im,[(12,11),(13,5),(18,1),(27,0),(33,3),(35,9),(33,12),(31,8),(16,8),(14,13)],hs)
  poly(im,[(15,6),(18,3),(26,2),(31,4),(29,6)],hb);line(im,[(17,4),(22,3)],hl)

def garment(im,kind,cs,cb,cl,index):
 # The native body supplies arms and shoulder shading. Construction details sit on top.
 inner='gris-claro' if kind not in ['band','tech','rave'] else 'noche'
 if kind in ['flannel','overshirt','hawaiian','leather','utility','blazer','cardigan','vest']:
  poly(im,[(18,32),(29,32),(31,43),(29,79),(18,79),(17,43)],inner)
  if kind=='vest':
   for b in [(3,36,9,79),(38,36,44,79)]:rect(im,b,'gris-claro')
  poly(im,[(16,32),(21,37),(18,42),(17,79),(11,79),(12,39)],cs)
  poly(im,[(31,32),(27,38),(30,43),(30,79),(35,79),(35,38)],cs)
  line(im,[(15,35),(18,39),(16,44),(16,75)],cl)
  line(im,[(32,35),(29,39),(31,44),(31,75)],cl)
  if kind=='flannel':
   for xx in [7,12,34,40]:line(im,[(xx,38),(xx,75)],cs)
   for yy in [41,48,55,62,69]:
    line(im,[(4,yy),(15,yy)],cl);line(im,[(32,yy),(43,yy)],cl)
  if kind in ['leather','blazer']:
   poly(im,[(15,33),(22,40),(17,46),(13,39)],cl)
   poly(im,[(32,33),(27,40),(31,45),(35,39)],cs)
   line(im,[(17,46),(15,74)],'gris-azul')
   line(im,[(6,52),(12,49)],'gris');line(im,[(35,50),(41,52)],'gris-azul')
  if kind in ['utility','overshirt','vest']:
   for xx in [6,34]:
    rr(im,(xx,43,xx+7,53),cb,cs,1);line(im,[(xx+1,45),(xx+6,45)],cl);rect(im,(xx+4,47,xx+4,47),'ambar')
  if kind=='hawaiian':
   for xx,yy in [(8,43),(36,39),(12,58),(38,59),(7,70)]:
    rect(im,(xx,yy,xx+3,yy+1),'crema');rect(im,(xx+1,yy-1,xx+2,yy+2),'crema');rect(im,(xx+1,yy,xx+1,yy),'oxido')
  if kind=='cardigan':
   for yy in [45,53,61,69]:rect(im,(16,yy,17,yy),'crema')
 if kind=='hoodie':
  poly(im,[(14,31),(18,33),(23,37),(29,33),(33,31),(32,39),(25,43),(17,38)],cs)
  line(im,[(15,33),(22,40)],cl);line(im,[(24,40),(31,34)],cl)
  for xx in [20,27]:line(im,[(xx,41),(xx,50)],'gris-claro')
  rr(im,(14,61,33,73),cb,cs,2);line(im,[(17,63),(30,63)],cl)
 if kind in ['jersey','retro']:
  for xx in [8,37]:rect(im,(xx,34,xx+2,49),'gris-claro')
  poly(im,[(17,31),(23,37),(29,31),(30,34),(23,40),(16,34)],'gris-claro')
  if kind=='retro':
   for xx in [15,29]:rect(im,(xx,40,xx+3,79),'crema')
  # Fictional crest, no real club logo.
  rr(im,(29,43,34,49),'crema',cs,1);rect(im,(31,45,32,47),cb)
  line(im,[(17,50),(20,48),(20,59)],'blanco',2);line(im,[(25,49),(30,49),(25,59),(30,59)],'blanco')
 if kind=='varsity':
  for b in [(3,37,10,79),(37,37,44,79)]:rect(im,b,'gris-claro')
  line(im,[(11,38),(11,76)],cs);line(im,[(36,38),(36,76)],cs)
  rect(im,(22,36,24,79),cs)
  for yy in [43,52,61,70]:rect(im,(23,yy,23,yy),'crema')
  line(im,[(15,44),(15,52),(19,52)],'crema',2)
  for yy in [74,77]:line(im,[(4,yy),(10,yy)],cb);line(im,[(37,yy),(43,yy)],cb)
 if kind in ['tech','rave','tracksuit']:
  rr(im,(17,31,30,38),cs,cs,1);line(im,[(23,33),(23,79)],cl)
  if kind=='tech':
   poly(im,[(14,38),(17,38),(36,65),(33,66)],'gris-azul')
   rr(im,(8,51,16,62),cs,'negro',1);rect(im,(10,53,14,54),'gris')
   rect(im,(32,42,34,45),'verde-claro' if index==17 else 'gris-claro')
  if kind=='rave':
   for xx in [8,37]:line(im,[(xx,37),(xx,72)],'cian',2)
   line(im,[(14,47),(31,47)],'cian');rr(im,(19,59,31,68),'noche','ciruela',1)
  if kind=='tracksuit':
   for xx in [5,8,38,41]:line(im,[(xx,38),(xx,75)],'gris-claro')
   line(im,[(14,46),(32,46)],'gris-claro')
 if kind=='band':
  rr(im,(14,43,33,62),'pizarra','negro',1)
  poly(im,[(17,57),(20,48),(24,52),(28,46),(30,57)],'gris-claro')
  line(im,[(18,59),(29,59)],'rojo-oscuro')
 if kind=='sweater':
  for yy in [42,46]:line(im,[(8,yy),(39,yy)],cl)
  # Tiny star motif, large enough to read at native resolution.
  poly(im,[(24,49),(26,54),(31,54),(27,57),(28,62),(24,59),(20,62),(21,57),(17,54),(22,54)],'crema')
 if kind=='blouse':
  poly(im,[(14,32),(22,36),(18,42),(13,37)],'blanco');poly(im,[(33,32),(25,36),(29,42),(35,37)],'blanco')
  for yy in [45,53,61,69]:rect(im,(23,yy,24,yy),'gris-azul')
  line(im,[(4,40),(10,40)],'blanco',2);line(im,[(37,40),(43,40)],'blanco',2)


def accessories(im,acc,skin,hs,hb):
 if acc in ['glasses','roundglasses','glasses_beard']:
  for xx in [15,26]:
   rr(im,(xx,11,xx+7,17),'gris-azul','negro',2 if acc=='roundglasses' else 1)
   rect(im,(xx+1,12,xx+2,13),'gris-claro');rect(im,(xx+3,13,xx+4,14),skin)
  line(im,[(23,13),(26,13)],'negro')
 if acc in ['beard','glasses_beard','stubble','moustache']:
  if acc in ['beard','glasses_beard']:
   poly(im,[(16,18),(19,20),(22,19),(26,19),(30,18),(30,22),(27,26),(22,26),(18,23)],hs)
   line(im,[(20,20),(26,20)],'negro');line(im,[(20,23),(23,24)],hb)
  elif acc=='moustache':line(im,[(19,19),(22,18),(24,19),(26,18),(29,19)],hs,2)
  else:
   for xx,yy in [(18,21),(20,23),(23,24),(27,22),(29,20)]:rect(im,(xx,yy,xx,yy),hs)
 if acc in ['choker','piercing']:
  if acc=='choker':
   line(im,[(19,28),(28,28)],'negro',2);rect(im,(23,28,24,29),'gris')
   line(im,[(22,37),(24,41),(26,37)],'gris');rect(im,(24,40,24,43),'gris-claro')
  else:
   rect(im,(25,17,26,17),'gris');rect(im,(13,18,14,19),'gris');rect(im,(29,21,29,21),'gris')
   for xx in [7,11,35,39]:rect(im,(xx,35,xx,36),'gris-claro')
   rr(im,(7,44,12,49),'rojo-oscuro','negro',1);line(im,[(8,46),(11,46)],'gris-claro')
   line(im,[(32,54),(35,58),(39,56)],'gris')
 if acc=='earbuds':rect(im,(12,14,13,18),'gris-claro');rect(im,(34,14,35,18),'gris-claro')
 if acc in ['headband','bandana']:
  line(im,[(13,7),(34,7)],'rojo' if acc=='bandana' else 'gris-claro',3)
  if acc=='bandana':
   for xx in [16,23,30]:rect(im,(xx,7,xx,7),'blanco')
   poly(im,[(33,8),(38,10),(36,14),(34,11)],'rojo-oscuro')
 if acc=='beanie':
  rr(im,(12,0,35,8),'oxido','cafe-oscuro',5);rect(im,(12,6,35,10),'tostado')
  for xx in range(15,35,4):line(im,[(xx,7),(xx,9)],'canela')
 if acc=='chain':line(im,[(18,33),(20,39),(25,41),(29,37)],'ambar');rect(im,(24,40,25,42),'amarillo')
 if acc=='clips':
  for xx in [13,31]:rect(im,(xx,9,xx+3,10),'cian');rect(im,(xx,12,xx+2,13),'amarillo')
 if acc in ['goggles','visor']:
  if acc=='goggles':
   rr(im,(13,4,22,9),'cian','noche',2);rr(im,(25,4,34,9),'magenta','noche',2);line(im,[(22,6),(25,6)],'gris')
  else:rr(im,(14,11,33,16),'azul-oscuro','noche',2);line(im,[(16,12),(27,12)],'cian')
 if acc=='tote':line(im,[(9,34),(13,57),(15,78)],'crema',3);rr(im,(5,65,15,79),'crema','canela',1)
 if acc=='bow':
  poly(im,[(24,34),(18,31),(18,37),(24,35),(30,31),(30,37)],'rosa');rect(im,(23,34,24,36),'magenta')
 if acc=='scarf':
  poly(im,[(17,29),(29,29),(30,34),(22,36),(19,45),(16,42),(18,34)],'ambar');line(im,[(18,32),(28,32)],'tostado')
 if acc=='headphones':
  line(im,[(11,15),(11,6),(16,1),(30,1),(36,7),(36,16)],'noche',2)
  rr(im,(10,12,13,21),'pizarra','negro',1);rr(im,(34,12,37,21),'pizarra','negro',1)
 if acc in ['cap','capback']:
  rr(im,(12,0,35,7),'verde-oscuro' if acc=='cap' else 'azul-oscuro','negro',4)
  if acc=='cap':rect(im,(19,6,38,8),'verde-noche');line(im,[(18,2),(24,1)],'verde')
  else:rect(im,(9,6,17,8),'azul-oscuro');rect(im,(20,5,27,7),'gris')
 if acc=='shells':
  line(im,[(18,32),(21,36),(26,37),(29,32)],'crema')
  for xx,yy in [(21,35),(24,36),(27,35)]:rect(im,(xx,yy,xx,yy+1),'blanco')


def render(index):
 name,style,pronouns,hair,hi,si,kind,cloth,acc=CAST[index]
 ps,pb,pl=SKINS[si];hs,hb,hl=HAIR[hi];cs,cb,cl=cloth
 im=Image.new('RGBA',(48,80));hair_back(im,hair,hs,hb,hl)
 rows=people.face(people.paint(people.body(False)),False,'esperando')
 colors={'o':'negro','p':ps,'q':pb,'r':pl,'h':hs,'i':hs,'j':hl,'c':cb,'d':cs,'e':cl}
 for y,row in enumerate(rows):
  for x,k in enumerate(row):
   if k=='.' or (k in 'hij' and y!=11):continue
   color=col(colors[k]);im.putpixel((x,y),tuple(bytes.fromhex(color[1:]))+(255,))
 garment(im,kind,cs,cb,cl,index)
 # Faces stay at the approved anchor. Small differences add expression without implying temperament by identity.
 if index in [3,7,10,14,21]:line(im,[(22,20),(24,21),(26,20)],'negro')
 if index in [2,11,17]:line(im,[(17,10),(20,11)],hs)
 hair_front(im,hair,hs,hb,hl)
 accessories(im,acc,pb,hs,hb)
 # A few earrings, independent of pronoun and style.
 if index in [1,5,8,13,14,19,22,23]:
  rect(im,(12,17,13,19),'gris' if index%2 else 'ambar')
 return im

FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def text(im,xy,t,size=22,color='gris-claro'):ImageDraw.Draw(im).text(xy,t,font=ImageFont.truetype(FONT,size),fill=col(color))
def sheet(start,end,title,filename):
 out=Image.new('RGB',(1360,1450),col('negro'));text(out,(32,22),title,32,'crema')
 text(out,(32,67),'REFERENCIAS · 48 × 80 px · Endesga 32 · escala ×4 · sin integrar',20,'gris')
 for k in range(start,end):
  j=k-start;x=32+(j%4)*332;y=113+(j//4)*436
  name,style,pro,*_=CAST[k]
  text(out,(x,y),f'{k+1:02}  {name}',26,'crema');text(out,(x,y+33),f'{style} · {pro}',20)
  bg=Image.new('RGB',(264,328),col('noche'))
  # Native sprite ×4; no filters or fractional scaling.
  im=render(k).resize((192,320),Image.Resampling.NEAREST);bg.paste(im,(36,4),im)
  out.paste(bg,(x,y+70))
 text(out,(32,1424),'Elige por número. Podemos combinar peinado, ropa y accesorios entre personajes.',17,'gris')
 out.save(ROOT/filename)

def context_sheet():
 spec=importlib.util.spec_from_file_location('cast_environment',REPO/'scripts/sprites/environment_gen.py')
 env=importlib.util.module_from_spec(spec);spec.loader.exec_module(env)
 definitions=json.loads((REPO/'design-proposals/kitchen-2026-10-31/source-sprites.json').read_text())
 def sprite(im,key,x,y):
  d=definitions['sprites'][key];piece=Image.new('RGBA',(d['width'],d['height']))
  for yy,row in enumerate(d['frames'][0]):
   for xx,letter in enumerate(row):
    if letter!='.':piece.putpixel((xx,yy),tuple(bytes.fromhex(P[d['colors'][letter]][1:]))+(255,))
  im.paste(piece,(x,y),piece)
 out=Image.new('RGB',(1400,1580),col('negro'))
 text(out,(32,22),'PRUEBA DE ESCALA / CON LOS OBJETOS FINALES',30,'crema')
 text(out,(32,67),'Mismas posiciones del juego · sin comanda ni ayudas para comparar al personaje',20,'gris')
 for j,i in enumerate([0,1,2,3,5,10]):
  x=32+j%2*680;y=120+j//2*480
  text(out,(x,y),f'{i+1:02}  {CAST[i][0]} / {CAST[i][1]}',24,'crema')
  im=Image.new('RGB',(320,200),col('noche'));im.paste(env.dining_horizontal(),(0,0))
  person=render(i);im.paste(person,(136,46),person);im.paste(env.red_bar(),(0,122))
  sprite(im,'plato',145,120)
  for k,xx in [('bote:catsup',194),('bote:mostaza',210),('bote:mayonesa',226)]:sprite(im,k,xx,103)
  for k,xx in [('bandeja_pan',64),('bandeja_queso',103),('bandeja_lechuga',142),('bandeja_tomate',181),('bandeja_cebolla',220)]:sprite(im,k,xx,139)
  sprite(im,'plancha',82,165);sprite(im,'charola',244,165);sprite(im,'basura',40,170)
  for k,xx,yy in [('pan_base',148,120),('carne:perfecta',147,117),('queso',148,114),('lechuga',146,111),('pan_tapa',148,105)]:sprite(im,k,xx,yy)
  out.paste(im.resize((640,400),Image.Resampling.NEAREST),(x,y+42))
 out.save(ROOT/'customers-in-context.png')

if __name__=='__main__':
 manifest=[];matrices={};allowed={tuple(bytes.fromhex(v[1:])) for v in P.values()}
 for i,entry in enumerate(CAST):
  im=render(i);im.save(ROOT/f'customer-{i+1:02}-1x.png')
  assert all(a==0 or (r,g,b) in allowed for r,g,b,a in im.getdata())
  letters='abcdefghijklmnopqrstuvwxyzABCDEF';used=sorted({p[:3] for p in im.getdata() if p[3]});lookup={p:letters[k] for k,p in enumerate(used)}
  reverse={tuple(bytes.fromhex(v[1:])):k for k,v in P.items()}
  matrices[f'customer_{i+1:02}']={'size':[48,80],'colors':{lookup[p]:reverse[p] for p in used},'pixels':[''.join(lookup[p[:3]] if p[3] else '.' for p in [im.getpixel((x,y)) for x in range(48)]) for y in range(80)]}
  manifest.append({'id':i+1,'name':entry[0],'style':entry[1],'pronouns':entry[2],'hair':entry[3],'garment':entry[6],'accessory':entry[8]})
 (ROOT/'cast.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 (ROOT/'candidate-matrices.json').write_text(json.dumps(matrices,ensure_ascii=False))
 sheet(0,12,'CLIENTES / 01—12','customers-01-12.png');sheet(12,24,'CLIENTES / 13—24','customers-13-24.png')
 context_sheet()
 print('24 reference sprites, two sheets, cast manifest and candidate matrices; Endesga 32 verified.')
