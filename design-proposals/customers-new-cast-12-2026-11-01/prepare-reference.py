from pathlib import Path
from PIL import Image
import importlib.util
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('context',ROOT.parent/'generic-customer-game-palette-2026-11-01/render.py')
ctx=importlib.util.module_from_spec(spec);spec.loader.exec_module(ctx)
ctx.prototype=lambda:Image.new('RGBA',(64,80))
im=ctx.scene();im.resize((1280,800),Image.Resampling.NEAREST).save(ROOT/'style-reference.png')
