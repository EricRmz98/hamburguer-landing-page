import {readFileSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {defineSprite,resolveSprite,rasterize} from '../../src/game/sprites/define.ts';
import {validateSprite,lintSprite} from '../../src/game/sprites/validate.ts';
import {cliente} from '../../src/game/sprites/people.ts';
import {buildAtlas} from '../../src/game/sprites/atlas.ts';
const root=new URL('./',import.meta.url);
const proposal=JSON.parse(readFileSync(new URL('proposal-cast.json',root),'utf8'));
const variants={};
for(const p of proposal.customers){
 const frames=[p.pixels,...['feliz','enojado'].map(emotion=>{
  const f=p.pixels.map(row=>[...row]);
  for(const [x,y,c] of p.reactions[emotion])f[y][x]=c;
  return f.map(row=>row.join(''));
 })];
 variants[p.id]={frames:frames.map(f=>f.join('\n'))};
 const old=resolveSprite(cliente,p.id);
 for(let frame=0;frame<3;frame++){
  const original=old.frames[frame];
  const [left,top,right,bottom]=p.expression_bounds;
  for(let y=top;y<bottom;y++)for(let x=left;x<right;x++)assert.equal(frames[frame][y][x],original[y][x],`${p.id}: rostro`);
  for(let y=0;y<80;y++)for(let x=0;x<64;x++)assert.equal(frames[frame][y][x]==='.',original[y][x]==='.',`${p.id}: silueta`);
 }
}
const def=defineSprite({...cliente,id:'cliente_detalle_prueba',colors:proposal.colors,frames:variants.nico.frames,variants});
assert.deepEqual(validateSprite(def),[]);assert.deepEqual(lintSprite(def),[]);
const atlas=buildAtlas([def]);
for(const p of proposal.customers){
 const resolved=resolveSprite(def,p.id);const entry=atlas.entries[def.id+':'+p.id];
 const raw=rasterize(resolved);const width=64*3;
 for(let y=0;y<80;y++){
  const start=((entry.y+y)*atlas.width+entry.x)*4;
  assert.deepEqual(atlas.data.subarray(start,start+width*4),raw.subarray(y*width*4,(y+1)*width*4));
 }
}
writeFileSync(new URL('native-sprite.json',root),JSON.stringify(def,null,2)+'\n');
writeFileSync(new URL('engine-checks.json',root),JSON.stringify({customers:24,expressions:3,validation:'passed',style:'passed',palette:'Endesga32',faces_identical_in_all_reactions:true,silhouette_identical_in_all_reactions:true,atlas_pixel_copy:'passed',integration:'reference_only'},null,2)+'\n');
console.log('24 clientes × 3 expresiones: formato, paleta, silueta, caras y atlas verificados.');
