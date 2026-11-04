# Generador histórico (48 × 80), conservado para las propuestas archivadas.
# Los 12 clientes nativos activos se regeneran con customers_gen.py y write_people.py.
W, H = 48, 80
SHADE = {  # material: (base, sombra, luz, ancho de luz, ancho de sombra)
    'piel': ('q', 'p', 'r', 2, 3),
    'pelo': ('h', 'i', 'j', 3, 3),
    'camisa': ('c', 'd', 'e', 3, 6),
}

def ellipse(grid, cx, cy, rx, ry, m, only=None):
    for y in range(H):
        for x in range(W):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1 and (only is None or only(x, y, grid[y][x])):
                grid[y][x] = m

def span(grid, y, x0, x1, m):
    for x in range(max(0, x0), min(W, x1)):
        grid[y][x] = m

def body(female):
    g = [[None] * W for _ in range(H)]
    if female:  # pelo largo por detrás: lo primero, para que el cuerpo y la cara queden encima
        ellipse(g, 24, 22, 14.5, 19, 'pelo')
    # Torso con hombros redondeados.
    for y in range(30, H):
        half = min(22 if not female else 20, 8 + (y - 30) * 4)
        span(g, y, 24 - half, 24 + half, 'camisa')
    # Cuello.
    for y in range(23, 33):
        span(g, y, 19, 29, 'piel')
    # Escote: V en el hombre, redondo en la mujer.
    for y in range(30, 37):
        half = (36 - y) if not female else max(0, 6 - abs(y - 31) * 1.3)
        span(g, y, round(24 - half), round(24 + half), 'piel')
    ellipse(g, 24, 14, 11, 13, 'piel')               # cabeza
    for y in range(12, 17):                          # orejas
        g[y][12] = g[y][13] = 'piel'
        g[y][34] = g[y][35] = 'piel'
    if female:
        ellipse(g, 24, 13, 12, 13.5, 'pelo', lambda x, y, c: y <= 8 or (y <= 13 and x <= 16))  # flequillo de lado
        for cx in (12, 35):                          # mechones al frente, sobre los hombros
            for x in range(cx - 2, cx + 3):
                for y in range(14, 39 - abs(x - cx) * 2):
                    if g[y][x] in ('camisa', 'pelo', None):
                        g[y][x] = 'pelo'
    else:
        ellipse(g, 24, 13.5, 12, 13.5, 'pelo', lambda x, y, c: y <= 7 or (y <= 11 and (x <= 14 or x >= 33)))
    return g

def paint(g):
    rows = [['.'] * W for _ in range(H)]
    for y in range(H):
        x = 0
        while x < W:
            m = g[y][x]
            if m is None:
                x += 1
                continue
            end = x
            while end < W and g[y][end] == m:
                end += 1
            base, shadow, light, lw, sw = SHADE[m]
            for i in range(x, end):
                rows[y][i] = light if i - x < lw else shadow if end - 1 - i < sw else base
            x = end
    for y in range(H):  # contorno donde el material toca el vacío
        for x in range(W):
            if g[y][x] is None:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and g[ny][nx] is None:
                    rows[y][x] = 'o'
            if y > 0 and g[y][x] == 'piel' and g[y - 1][x] == 'pelo' and rows[y][x] != 'o':
                rows[y][x] = 'p'                     # sombra del pelo sobre la piel
    for y in range(23, H):                           # cuello en sombra bajo la barbilla; escote en tono base
        for x in range(W):
            if g[y][x] == 'piel' and rows[y][x] != 'o' and y > 25:
                rows[y][x] = 'p' if y < 30 else ('q' if rows[y][x] != 'p' else 'p')
    for y in range(40, H):                           # pliegues entre brazos y torso
        for x in (9, 38):
            if g[y][x] == 'camisa' and rows[y][x] != 'o':
                rows[y][x] = 'd'
    return rows

def face(rows, female, expr):
    put = lambda x, y, c: rows[y].__setitem__(x, c)
    for ex in (18, 28):                              # ojos
        for dy in (13, 14):
            put(ex, dy, 'o'); put(ex + 1, dy, 'o')
    if female:
        put(17, 12, 'o'); put(30, 12, 'o')           # pestañas
        put(12, 17, 'g'); put(35, 17, 'g')           # aretes
    if expr == 'enojado':
        for x, y in ((17, 10), (18, 10), (19, 11), (28, 11), (29, 10), (30, 10)):
            put(x, y, 'o')
    else:
        for x in (17, 18, 19, 28, 29, 30):
            put(x, 11, 'i')                          # cejas del color del pelo
    put(25, 17, 'p')                                 # nariz
    if expr == 'feliz':
        put(21, 20, 'o'); put(27, 20, 'o')
        for x in range(22, 27): put(x, 21, 'o')
    elif expr == 'enojado':
        for x in range(21, 27): put(x, 20, 'o')
        put(20, 21, 'o'); put(27, 21, 'o')
    else:
        for x in range(22, 27): put(x, 20, 'o')
    return [''.join(r) for r in rows]

def frames(female):
    return [face(paint(body(female)), female, e) for e in ('esperando', 'feliz', 'enojado')]
