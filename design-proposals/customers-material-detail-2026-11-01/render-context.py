from pathlib import Path
from PIL import Image
import importlib.util,json
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('detail',ROOT/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('context',ROOT.parent/'generic-customer-game-palette-2026-11-01/render.py');ctx=importlib.util.module_from_spec(spec);spec.loader.exec_module(ctx)
proposal=json.loads((ROOT/'proposal-cast.json').read_text());source=json.loads((ROOT/'source-cast.json').read_text())
out=Image.new('RGB',(1328,1500),g.P['noche'])
g.text(out,(24,20),'PRUEBA CON LA COCINA Y EL ENTORNO',38,'blanco',True)
g.text(out,(24,75),'Misma escala y posición · original a la izquierda, propuesta a la derecha',24,'gris-claro')
for i,key in enumerate(['nico','dani','ari']):
 y=130+i*450
 for j,(label,cast) in enumerate([('ANTES',source),('PROPUESTA',proposal)]):
  person=next(p for p in cast['customers'] if p['id']==key)
  ctx.prototype=lambda rows=person['pixels']:g.render(rows)
  scene=ctx.scene().resize((640,400),Image.Resampling.NEAREST)
  x=16+j*656;g.text(out,(x,y),f'{person["name"].upper()} / {label}',25,'blanco',True)
  out.paste(scene,(x,y+37),scene)
out.save(ROOT/'contexto-antes-despues.png')
# Native game-size contact sheet for judging whether details remain readable.
cw,ch,gap=144,164,12
out=Image.new('RGB',(6*cw+7*gap,120+4*ch+5*gap),g.P['noche'])
g.text(out,(16,18),'PRUEBA / ESCALA DEL JUEGO',28,'blanco',True)
for i,person in enumerate(proposal['customers']):
 x=gap+(i%6)*(cw+gap);y=120+gap+(i//6)*(ch+gap)
 from PIL import ImageDraw
 ImageDraw.Draw(out).rectangle((x,y,x+cw-1,y+ch-1),fill='#e8e9ed')
 g.text(out,(x+8,y+8),person['name'].upper(),16,bold=True)
 im=g.render(person['pixels']).resize((96,120),Image.Resampling.NEAREST);out.paste(im,(x+24,y+35),im)
out.save(ROOT/'clientes-escala-juego.png')
