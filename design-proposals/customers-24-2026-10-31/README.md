# Clientes con personalidad — 24 referencias

Primera selección para aprobación, no integrada al juego. Las 24 propuestas conservan 48 × 80 píxeles, el ancla de cabeza/cuerpo de los clientes existentes, Endesga 32, contornos pixelados y luz desde la izquierda. Se reutilizan las proporciones y la base de `people_gen.py`; prendas, peinados y accesorios se dibujan en un generador independiente.

## Ver y aprobar

- `customers-01-12.png`: personajes 01 a 12, escala ×4.
- `customers-13-24.png`: personajes 13 a 24, escala ×4.
- `customers-in-context.png`: seis muestras con el entorno y los objetos finales, escala ×2. Se omite la interfaz para ver la ropa.
- `customer-01-1x.png` … `customer-24-1x.png`: originales transparentes a escala lógica.
- `cast.json`: nombres, estilos, pronombres, peinados, prendas y accesorios.
- `candidate-matrices.json`: las mismas imágenes en matrices de texto y nombres de paleta. No están registradas en `SPRITES` ni `CUSTOMERS`.

Las identidades son personajes ficticios con pronombres definidos; los looks no determinan la identidad. Hay ocho personajes con él, ocho con ella y ocho con elle, con distintos tonos de piel y peinados. Los estilos son una selección inicial, no un inventario exhaustivo de subculturas. Cualquier ropa, accesorio o peinado se puede combinar en la revisión.

## Elenco

| ID | Nombre | Estilo | Pronombres |
| --- | --- | --- | --- |
| 01 | Nico | Hipster, camisa de cuadros y gafas | él |
| 02 | Ren | Gótica, chaqueta y gargantilla | ella |
| 03 | Alex | Techwear, bandas y bolsillos técnicos | elle |
| 04 | Dani | Fútbol, jersey y diadema | ella |
| 05 | Beto | Skater, hoodie y gorro | él |
| 06 | Vale | Punk, cresta, pins y tachuelas | elle |
| 07 | Mar | Grunge, pelo largo y camisa abierta | él |
| 08 | Sol | Indie, cárdigan y gafas | ella |
| 09 | Sam | Streetwear, trenzas y varsity | elle |
| 10 | Ivo | Metal, barba y camiseta de banda ficticia | él |
| 11 | Luz | Kawaii, moños y clips | ella |
| 12 | Noa | Rave, goggles y acentos cian | elle |
| 13 | Teo | Normcore, sobrecamisa y tote | él |
| 14 | Mai | Coquette, cuello blanco y lazo | ella |
| 15 | Jules | Art school, chaqueta y pañuelo | elle |
| 16 | Moren | Athleisure, chándal y auriculares | ella |
| 17 | Chema | Fútbol retro, jersey y bigote | él |
| 18 | Ari | Cyber, flequillo y visor | elle |
| 19 | Ros | Workwear, bolsillos y gorra | él |
| 20 | Andy | Rockabilly, chaqueta y bandana | ella |
| 21 | Fer | Dark academia, blazer y gafas | elle |
| 22 | Leo | Surf, camisa estampada y collar | él |
| 23 | Pao | Sneakerhead, varsity y gorra invertida | ella |
| 24 | Cris | Vintage, chaleco y pelo gris | elle |

## Comprobaciones y límites

Se inspeccionaron ambas láminas y la prueba de contexto. Se diferenciaron las chaquetas gótica y punk mediante colgante, pins y tachuelas. El generador comprueba la paleta de cada píxel visible y exporta solo múltiplos enteros, sin suavizar el personaje. No hay logos de clubes o bandas reales.

Son referencias en pose de espera. Tras la aprobación faltan expresiones feliz/enojada, retoque fino de rasgos y sombras por material, revisión con la interfaz real, contraste con todos los fondos y adaptación de la rotación de clientes. No se modificó `src/game/sprites/people.ts`, el registro del juego ni sus clientes activos. No se ejecuta la compilación porque estas propuestas no entran en la aplicación.

Reproducir con un entorno Python que tenga Pillow:

```sh
python3 design-proposals/customers-24-2026-10-31/generate.py
```
