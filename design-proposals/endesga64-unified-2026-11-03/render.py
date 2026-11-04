"""Rasterize the actual code-native assets and assemble the actual browser captures."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'native-assets.json').read_text());P=DATA['palette'];S={s['key']:s for s in DATA['sprites']}
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def label(im,xy,text,size=20,color='white'):
    ImageDraw.Draw(im).text(xy,text,font=ImageFont.truetype(FONT,size),fill=color)
def sprite(key):
    s=S[key];im=Image.new('RGBA',(s['width'],s['height']))
    for y,row in enumerate(s['frames'][0]):
        for x,c in enumerate(row):
            if c!='.':im.putpixel((x,y),tuple(bytes.fromhex(P[s['colors'][c]][1:]))+(255,))
    return im
# Fully assembled native portraits, with the production colors and poses.
sheet=Image.new('RGB',(1280,1312),'#2a2f4e')
label(sheet,(20,14),'CLIENTES / ENDESGA 64',32)
label(sheet,(20,58),'Misma cuadrícula · proporciones aprobadas · perfiles alternados',20,'#c7cfdd')
for i,p in enumerate(DATA['customers']):
    x=16+(i%4)*316;y=100+(i//4)*400
    ImageDraw.Draw(sheet).rectangle((x,y,x+303,y+392),fill=P['gris-claro'])
    label(sheet,(x+8,y+6),p['name'],23,P['negro']);im=sprite(p['key']).resize((288,360),Image.Resampling.NEAREST)
    sheet.paste(im,(x+8,y+28),im)
sheet.save(ROOT/'12-clientes-endesga.png')
keys=['pan_base','pan_tapa','carne:cruda','carne:cocinandose','carne:perfecta','carne:quemada','queso','lechuga','tomate','cebolla','salsa:catsup','salsa:mostaza','salsa:mayonesa','plato','charola','bote:catsup','bote:mostaza','bote:mayonesa','bandeja_pan','bandeja_queso','bandeja_lechuga','bandeja_tomate','bandeja_cebolla','basura']
sheet=Image.new('RGB',(1200,1050),P['noche']);label(sheet,(20,14),'COCINA / MATERIALES Y ESTADOS',30)
for i,key in enumerate(keys):
    x=12+(i%6)*198;y=70+(i//6)*240
    label(sheet,(x,y),key.replace('bandeja_','').replace('carne:','carne / '),15)
    ImageDraw.Draw(sheet).rectangle((x,y+28,x+183,y+222),fill=P['gris-claro'])
    im=sprite(key);im=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)
    sheet.paste(im,(x+(184-im.width)//2,y+34+(180-im.height)//2),im)
sheet.save(ROOT/'cocina-detalle.png')
for key in ['comedor','comedor_v','barra_roja','barra_roja_v','plancha','plancha_v']:
    im=sprite(key);im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST).save(ROOT/(key+'.png'))
checks=json.loads((ROOT/'composicion/browser-checks.json').read_text())
for c in checks:
    b=c['clip'];n=c['index']+1;mode=c['layout']
    im=Image.open(ROOT/f'composicion/{mode}-full-{n:02}.png');x=math.floor(b['x']+.5);y=math.floor(b['y']+.5)
    assert x>=0 and y>=0 and x+b['width']<=im.width and y+b['height']<=im.height
    im.crop((x,y,x+b['width'],y+b['height'])).save(ROOT/f'composicion/{mode}-{n:02}.png')
for mode,w,h,cols in [('horizontal',640,400,3),('vertical',360,560,4)]:
    out=Image.new('RGB',(cols*(w+20)+20,(12//cols)*(h+56)+20),'#0a0a0a')
    for i,p in enumerate(DATA['customers']):
        x=20+(i%cols)*(w+20);y=20+(i//cols)*(h+56)
        label(out,(x,y),f'{i+1:02} · {p["name"]}')
        out.paste(Image.open(ROOT/f'composicion/{mode}-{i+1:02}.png').convert('RGB'),(x,y+36))
    out.save(ROOT/f'composicion/12-clientes-{mode}.jpg',quality=94)
out=Image.new('RGB',(1048,630),'#0a0a0a')
label(out,(16,12),'Endesga 64 · Horizontal');label(out,(680,12),'Endesga 64 · Vertical')
out.paste(Image.open(ROOT/'composicion/horizontal-01.png').convert('RGB'),(16,50));out.paste(Image.open(ROOT/'composicion/vertical-01.png').convert('RGB'),(680,50))
out.save(ROOT/'composicion-final.png')
out=Image.new('RGB',(1312,460),'#0a0a0a');label(out,(12,12),'Antes · Resurrect 64');label(out,(668,12),'Ahora · Endesga 64 / acabado común')
out.paste(Image.open(ROOT.parent/'resurrect-style-2026-11-03/composicion/horizontal-01.png').convert('RGB'),(12,48));out.paste(Image.open(ROOT/'composicion/horizontal-01.png').convert('RGB'),(668,48));out.save(ROOT/'antes-despues.png')
print('Native art sheets and both full browser compositions rendered.')
