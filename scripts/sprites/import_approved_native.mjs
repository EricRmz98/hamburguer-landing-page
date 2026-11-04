// One-time import of the approved native cast, preserving every cell and its alpha.
// Recolor from the approved Endesga swatches to the closest Endesga colors.
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { PALETTE } from '../../src/game/sprites/palette.ts';
import { resolveSprite, rasterize } from '../../src/game/sprites/define.ts';
import { imageToSprite } from '../../src/game/sprites/convert.ts';
const dir = new URL('../../design-proposals/customers-native-96x120-2026-11-03/',import.meta.url);
const defs=JSON.parse(readFileSync(new URL('sprite-definitions.json',dir)));
const sourcePalette=JSON.parse(readFileSync(new URL('palette.json',dir)));
const manifest=JSON.parse(readFileSync(new URL('manifest.json',dir)));
const customers=defs.map((def,i)=>{
  const source=resolveSprite(def);
  const bytes=new Uint8ClampedArray(96*120*4);
  source.frames[0].forEach((row,y)=>[...row].forEach((letter,x)=>{
    if(letter==='.')return;
    const hex=sourcePalette[source.colors[letter]];
    bytes.set([parseInt(hex.slice(1,3),16),parseInt(hex.slice(3,5),16),parseInt(hex.slice(5,7),16),255],(y*96+x)*4);
  }));
  const id=manifest.characters[i].id.slice(3);
  const imported=imageToSprite(bytes,96,120,{id});
  const resolved={width:96,height:120,colors:imported.colors,frames:imported.frames};
  const m=manifest.characters[i];
  return {id,name:m.name,style:m.style,facing:m.facing,proportion_scale:m.proportion_scale,face_bounds:m.native_face_bounds.map(Math.round),colors:imported.colors,pixels:imported.frames[0],approved_sha256:createHash('sha256').update(rasterize(resolved)).digest('hex')};
});
writeFileSync(new URL('./customers-native.json',import.meta.url),JSON.stringify({size:[96,120],waist:114,palette:'Endesga 64',author:'ENDESGA',source:'Approved native cast, proportions and alternating orientations, 2026-11-03',customers},null,2)+'\n');
console.log('12 native customers imported without resampling; exact Endesga palette.');
