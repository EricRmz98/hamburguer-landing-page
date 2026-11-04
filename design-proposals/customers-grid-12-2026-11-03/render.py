from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,importlib.util,zipfile
ROOT=Path(__file__).resolve().parent
M=json.loads((ROOT/'manifest.json').read_text());P=json.loads((ROOT/'palette.json').read_text())
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def text(im,xy,label,size=28,color='noche',bold=False):
 ImageDraw.Draw(im).text(xy,label,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=P.get(color,color))
def sprite(p):return Image.open(ROOT/p['file']).convert('RGBA')
def sheet(people,name,cols=4,native=False):
 cw,ch,gap,header=(152,172,12,110) if native else (432,560,16,160)
 mult=1.5 if native else 6
 rows=(len(people)+cols-1)//cols
 out=Image.new('RGB',(cols*cw+(cols+1)*gap,header+rows*ch+(rows+1)*gap),P['noche'])
 text(out,(20,20),'12 CLIENTES / CUADRÍCULA DEL JUEGO',26 if native else 44,'blanco',True)
 text(out,(20,68 if native else 92),'64 × 80 píxeles · paleta Endesga 32'+('' if native else ' · ampliación sin suavizado'),18 if native else 25,'gris-claro')
 for i,p in enumerate(people):
  x=gap+(i%cols)*(cw+gap);y=header+gap+(i//cols)*(ch+gap)
  ImageDraw.Draw(out).rectangle((x,y,x+cw-1,y+ch-1),fill='#e8e9ed')
  text(out,(x+10,y+8),p['id'][:2]+' '+p['name'].upper(),16 if native else 30,bold=True)
  im=sprite(p).resize((round(64*mult),round(80*mult)),Image.Resampling.NEAREST)
  out.paste(im,(x+(cw-im.width)//2,y+(36 if native else 64)),im)
 out.save(ROOT/name)
def context():
 spec=importlib.util.spec_from_file_location('context',ROOT.parent/'generic-customer-game-palette-2026-11-01/render.py');ctx=importlib.util.module_from_spec(spec);spec.loader.exec_module(ctx)
 out=Image.new('RGB',(1344,1450),P['noche'])
 text(out,(20,20),'PRUEBA EN EL ENTORNO / ESCALA ACTUAL',34,'blanco',True)
 for i,key in enumerate(['01-lia','02-bruno','03-zoe','04-ciro','09-vega','12-sasha']):
  p=next(p for p in M['characters'] if p['id']==key);ctx.prototype=lambda p=p:sprite(p)
  x=16+(i%2)*664;y=96+(i//2)*448
  text(out,(x,y),p['id'][:2]+' '+p['name'].upper(),25,'blanco',True)
  im=ctx.scene().resize((640,400),Image.Resampling.NEAREST);out.paste(im,(x,y+34),im)
 out.save(ROOT/'prueba-en-entorno.png')
 p=M['characters'][0];ctx.prototype=lambda:sprite(p)
 im=ctx.scene('vertical');im.resize((720,1120),Image.Resampling.NEAREST).save(ROOT/'prueba-vertical.png')
def main():
 sheet(M['characters'],'12-clientes-cuadricula.png')
 sheet(M['characters'][:6],'clientes-01-06-detalle.png',3)
 sheet(M['characters'][6:],'clientes-07-12-detalle.png',3)
 sheet(M['characters'],'clientes-tamano-juego.png',4,True)
 context()
 atlas=Image.new('RGBA',(64*4,80*3))
 for i,p in enumerate(M['characters']):atlas.paste(sprite(p),((i%4)*64,(i//4)*80))
 atlas.save(ROOT/'plantilla-64x80-transparente.png')
 with zipfile.ZipFile(ROOT/'12-clientes-adaptados.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in M['characters']:
   z.write(ROOT/p['file'],p['file']);z.write(ROOT/(p['id']+'.ts'),p['id']+'.ts')
  for f in ['manifest.json','sprite-definitions.json','engine-checks.json','plantilla-64x80-transparente.png','12-clientes-cuadricula.png','customers.ts','README.md']:
   if (ROOT/f).exists():z.write(ROOT/f,f)
if __name__=='__main__':main()
