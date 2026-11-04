"""Review sheets and native export; never resizes a sprite for the game."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, zipfile
ROOT=Path(__file__).resolve().parent
M=json.loads((ROOT/'manifest.json').read_text())
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def sheet(people, filename, cols=4):
    cw,ch,gap,header=416,550,16,110
    out=Image.new('RGB',(cols*cw+(cols+1)*gap,header+((len(people)+cols-1)//cols)*(ch+gap)),'#262b44')
    d=ImageDraw.Draw(out)
    d.text((20,16),'CLIENTES / CUADRÍCULA NATIVA',font=ImageFont.truetype(FONT,36),fill='white')
    d.text((20,65),'96 × 120 · 1 píxel del cliente = 1 píxel del entorno · Endesga 32',font=ImageFont.truetype(FONT,24),fill='#c0cbdc')
    for i,p in enumerate(people):
        x=gap+(i%cols)*(cw+gap); y=header+(i//cols)*(ch+gap)
        d.rectangle((x,y,x+cw-1,y+ch-1),fill='#c0cbdc')
        d.text((x+12,y+10),f'{p["id"][:2]} · {p["name"]}',font=ImageFont.truetype(FONT,28),fill='#181425')
        im=Image.open(ROOT/p['file']).convert('RGBA').resize((384,480),Image.Resampling.NEAREST)
        out.paste(im,(x+16,y+58),im)
    out.save(ROOT/filename)
sheet(M['characters'],'12-clientes-nativos.png')
sheet(M['characters'][:6],'clientes-01-06-detalle.png',3)
sheet(M['characters'][6:],'clientes-07-12-detalle.png',3)
atlas=Image.new('RGBA',(96*4,120*3))
for i,p in enumerate(M['characters']): atlas.paste(Image.open(ROOT/p['file']),((i%4)*96,(i//4)*120))
atlas.save(ROOT/'plantilla-96x120-transparente.png')
with zipfile.ZipFile(ROOT/'12-clientes-nativos.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in M['characters']:
        z.write(ROOT/p['file'],p['file']);z.write(ROOT/(p['id']+'.ts'),p['id']+'.ts')
    for f in ['customers.ts','manifest.json','palette.json','sprite-definitions.json','engine-checks.json','plantilla-96x120-transparente.png','12-clientes-nativos.png','README.md','revision-proporciones/review-checks.json','revision-proporciones/composicion/browser-checks.json']:
        if (ROOT/f).exists():z.write(ROOT/f,f)
