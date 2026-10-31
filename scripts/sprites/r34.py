# Renderizador 3/4 con detalle para los sprites del juego.
# Cámara elevada 32° y girada 12°; tonos: luz (arriba), base (frente/izquierda), sombra (derecha y
# contacto abajo), contorno selectivo; texturas por material; limpieza de escalones.
import math

PITCH, YAW = math.radians(32), math.radians(12)

def norm(v):
    l = math.sqrt(sum(c * c for c in v)); return tuple(c / l for c in v)

def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def set_camera(pitch_deg=32, yaw_deg=12):
    """Cámara 3/4. Lo redondo usa el giro de 12°; lo rectangular que se alinea con la cuadrícula, 0°."""
    global F, RIGHT, UP
    pitch, yaw = math.radians(pitch_deg), math.radians(yaw_deg)
    F = norm((-math.sin(yaw) * math.cos(pitch), -math.sin(pitch), -math.cos(yaw) * math.cos(pitch)))
    RIGHT = norm((math.cos(yaw), 0, -math.sin(yaw)))
    UP = cross(RIGHT, F)
    if UP[1] < 0:
        UP = tuple(-c for c in UP)

set_camera()

class Model:
    def __init__(self):
        self.v = {}
    def put(self, x, y, z, m):
        self.v[(x, y, z)] = m
    def disc(self, r_of, y0, y1, m, cx=0, cz=0, keep=None):
        R = 26
        for y in range(y0, y1):
            for x in range(int(cx) - R, int(cx) + R + 1):
                for z in range(int(cz) - R, int(cz) + R + 1):
                    dx, dz = x + .5 - cx, z + .5 - cz
                    rr = r_of(y, math.atan2(dz, dx)) if callable(r_of) else r_of
                    if dx * dx + dz * dz <= rr * rr and (keep is None or keep(dx, y, dz)):
                        self.put(x, y, z, m)
    def dome(self, r, y0, h, m, cx=0, cz=0):
        R = int(r) + 2
        for x in range(int(cx) - R, int(cx) + R + 1):
            for z in range(int(cz) - R, int(cz) + R + 1):
                for y in range(y0, y0 + h + 1):
                    if ((x + .5 - cx) / r) ** 2 + ((z + .5 - cz) / r) ** 2 + ((y + .5 - y0) / h) ** 2 <= 1:
                        self.put(x, y, z, m)
    def box(self, x0, x1, y0, y1, z0, z1, m):
        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    self.put(x, y, z, m)
    def top_at(self, x, z):
        ys = [y for (xx, y, zz) in self.v if xx == x and zz == z]
        return max(ys) if ys else None

def project(p):
    return dot(p, RIGHT), dot(p, UP)

def render(model, bounds=None):
    pts = [(x + dx, y + dy, z + dz) for (x, y, z) in model.v for dx in (0, 1) for dy in (0, 1) for dz in (0, 1)]
    us = [dot(p, RIGHT) for p in pts]; vs = [dot(p, UP) for p in pts]; ds = [dot(p, F) for p in pts]
    u0, u1, v0, v1 = (math.floor(min(us)), math.ceil(max(us)), math.floor(min(vs)), math.ceil(max(vs))) if bounds is None else bounds
    dmin, dmax = min(ds) - 2, max(ds) + 2
    W, H = u1 - u0, v1 - v0
    mat = [[None] * W for _ in range(H)]; face = [[None] * W for _ in range(H)]; cellat = [[None] * W for _ in range(H)]
    for j in range(H):
        for i in range(W):
            su = u0 + i + .5; sv = v1 - j - .5
            o = tuple(su * RIGHT[k] + sv * UP[k] + dmin * F[k] for k in range(3))
            t, prev = 0.0, None
            while dmin + t <= dmax:
                p = tuple(o[k] + t * F[k] for k in range(3))
                cell = (math.floor(p[0]), math.floor(p[1]), math.floor(p[2]))
                if cell != prev and cell in model.v:
                    if prev is None:
                        axis = 1
                    else:
                        diff = [abs(cell[k] - prev[k]) for k in range(3)]; axis = diff.index(max(diff))
                    n = [0, 0, 0]; n[axis] = -1 if F[axis] > 0 else 1
                    mat[j][i], face[j][i], cellat[j][i] = model.v[cell], tuple(n), cell
                    break
                prev = cell; t += 0.12
    return mat, face, cellat, (u0, u1, v0, v1)

def smooth(mat, face):
    # Limpieza de escalones: un pixel de frente rodeado de caras de arriba del mismo material pasa a ser de arriba.
    H, W = len(mat), len(mat[0])
    out = [row[:] for row in face]
    for j in range(1, H - 1):
        for i in range(1, W - 1):
            if face[j][i] and face[j][i][1] != 1 and mat[j][i]:
                tops = sum(1 for dj in (-1, 0, 1) for di in (-1, 0, 1) if (dj or di) and mat[j + dj][i + di] == mat[j][i] and face[j + dj][i + di] and face[j + dj][i + di][1] == 1)
                if tops >= 6:
                    out[j][i] = (0, 1, 0)
    return out

def hashp(x, y, z, salt=0):
    return ((x * 73856093) ^ (y * 19349663) ^ (z * 83492791) ^ (salt * 2654435761)) % 1000

def shade(mat, face, cellat, palette, texture=None):
    """palette: material → (contorno, sombra, base, luz). texture: material → función(celda, cara, letras) → letra o None."""
    H, W = len(mat), len(mat[0])
    face = smooth(mat, face)
    out = [['.'] * W for _ in range(H)]
    for j in range(H):
        for i in range(W):
            m = mat[j][i]
            if m is None:
                continue
            o, s, b, l = palette[m]
            n = face[j][i]
            c = l if n[1] == 1 else s if n[0] == 1 else b
            # Sombra de contacto: última fila de frente antes de otra cosa o del vacío.
            if n[1] != 1 and j + 1 < H and (mat[j + 1][i] != m or (face[j + 1][i] and face[j + 1][i][1] == 1)):
                c = s
            if texture and m in texture:
                t = texture[m](cellat[j][i], n, (o, s, b, l))
                if t:
                    c = t
            out[j][i] = c
    for j in range(H):
        for i in range(W):
            m = mat[j][i]
            if m is None:
                continue
            o, s, b, l = palette[m]
            empty = lambda jj, ii: not (0 <= jj < H and 0 <= ii < W) or mat[jj][ii] is None
            if empty(j, i + 1) or empty(j + 1, i):
                out[j][i] = o
            elif empty(j, i - 1) or empty(j - 1, i):
                out[j][i] = s if face[j][i][1] != 1 else b
            elif j + 1 < H and mat[j + 1][i] not in (None, m) and 'semilla' not in (m, mat[j + 1][i]):
                out[j][i] = o
    return [''.join(r) for r in out]

def crop(rows, bbox=None):
    if bbox is None:
        ys = [j for j, r in enumerate(rows) if r.strip('.')]
        xs = [i for r in rows for i, c in enumerate(r) if c != '.']
        bbox = (min(xs), max(xs) + 1, min(ys), max(ys) + 1)
    x0, x1, y0, y1 = bbox
    return [r[x0:x1] for r in rows[y0:y1]], bbox

def anchor(bounds, bbox, point=(0, 0, 0)):
    """Posición en el sprite recortado del punto 3D dado (la base del objeto)."""
    u0, u1, v0, v1 = bounds
    u, v = project(point)
    return (u - u0 - bbox[0], v1 - v - bbox[2])
