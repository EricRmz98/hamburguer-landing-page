import math, json, sys
import r34
from r34 import Model, render, shade, crop, anchor, hashp, project, dot

PAN = ('o', 's', 'b', 'l')

def local_texture(texture, origin):
    return lambda cell,n,L: texture(tuple(v-o for v,o in zip(cell,origin)),n,L)

def wav(r, amp, k, ph=0):
    return lambda y, a: r + amp * math.sin(k * a + ph)

def tex_pan(cell, n, L):
    o, s, b, l = L
    x,y,z=cell
    # Open crumb, with pores clustered around small islands rather than uniform stippling.
    h=hashp(x//2,y//2,z//2,1)
    if n[1] == 1:
        if x*x+z*z>95:return b
        if h<120:return b
        if h<300:return 'a'
        return l if x+z<3 else 'a'
    return s if h<240 or y==0 else b

def tex_tapa(cell, n, L):
    o, s, b, l = L
    x, y, z = cell
    h=hashp(x//2,y//2,z//2,2)
    if n[1] == 1:
        # Broad warm light on the dome, caramel shoulders and a darker baked skirt.
        if y<3:return s if h<420 else b
        if x>4 or z>7:return b if h<600 else 'p'
        if x<-2 and z<3:return 'a' if h<230 else l
        if h<190:return b
        return 'p'
    if y<=2:return o if h<180 else s
    return b if x<2 else s

def tex_carne(cell, n, L):
    o, s, b, l = L
    x,y,z=cell
    h = hashp(x//2,y//2,z//2,3)
    if n[1] == 1:
        # Broken sear lines follow one direction; the fat glints stay on the lit half.
        if (x+2*z)%8 in (0,1) and abs(z)<9:return s if h<750 else b
        if h<200:return b
        if h>790 and x<3:return 'h'
        return l if x+z<4 else b
    return s if h<450 or y==0 else b

def tex_queso(cell,n,L):
    o,s,b,l=L;x,y,z=cell
    if n[1]==1:
        # Supple slice: soft folds, pinprick pores and a thin translucent lit edge.
        if x<-6 or z<-7:return l
        if x>5 and z>0:return s
        if hashp(x//2,0,z//2,71)<110:return 'j'
        return b
    return s if x<0 else o

def tex_lechuga(cell, n, L):
    o, s, b, l = L
    x,y,z=cell
    if n[1]==1:
        # Main rib and branching veins, separated by broad folded leaf surfaces.
        rib=x+z//3
        if abs(rib)<=1:return 'V' if x<-1 and z<1 else l if x<1 and z<2 else b
        if (z-abs(rib))%6==0 and abs(rib)<10:return l if x<1 and z<2 else b
        fold=math.sin((x+2*z)*.55)
        if fold<-.6:return s if x>3 else b
        return l if fold>.35 and x<0 and z<3 else b
    return s if x>0 else b

def tex_tomate(cell, n, L):
    o, s, b, l = L
    x, y, z = cell
    d = math.hypot(x + .5, z + .5) * 14 / SLICE_R  # el dibujo se pensó para radio 14
    if n[1] == 1:
        angle=math.atan2(z+.5,x+.5)
        chamber=math.sin(angle*4+.6)
        if d>12:return b if x<0 else 'a'
        if d<2:return 'P'
        if 4<d<9 and chamber>.73:return 'B' if hashp(x,0,z,7)<650 else 'P'
        if 4<d<10 and chamber>.1:return 'a'
        return l if x+z<0 else b
    return None

def tex_cebolla(cell, n, L):
    o, s, b, l = L
    x, y, z = cell
    d = math.hypot(x + .5, z + .5) * 14 / SLICE_R
    if n[1]==1:
        if 4.6<=d<6 or 9<=d<10.4:return s if x<2 else o
        if 6<=d<7.3 or d>11.5:return 'i'
        return l if z<-2 and x<2 else 'j'
    return b

def tex_salsa(cell,n,L):
    o,s,b,l=L;x,y,z=cell
    if n[1]==1:
        # A viscous pool has a soft dark edge and two connected specular highlights.
        d=math.hypot(x+1,z+1)
        if d>7.2:return b if x<0 else s
        if (x+3)**2+(z+2)**2<5:return 'O'
        if x<-1 and z<3:return l
        return b

def tex_bolsa(cell, n, L):
    o, s, b, l = L
    return 'P' if n[1] == 1 and hashp(*cell, 32) < 160 else None  # brillos del plástico

def tex_basura(cell, n, L):
    o, s, b, l = L
    return s if n[1] != 1 and cell[0] % 4 == 0 else None


# Escala de los ingredientes: la misma que en las bandejas (el pan mide 24 de ancho).
BUN_R, PATTY_R, SLICE_R, LEAF_R, CHEESE, SAUCE_R, PLATE_R = 12, 12.5, 10.5, 13, 10, 9, 15

def plancha(m, width, knobs, depth=36):
    m.box(0, width, -10, 0, depth - 2, depth, 'acero')               # panel frontal
    m.box(0, width, 0, 2, 2, depth, 'plancha')                       # placa de acero curtido
    m.box(0, width, 1, 2, depth - 4, depth - 2, 'canal')             # canal de grasa al frente
    m.box(0, width, 0, 8, 0, 2, 'acero')                             # salpicadera
    m.box(0, 2, 2, 4, 2, depth, 'acero'); m.box(width - 2, width, 2, 4, 2, depth, 'acero')  # rieles
    for kx in knobs:                                                 # una perilla por lugar
        m.box(kx - 2, kx + 2, -8, -3, depth, depth + 2, 'perilla')
        m.put(kx, -4, depth + 2, 'perilla_luz')

def rounded(x, z, x0, x1, z0, z1, r):
    """¿La celda (x, z) cae dentro de un rectángulo con esquinas redondeadas de radio r?"""
    cx = min(max(x + .5, x0 + r), x1 - r)
    cz = min(max(z + .5, z0 + r), z1 - r)
    return x0 <= x + .5 <= x1 and z0 <= z + .5 <= z1 and (x + .5 - cx) ** 2 + (z + .5 - cz) ** 2 <= r * r

PAN_W, PAN_D, PAN_H = 32, 22, 14  # frente de 9 filas: cinta de 7 con margen arriba y abajo

def bandeja(m, fill, W=PAN_W, D=PAN_D):
    """Bandeja gastronorm: esquinas redondeadas, costados que se angostan abajo y orilla ancha arriba."""
    H = PAN_H
    for y in range(0, H):
        inset = 1 if y < 2 else 0
        x0, x1, z0, z1 = inset, W - inset, inset, D - inset
        for x in range(-1, W + 1):
            for z in range(-1, D + 1):
                outer = rounded(x, z, x0, x1, z0, z1, 2.5)
                inner = rounded(x, z, x0 + 1, x1 - 1, z0 + 1, z1 - 1, 1.5)
                if outer and (y == 0 or not inner):
                    m.put(x, y, z, 'bandeja')
    for x in range(-2, W + 2):  # orilla ancha alrededor
        for z in range(-2, D + 2):
            if rounded(x, z, -1.5, W + 1.5, -1.5, D + 1.5, 3) and not rounded(x, z, 1, W - 1, 1, D - 1, 1.5):
                m.put(x, H, z, 'orilla')
    walls = {k: v for k, v in m.v.items()}
    contents[fill](m, W, D)
    for (x, y, z) in [k for k in m.v if k not in walls and k[1] < H and not rounded(k[0], k[2], 1, W - 1, 1, D - 1, 1.5)]:
        del m.v[(x, y, z)]  # debajo de la orilla, el contenido queda dentro de las paredes
    m.v.update(walls)  # y nunca se come las paredes

RIM = PAN_H  # altura de la orilla

def _pan(m, W=PAN_W, D=PAN_D):
    """Pila ordenada de bollos del tamaño del de la hamburguesa: se ven las orillas de los de abajo y el
    domo con ajonjolí del de arriba."""
    cx, cz, r = W / 2, D / 2, BUN_R
    for k in range(3):
        y = RIM - 1 + 2 * k
        mat = ('bollo_a', 'bollo_b', 'bollo')[k]
        m.disc(r - (k % 2) * 0.4, y, y + 2, mat, cx=cx + (k % 2) * 0.5, cz=cz)
        if k == 2:
            m.dome(r, y + 2, 6, mat, cx=cx, cz=cz)
    for sx, sz in [(-6, -2), (-2, -6), (3, -4), (7, 1), (-4, 3), (1, 1), (5, 5), (-8, 6), (-9, -1), (8, -5), (-3, -9)]:
        x, z = int(cx + sx), int(cz + sz)
        top = m.top_at(x, z)
        if top is not None and m.v.get((x, top, z)) == 'bollo':
            m.put(x, top + 1, z, 'semilla')

def _queso(m, W=PAN_W, D=PAN_D):
    """Pila ordenada de rebanadas cuadradas, como en la salchichonería: cada una apenas movida, para
    que se vean las orillas de todas."""
    cx, cz, ang = W / 2, D / 2, 0.22
    c, sn = math.cos(ang), math.sin(ang)
    for s in range(7):
        dx, dz = (0, 1, 0, -1, 0, 1, 0)[s], (0, 0, 1, 0, 0, 1, 0)[s]
        mat = 'queso' if s == 6 else ('queso_a' if s % 2 == 0 else 'queso_b')
        for x in range(-4, W + 4):
            for z in range(-4, D + 4):
                u, v = (x + .5 - cx - dx) * c - (z + .5 - cz - dz) * sn, (x + .5 - cx - dx) * sn + (z + .5 - cz - dz) * c
                if abs(u) <= 10 and abs(v) <= 10:
                    m.put(x, RIM - 1 + s, z, mat)

def _carne_cruda(m, W, D):
    """Carne molida cruda, sin forma: un montón con grumos que llena la bandeja y sobresale al centro."""
    cx, cz = W / 2, D / 2
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            if not rounded(x, z, 1, W - 1, 1, D - 1, 1.5):
                continue
            u, v = (x + .5 - cx) / (W / 2), (z + .5 - cz) / (D / 2)
            mound = 5 * max(0, 1 - u * u * 0.8 - v * v * 0.9)            # loma al centro
            lumps = (hashp(x // 3, 0, z // 3, 41) % 3) + (hashp(x // 2, 1, z // 2, 42) % 2) * 0.5  # grumos
            for y in range(1, int(RIM - 1 + mound + lumps)):
                m.put(x, y, z, 'molida')

contents = {
    'carne': _carne_cruda,
    'pan': _pan,
    'queso': _queso,
    'vacia': lambda m, W, D: None,
}

def tex_molida(cell, n, L):
    """Hebras de carne molida: rayitas cortas oscuras y claras, con grasa del lado de la luz."""
    o, s, b, l = L
    x, y, z = cell
    if n[1] != 1:
        return None
    h = hashp(x, y, z, 43)
    worm = (x + 2 * z + hashp(x // 2, 0, z, 44) % 3) % 4  # hebras inclinadas
    if worm == 0:
        return s               # surco entre hebras
    if worm == 1 and h < 450 and x < 24:
        return 'h' if h < 60 else l  # brillo y grasa de las hebras, del lado de la luz
    return b

def tex_bandeja(cell, n, L):
    o, s, b, l = L
    x,y,z=cell
    if n[2]==1:
        if y>=PAN_H-2:return 'W' if 3<x<12 else l
        if x>27:return 'Z'
        if x<3:return s
        if 5<x<10:return l if y>6 else b
        if y==2:return b if x<20 else s
        if y>7 and (x+2*y)%19<4:return l
        return b if x<21 else s
    if n[0]==1:return s
    if n[1]==1:
        if z%7==1 and x<24:return l
        return b
    return None

def tex_plato(cell,n,L):
    o,s,b,l=L;x,y,z=cell;d=math.hypot(x+.5,z+.5)
    if n[1]==1 and 10<d<12.5:return b if x>0 else l
    if n[1]==1 and d<10 and x>5:return b
    return None

def tex_bote(cell,n,L):
    o,s,b,l=L;x,y,z=cell
    if n[1]==1 and x<-1:return l
    if n[2]==1 and x<-2 and 2<y<21:return l
    if n[2]==1 and x>3:return s
    return None

def build(name, frame=0):
    m = Model()
    if name == 'pan_base':
        m.disc(lambda y, a: BUN_R - 1 if y == 0 else BUN_R, 0, 4, 'pan')
    elif name == 'pan_medio':
        m.disc(lambda y, a: BUN_R - 0.5 if y != 1 else BUN_R, 0, 3, 'pan')
    elif name == 'pan_tapa':
        m.disc(BUN_R, 0, 2, 'tapa')
        m.dome(BUN_R, 2, 6, 'tapa')
        for (sx, sz) in [(-5, -2), (-2, -6), (3, -4), (6, 1), (-4, 3), (1, 1), (5, 5), (-7, 6), (-8, -1), (7, -5), (-3, -8)]:
            top = m.top_at(sx, sz)
            if top is not None:
                m.put(sx, top, sz, 'semilla')
    elif name == 'carne':
        m.disc(wav(PATTY_R, 0.5, 5), 0, 4, 'carne')
    elif name == 'queso':
        m.box(-CHEESE, CHEESE, 0, 1, -CHEESE, CHEESE, 'queso')
        for cx in (-CHEESE, CHEESE - 2):
            for cz in (-CHEESE, CHEESE - 2):
                m.box(cx, cx + 2, -2, 0, cz, cz + 2, 'queso')  # esquinas que cuelgan
    elif name == 'lechuga':
        m.disc(wav(LEAF_R, 1.2, 7), 0, 1, 'lechuga')
        m.disc(wav(LEAF_R, 1.2, 7), 1, 2, 'lechuga', keep=lambda dx, y, dz: math.hypot(dx, dz) > LEAF_R - 3.5 and math.sin(7 * math.atan2(dz, dx)) > 0.2)
    elif name == 'tomate':
        m.disc(SLICE_R, 0, 2, 'tomate')
    elif name == 'cebolla':
        m.disc(SLICE_R, 0, 1, 'cebolla')
    elif name == 'salsa':
        m.disc(wav(SAUCE_R, 1.4, 5, 1), 0, 1, 'salsa')
        for a in (0.7, 1.4, 2.2):
            x, z = round((SAUCE_R + 0.5) * math.cos(a)), round((SAUCE_R + 0.5) * math.sin(a))
            m.box(x, x + 1, -2, 0, z, z + 1, 'salsa')
    elif name == 'plato':
        m.disc(PLATE_R, 0, 1, 'plato')
        m.disc(PLATE_R, 1, 2, 'plato', keep=lambda dx, y, dz: math.hypot(dx, dz) >= PLATE_R - 2.5)
    elif name == 'bote':
        squeeze = frame == 1
        m.disc(lambda y, a: 6 if squeeze and 6 <= y < 19 else 7, 0, 22, 'salsa')
        m.disc(lambda y, a: 6.05 if squeeze and 6 <= y < 19 else 7.05, 8, 15, 'etiqueta')
        m.disc(lambda y, a: 7 - (y - 22) * 0.75, 22, 26, 'salsa')
        m.disc(4, 26, 29, 'tapa')
        m.disc(lambda y, a: max(0.8, 2 - (y - 29) * 0.3), 29, 34, 'tapa')
        if squeeze:
            m.put(0, 35, 0, 'salsa'); m.put(0, 36, 0, 'salsa')
    elif name == 'plancha':
        PLANCHA['slots'] = [21 + 38 * i for i in range(4)]
        plancha(m, 156, PLANCHA['slots'])
    elif name == 'plancha_v':
        PLANCHA['slots'] = [18 + 33 * i for i in range(4)]
        plancha(m, 134, PLANCHA['slots'])
    elif name == 'charola':  # bandeja más ancha y rectangular con carne cruda
        bandeja(m, 'carne', W=38, D=PAN_D)
    elif name.startswith('bandeja_'):
        fill = name.split('_', 1)[1]
        bandeja(m, fill if fill in contents else 'vacia')
    elif name == 'basura':
        W, D = 32, 24
        for x in range(W):
            for z in range(D):
                ring = not (3 <= x < W - 3 and 3 <= z < D - 3)
                if ring:
                    m.put(x, 0, z, 'aro')              # aro de acero al ras de la barra
                elif not (4 <= x < W - 4 and 4 <= z < D - 4):
                    m.put(x, 0, z, 'bolsa')            # bolsa doblada sobre la orilla
                    if hashp(x, 0, z, 31) < 300:
                        m.put(x, 1, z, 'bolsa')        # pliegues
                else:
                    m.put(x, -8, z, 'fondo')           # fondo del bote, en sombra
        for y in range(-8, 0):                         # paredes interiores forradas con la bolsa
            for x in range(4, W - 4):
                m.put(x, y, 4, 'bolsa')
            for z in range(4, D - 4):
                m.put(4, y, z, 'bolsa'); m.put(W - 5, y, z, 'bolsa')
    return m

# Materiales: letras (contorno, sombra, base, luz) de cada sprite.
SPEC = {
    'pan_base':  ({'pan': PAN}, {'o': 'oxido', 's': 'canela', 'b': 'piel', 'l': 'crema', 'a': 'piel-clara'}, ['pan'], {'pan': tex_pan}),
    'pan_medio': ({'pan': PAN}, {'o': 'oxido', 's': 'canela', 'b': 'piel', 'l': 'crema', 'a': 'piel-clara'}, ['pan'], {'pan': tex_pan}),
    'pan_tapa':  ({'tapa': ('o', 's', 'b', 'l'), 'semilla': ('e', 'e', 'e', 'e')},
                  {'o': 'oxido', 's': 'canela', 'b': 'piel', 'l': 'tostado', 'e': 'crema', 'p': 'tostado', 'a': 'piel-clara'}, ['pan'], {'tapa': tex_tapa}),
    'carne':     ({'carne': ('k', 'm', 'n', 'p')}, {'k': 'negro', 'm': 'cafe-oscuro', 'n': 'cafe', 'p': 'canela', 'h': 'piel'}, ['carne'], {'carne': tex_carne}),
    'queso':     ({'queso': ('q', 'r', 't', 'u')}, {'q': 'canela', 'r': 'ambar', 't': 'amarillo', 'u': 'vainilla', 'j': 'tostado'}, ['queso'], {'queso': tex_queso}),
    'lechuga':   ({'lechuga': ('v', 'w', 'x', 'y')}, {'v': 'verde-noche', 'w': 'verde-oscuro', 'x': 'verde-claro', 'y': 'lima', 'V': 'pistacho'}, ['lechuga'], {'lechuga': tex_lechuga}),
    'tomate':    ({'tomate': ('A', 'A', 'C', 'D')}, {'A': 'rojo-oscuro', 'C': 'rojo', 'D': 'coral', 'B': 'tostado', 'a': 'rojo-ladrillo', 'P': 'piel-clara'}, ['tomate'], {'tomate': tex_tomate}),
    'cebolla':   ({'cebolla': ('E', 'F', 'G', 'H')}, {'E': 'ciruela', 'F': 'magenta', 'G': 'gris-claro', 'H': 'blanco', 'i': 'rosa-palido', 'j': 'gris-claro'}, ['cebolla'], {'cebolla': tex_cebolla}),
    'salsa':     ({'salsa': ('I', 'J', 'K', 'L')}, {'I': 'cafe-oscuro', 'J': 'rojo-oscuro', 'K': 'rojo-ladrillo', 'L': 'rojo', 'O': 'coral'}, ['catsup'], {'salsa': tex_salsa}),
    'plato':     ({'plato': ('E', 'F', 'G', 'H')}, {'E': 'gris-azul', 'F': 'gris', 'G': 'gris-claro', 'H': 'blanco'}, ['ceramica'], {'plato': tex_plato}),
    'bote':      ({'salsa': ('I', 'J', 'K', 'L'), 'etiqueta': ('R', 'R', 'S', 'S'), 'tapa': ('M', 'N', 'P', 'Q')},
                  {'I': 'cafe-oscuro', 'J': 'rojo-oscuro', 'K': 'rojo', 'L': 'rosa', 'R': 'gris-claro', 'S': 'blanco', 'M': 'negro', 'N': 'pizarra', 'P': 'gris', 'Q': 'gris-claro'},
                  ['catsup', 'etiqueta', 'metal'], {'salsa': tex_bote}),
    'charola':   ({'charola': ('M', 'N', 'P', 'Q'), 'fondo': ('M', 'N', 'N', 'P'), 'cruda': ('k', 'm', 'n', 'p'), 'cruda_b': ('k', 'm', 'n', 'p')},
                  {'M': 'negro', 'N': 'noche', 'P': 'pizarra', 'Q': 'gris-azul', 'k': 'rojo-oscuro', 'm': 'rosa-viejo', 'n': 'rosa', 'p': 'piel-clara'},
                  ['metal', 'carne-cruda'], None),
    'basura':    ({'aro': ('K', 'R', 'S', 'U'), 'bolsa': ('M', 'M', 'N', 'P'), 'fondo': ('M', 'M', 'M', 'M')},
                  {'K': 'negro', 'R': 'gris-azul', 'S': 'gris', 'U': 'gris-claro', 'M': 'negro', 'N': 'noche', 'P': 'pizarra'},
                  ['metal'], {'bolsa': tex_bolsa}),
}


STEEL = {'R': 'gris-azul', 'S': 'gris', 'T': 'gris', 'U': 'gris-claro', 'K': 'negro'}

PLANCHA = {'slots': [], 'cz': 17}  # centros de los lugares; los pone `build` al armar la plancha

def tex_plancha(cell, n, L):
    """Placa curtida: donde van las carnes, la grasa requemada la deja casi negra; hacia las orillas,
    y entre lugar y lugar, el acero queda más claro con vetas de brillo. Transiciones con tramado."""
    o, s, b, l = L
    x, y, z = cell
    if n[1] != 1:
        return None
    d = min(math.hypot((x + .5 - sx) / 19, (z + .5 - PLANCHA['cz']) / 13) for sx in PLANCHA['slots'])
    d += (hashp(x // 3, 0, z // 3, 14) - 500) / 7000  # orillas irregulares de la mancha
    if d < 0.45:
        return s if hashp(x//3,0,z//2,61)<120 else 'M'
    if d < 0.85:
        return s                                             # halo de grasa
    if d < 0.97:
        return b
    if hashp(0, 0, z, 11) % 6 == 0 and hashp(x // 7, 0, z, 12) < 400:
        return 'Q'  # vetas de brillo del acero limpio
    return None

def tex_acero(cell, n, L):
    o, s, b, l = L
    x,y,z=cell
    if n[2]==1:
        if y==-1:return 'W' if x%38<20 else l
        if y==-2:return s
        if x%38 in (4,5,6):return l
        if x%38>29:return s
        return l if y==-8 and x%7<4 else b
    if n[1]==1 and z<2:return l if x%38<22 else b
    return None

SPEC.update({
    'plancha': ({'plancha': ('M', 'N', 'N', 'P'), 'acero': ('K', 'R', 'S', 'U'), 'canal': ('M', 'M', 'M', 'N'),
                 'perilla': ('M', 'M', 'N', 'P'), 'perilla_luz': ('U', 'U', 'U', 'U')},
                {'M': 'negro', 'N': 'noche', 'P': 'pizarra', 'Q': 'gris-azul', 'K': 'negro', 'R': 'gris-azul', 'S': 'gris', 'U': 'gris-claro', 'W': 'blanco'},
                ['metal'], {'plancha': tex_plancha, 'acero': tex_acero}),
})
SPEC['plancha_v'] = SPEC['plancha']
STEEL_PAN = {'bandeja': ('K', 'R', 'S', 'U'), 'orilla': ('R', 'S', 'U', 'U')}
STEEL_COLORS = {'K': 'negro', 'R': 'gris-azul', 'S': 'gris', 'U': 'gris-claro', 'W': 'blanco', 'Z': 'pizarra'}
BANDEJAS = ['bandeja_pan', 'bandeja_queso', 'bandeja_lechuga', 'bandeja_tomate', 'bandeja_cebolla']
for name in BANDEJAS:
    SPEC[name] = (STEEL_PAN, STEEL_COLORS, ['metal'], {'bandeja': tex_bandeja})
# Pan y queso van en pilas ordenadas modeladas en 3D (la variante que mejor se lee a este tamaño).
SPEC['bandeja_pan'] = ({**STEEL_PAN, 'bollo': ('o', 's', 'b', 'l'), 'bollo_a': ('o', 's', 'b', 'l'), 'bollo_b': ('o', 's', 'b', 'l'), 'semilla': ('e', 'e', 'e', 'e')},
                       {**STEEL_COLORS, 'o': 'oxido', 's': 'canela', 'b': 'piel', 'l': 'tostado', 'e': 'crema', 'p': 'tostado', 'a': 'piel-clara'}, ['metal', 'pan'], {'bandeja': tex_bandeja, 'bollo': local_texture(tex_tapa,(PAN_W//2,RIM+3,PAN_D//2)), 'bollo_a': local_texture(tex_pan,(PAN_W//2,0,PAN_D//2)), 'bollo_b': local_texture(tex_pan,(PAN_W//2,0,PAN_D//2))})
SPEC['bandeja_queso'] = ({**STEEL_PAN, 'queso': ('q', 'r', 't', 'u'), 'queso_a': ('q', 'r', 't', 'u'), 'queso_b': ('q', 'r', 't', 'u')},
                         {**STEEL_COLORS, 'q': 'canela', 'r': 'ambar', 't': 'amarillo', 'u': 'vainilla', 'j': 'tostado'}, ['metal', 'queso'], {'bandeja': tex_bandeja, 'queso': local_texture(tex_queso,(PAN_W//2,0,PAN_D//2)), 'queso_a': local_texture(tex_queso,(PAN_W//2,0,PAN_D//2)), 'queso_b': local_texture(tex_queso,(PAN_W//2,0,PAN_D//2))})
SPEC['charola'] = ({**STEEL_PAN, 'molida': ('k', 'm', 'n', 'p')},
                   {**STEEL_COLORS, 'k': 'rojo-oscuro', 'm': 'rosa-viejo', 'n': 'rosa', 'p': 'piel-clara', 'h': 'blanco'},
                   ['metal', 'carne-cruda'], {'bandeja': tex_bandeja, 'molida': tex_molida})
CAMERA = {name: 0 for name in SPEC if name.startswith('plancha') or name.startswith('bandeja_') or name in ('basura', 'charola')}

def native_bottle():
    """Hand-placed 2D cells, with a soft body and paper label; same size/anchor as the kitchen."""
    frames=[]
    for squeeze in [False,True]:
        g=[['.']*14 for _ in range(35)]
        def span(y,l,r,c):
            for x in range(l,r+1):g[y][x]=c
        for y in range(7,35):
            inset=3 if y in (7,34) else 2 if y in (8,33) else 1
            if squeeze and 14<=y<=27:inset=2
            span(y,inset,13-inset,'I')
            if y<34:
                span(y,inset+1,12-inset,'K')
                if y>8:g[y][12-inset]='J'
                if 10<y<32:g[y][inset+1]='L'
                if 11<y<32 and y not in range(17,26):g[y][inset+2]='K'
        for y in range(4,8):
            span(y,4,10,'I');span(y,5,9,'K');g[y][5]='L'
        for y in range(17,26):
            left=2 if not squeeze else 3;right=11 if not squeeze else 10
            span(y,left,right,'R' if y==25 else 'S')
            g[y][right]='R'
        span(20,5,8,'J');span(22,5,8,'K')
        span(3,4,10,'M');span(4,4,10,'N');span(5,4,10,'M')
        span(3,5,9,'Q');span(4,5,9,'P')
        for y in range(3):
            span(y,6,8,'M');g[y][6]='P'
        frames.append([''.join(row) for row in g])
    return {'size':[14,35],'anchor':[7,31],'frames':frames,'materials':['catsup','etiqueta','metal'],
        'colors':{'I':'rojo-oscuro','J':'carmesi','K':'rojo','L':'coral','R':'gris-claro','S':'blanco','M':'negro','N':'noche','P':'gris','Q':'gris-claro'}}

def generate(name):
    if name=='bote':return native_bottle()
    palette, colors, materials, texture = SPEC[name]
    r34.set_camera(yaw_deg=CAMERA.get(name, 12))
    frames = 2 if name == 'bote' else 1
    models = [build(name, f) for f in range(frames)]

    # mismos límites para todos los cuadros
    pts = [(x + dx, y + dy, z + dz) for mm in models for (x, y, z) in mm.v for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
    us = [dot(p, r34.RIGHT) for p in pts]; vs = [dot(p, r34.UP) for p in pts]
    bounds = (math.floor(min(us)), math.ceil(max(us)), math.floor(min(vs)), math.ceil(max(vs)))
    shaded, cells = [], []
    for mm in models:
        mat, face, cellat, _ = render(mm, bounds)
        shaded.append(shade(mat, face, cellat, palette, texture))
        cells.append(cellat)
    xs = [i for rows in shaded for r in rows for i, c in enumerate(r) if c != '.']
    ys = [j for rows in shaded for j, r in enumerate(rows) if r.strip('.')]
    bbox = (min(xs), max(xs) + 1, min(ys), max(ys) + 1)
    frames_rows = [crop(rows, bbox)[0] for rows in shaded]
    if name == 'basura':
        # La barra (que no se modela) tapa las paredes interiores: se corta en la orilla frontal del aro.
        last = max(j for j, r in enumerate(frames_rows[0]) if r.count('K') > len(r) * 0.8)
        frames_rows = [f[:last + 1] for f in frames_rows]
    base_y = 1 if name == 'plato' else 0
    ax, ay = anchor(bounds, bbox, (0, base_y, 0))
    used = {c for rows in frames_rows for r in rows for c in r} - {'.'}
    extra = {}
    if name.startswith('bandeja_'):
        x0, x1, y0, y1 = bbox
        extra['front'] = [''.join('1' if c and c[2] >= PAN_D - 1 else '0' for c in row[x0:x1]) for row in cells[0][y0:y1]]
        extra['rim'] = [round(v) for v in anchor(bounds, bbox, (PAN_W / 2, RIM + 1, PAN_D / 2))]
    return {**extra, 'frames': frames_rows, 'colors': {k: v for k, v in colors.items() if k in used}, 'materials': materials,
            'anchor': [round(ax), round(ay)], 'size': [len(frames_rows[0][0]), len(frames_rows[0])]}

# Lo que va en cada bandeja: los mismos sprites del plato, (sprite, dx, dy) desde el centro de la
# orilla, en orden de dibujo (de atrás hacia adelante).
FILL = {
    'bandeja_lechuga': [('lechuga', -5, 1), ('lechuga', 5, 2), ('lechuga', 0, 4)],
    'bandeja_tomate': [('tomate', -5, 1), ('tomate', 5, 3)],
    'bandeja_cebolla': [('cebolla', -5, 1), ('cebolla', 5, 3)],
}

def compose(pan, items, out):
    """Bandeja vacía + sprites del plato encima; el frente de la bandeja se vuelve a pintar al final."""
    PAD = 24
    w, h = pan['size']
    canvas = [['.'] * w for _ in range(h + PAD)]
    for j, row in enumerate(pan['frames'][0]):
        for i, c in enumerate(row):
            canvas[j + PAD][i] = c
    colors, materials = dict(pan['colors']), list(pan['materials'])
    rx, ry = pan['rim'][0], pan['rim'][1] + PAD
    for item, dx, dy in items:
        s = out[item]
        ax, ay = s['anchor']
        for j, row in enumerate(s['frames'][0]):
            for i, c in enumerate(row):
                x, y = rx + dx - ax + i, ry + dy - ay + j
                if c != '.' and 0 <= x < w and 0 <= y < h + PAD:
                    canvas[y][x] = c
        colors.update(s['colors'])
        materials += [m for m in s['materials'] if m not in materials]
    for j, row in enumerate(pan['front']):
        for i, f in enumerate(row):
            if f == '1':
                canvas[j + PAD][i] = pan['frames'][0][j][i]
    rows = [''.join(r) for r in canvas]
    top = next(j for j, r in enumerate(rows) if r.strip('.'))
    rows = rows[top:]
    used = {c for r in rows for c in r} - {'.'}
    return {'frames': [rows], 'colors': {k: v for k, v in colors.items() if k in used}, 'materials': materials,
            'anchor': [pan['anchor'][0], pan['anchor'][1] + PAD - top], 'size': [w, len(rows)]}

if __name__ == '__main__':
    out = {name: generate(name) for name in SPEC}
    for name, items in FILL.items():
        out[name] = compose(out[name], items, out)
    json.dump(out, open(sys.argv[1], 'w'))
    for name, d in out.items():
        print(f"{name:10s} {d['size'][0]}×{d['size'][1]} ancla {d['anchor']} cuadros {len(d['frames'])}")
    print('\n'.join(out['carne']['frames'][0]))
    print('\n'.join(out['pan_tapa']['frames'][0]))
