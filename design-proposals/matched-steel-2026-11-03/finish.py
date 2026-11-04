from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
def label(im,xy,text):ImageDraw.Draw(im).text(xy,text,font=font,fill='white')
checks=json.loads((OUT/'composicion/browser-checks.json').read_text())
for c in checks:
 b=c['clip'];x=math.floor(b['x']+.5);y=math.floor(b['y']+.5);im=Image.open(OUT/f'composicion/{c["layout"]}-full.png')
 assert c['scale']==int(c['scale']) and c['groupCentered'] and c['sameHeight']
 assert x+b['width']<=im.width and y+b['height']<=im.height
 im.crop((x,y,x+b['width'],y+b['height'])).save(OUT/f'composicion/{c["layout"]}.png')
im=Image.new('RGB',(1048,670),'#0a0a0a');label(im,(16,12),'Acero del mismo estilo · Horizontal');label(im,(680,12),'Vertical')
im.paste(Image.open(OUT/'composicion/horizontal.png'),(16,50));im.paste(Image.open(OUT/'composicion/vertical.png'),(680,50));im.save(OUT/'composicion-final.png')
im=Image.new('RGB',(1312,490),'#0a0a0a');label(im,(12,12),'Antes');label(im,(668,12),'Ahora · alturas y márgenes equilibrados')
im.paste(Image.open(OUT.parent/'bright-steel-liner-2026-11-03/composicion/horizontal.png'),(12,48));im.paste(Image.open(OUT/'composicion/horizontal.png'),(668,48));im.save(OUT/'antes-despues.png')
