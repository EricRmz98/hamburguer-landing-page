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
