"""Draw the service counter directly on the game's native Endesga64 grid.
No image resampling: straight grout, layered red glaze, brushed steel and contact shadows.
Run before environment_gen.py. Requires Pillow.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import re,math

ROOT=Path(__file__).resolve().parents[2]
P={a or b:h for a,b,h in re.findall(r"(?:'([^']+)'|([\w-]+)):\s*'(#[0-9a-f]{6})'",(ROOT/'src/game/sprites/palette.ts').read_text())}

def brushed_steel(im,box):
    """Cool steel base and narrow reflected planes, matching the grill's front face."""
    x0,y0,w,h=box
    for y in range(h):
        for x in range(w):
            u=(x+y*.16)/max(1,w-1)
            reflection=sum(.08*math.exp(-((u-centre)/.025)**2) for centre in (.08,.42,.79))
            # Fine brushing only modulates reflected areas, leaving the steel body quiet.
            grain=(((x//7)*37+y*73)%17-8)*.00045 if reflection>.01 else 0
            light=reflection+grain
            tone='gris-claro' if light>.055 else 'plata' if light>.012 else 'gris'
            if y>=h-2:tone='gris-azul'
            im.putpixel((x0+x,y0+y),tuple(bytes.fromhex(P[tone][1:])))

def counter(w,h,depth):
    im=Image.new('RGB',(w,h),P['rojo-oscuro']);d=ImageDraw.Draw(im)
    def line(points,color):d.line(points,fill=P[color])
    def rect(box,color):d.rectangle(box,fill=P[color])
    # Orthogonal ceramic joints and broad, curved reflections inside each flat tile.
    for row,y in enumerate(range(depth,h-5,17)):
        for col,x in enumerate(range(0,w,32)):
            rect((x,y,x+31,min(y+16,h-3)),'cafe-oscuro')
            rect((x+1,y+1,x+30,min(y+15,h-4)),'rojo-oscuro')
            rect((x+2,y+2,x+29,min(y+13,h-4)),'carmesi')
            # Glaze pools darker at the lower edge; the upper left catches the ceiling light.
            line((x+2,y+1,x+29,y+1),'rojo-ladrillo')
            line((x+1,y+2,x+1,min(y+13,h-4)),'carmesi')
            if y+13<h-4:
                line((x+3,y+13,x+28,y+13),'rojo-oscuro')
                line((x+2,y+14,x+28,y+14),'carmesi')
            end=15+(col*7+row*3)%10
            for dy,start in [(2,3),(3,3),(4,4),(5,6)]:
                if y+dy<h-4:line((x+start,y+dy,x+end-dy,y+dy),'rojo-ladrillo')
            if (col+row*2)%3==0:
                line((x+4,y+2,x+9,y+2),'rojo')
                line((x+4,y+3,x+5,y+3),'rojo')
            # Sparse glaze flecks are connected two-cell strokes, never random noise.
            if y+10<h-4 and (col+row)%4==1:
                line((x+5,y+9,x+7,y+9),'rojo-ladrillo')
                line((x+8,y+10,x+10,y+10),'carmesi')
            if (col+2*row)%5==0 and y+12<h-4:
                line((x+24,y+10,x+25,y+10),'rojo-oscuro')
                line((x+25,y+11,x+27,y+11),'rojo-oscuro')
    # Working depth is composed natively for each layout, leaving air around the larger plate.
    brushed_steel(im,(0,0,w,depth-4))
    line((0,0,w-1,0),'gris-claro')
    line((0,depth-4,w-1,depth-4),'gris-claro')
    line((0,depth-3,w-1,depth-3),'gris-azul')
    line((0,depth-2,w-1,depth-2),'pizarra')
    line((0,depth-1,w-1,depth-1),'cafe-oscuro')
    rect((0,h-3,w-1,h-1),'noche')
    line((0,h-3,w-1,h-3),'carmesi')
    return im

if __name__=='__main__':
    for id,w,h,depth in [('barra_roja',320,90,28),('barra_roja_v',180,100,36)]:
        counter(w,h,depth).save(ROOT/'scripts/sprites/environment-native'/f'{id}.png')
    print('Two detailed native counter masters written.')
