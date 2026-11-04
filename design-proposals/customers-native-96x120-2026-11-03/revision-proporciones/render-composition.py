"""Assemble review pages from actual full browser captures and recorded stage bounds."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, math

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'revision-proporciones/composicion'
people=json.loads((ROOT/'manifest.json').read_text())['characters']
checks=json.loads((OUT/'browser-checks.json').read_text())
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
for c in checks:
    mode=c['layout']; n=c['index']+1; b=c['clip']
    im=Image.open(OUT/f'{mode}-full-{n:02}.png')
    x=math.floor(b['x']+.5); y=math.floor(b['y']+.5)
    assert x>=0 and y>=0 and x+b['width']<=im.width and y+b['height']<=im.height
    im.crop((x,y,x+b['width'],y+b['height'])).save(OUT/f'{mode}-{n:02}.png')
for mode,w,h,cols in [('horizontal',640,400,3),('vertical',360,560,4)]:
    pad=20; label=36
    sheet=Image.new('RGB',(cols*(w+pad)+pad,(12//cols)*(h+label+pad)+pad),'#0a0a0a')
    d=ImageDraw.Draw(sheet)
    for i,c in enumerate(people):
        x=pad+(i%cols)*(w+pad); y=pad+(i//cols)*(h+label+pad)
        d.text((x,y),f'{i+1:02} · {c["name"]}',font=font,fill='white')
        sheet.paste(Image.open(OUT/f'{mode}-{i+1:02}.png').convert('RGB'),(x,y+label))
    sheet.save(OUT/f'12-clientes-{mode}.jpg',quality=94)
comparison=Image.new('RGB',(1312,460),'#0a0a0a');d=ImageDraw.Draw(comparison)
d.text((12,12),'Inés · Antes',font=font,fill='white')
d.text((668,12),'Inés · Ahora: menor estatura y escala facial',font=font,fill='white')
comparison.paste(Image.open(ROOT/'composicion/horizontal-10.png').convert('RGB'),(12,48))
comparison.paste(Image.open(OUT/'horizontal-10.png').convert('RGB'),(668,48))
comparison.save(OUT/'ines-antes-despues.png')
