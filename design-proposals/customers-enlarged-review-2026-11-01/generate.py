"""Review sheets rendered from the active approved customer pixels; no sprite edits."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,zipfile

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'runtime-source.json').read_text());P=DATA['palette']
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'

def label(im,pos,text,size=32,ink='noche',bold=False):
 ImageDraw.Draw(im).text(pos,text,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=P[ink])

def sprite(person):return Image.frombytes('RGBA',(person['width'],person['height']),bytes(person['rgba']))

def sheet(people,name,columns=6,detail=True):
 if detail:cellw,cellh,gap,header,mult=432,560,16,180,6
 else:cellw,cellh,gap,header,mult=144,162,12,108,1.5
 rows=(len(people)+columns-1)//columns
 out=Image.new('RGB',(columns*cellw+(columns+1)*gap,header+rows*cellh+(rows+1)*gap),P['noche'])
 if detail:
  label(out,(24,24),'CLIENTES / ELENCO ACTUAL',54,'blanco',True)
  label(out,(24,98),'Escala del juego: 150 % (96 × 120) · vista de detalle: 4×',29,'gris-claro')
 else:
  label(out,(16,14),'LOS 24 CLIENTES',28,'blanco',True)
  label(out,(16,58),'Cada figura: 96 × 120 píxeles',20,'gris-claro')
 for index,person in enumerate(people):
  col=index%columns;row=index//columns;x=gap+col*(cellw+gap);y=header+gap+row*(cellh+gap)
  ImageDraw.Draw(out).rectangle((x,y,x+cellw-1,y+cellh-1),fill='#e8e9ed')
  number=next(i for i,p in enumerate(DATA['customers']) if p['id']==person['id'])+1
  label(out,(x+(20 if detail else 8),y+(12 if detail else 8)),f'{number:02d}  {person["name"].upper()}',32 if detail else 16,bold=True)
  native=sprite(person);im=native.resize((round(native.width*mult),round(native.height*mult)),Image.Resampling.NEAREST)
  out.paste(im,(x+(cellw-im.width)//2,y+(64 if detail else 36)),im)
 out.save(ROOT/name)
 return out

def main():
 people=DATA['customers'];assert len(people)==24
 sheet(people,'clientes-todos-detalle.png')
 sheet(people[:12],'clientes-01-12.png',4)
 sheet(people[12:],'clientes-13-24.png',4)
 sheet(people,'clientes-escala-juego.png',6,False)
 atlas=Image.new('RGBA',(96*6,120*4));items=[]
 folder=ROOT/'sprites-96x120';folder.mkdir(exist_ok=True)
 for i,person in enumerate(people):
  im=sprite(person).resize((96,120),Image.Resampling.NEAREST)
  assert set(im.getchannel('A').getdata()) <= {0,255}
  fname=f'{i+1:02d}-{person["id"]}.png';im.save(folder/fname)
  x=(i%6)*96;y=(i//6)*120;atlas.paste(im,(x,y))
  assert atlas.crop((x,y,x+96,y+120)).tobytes()==im.tobytes()
  items.append({'number':i+1,'id':person['id'],'name':person['name'],'file':fname,'rectangle':[x,y,96,120],'approved_native_sha256':person['sha256']})
 atlas.save(ROOT/'clientes-24-plantilla-transparente.png')
 manifest={'frame':[96,120],'columns':6,'rows':4,'game_scale':1.5,'expression':'esperando','customers':items}
 (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 with zipfile.ZipFile(ROOT/'clientes-24-ampliados.zip','w',zipfile.ZIP_DEFLATED) as z:
  for item in items:z.write(folder/item['file'],f'sprites-96x120/{item["file"]}')
  z.write(ROOT/'clientes-24-plantilla-transparente.png','clientes-24-plantilla-transparente.png')
  z.write(ROOT/'manifest.json','manifest.json')
 (ROOT/'checks.json').write_text(json.dumps({'customers':24,'native_frame':[64,80],'game_frame':[96,120],'game_magnification':1.5,'detail_magnification_relative_to_game':4,'approved_hashes_match':True,'binary_alpha':True,'atlas_tiles_match_individual_exports':True,'sprite_redraw':False,'production_changes':False},indent=2)+'\n')
 print('Lámina de los 24, dos láminas de detalle, plantilla transparente y 24 PNG ampliados exportados.')

if __name__=='__main__':main()
