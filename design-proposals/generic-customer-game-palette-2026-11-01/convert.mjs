import {readFileSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {imageToSprite} from '../../src/game/sprites/convert.ts';
import {defineSprite,resolveSprite,rasterize} from '../../src/game/sprites/define.ts';
import {validateSprite,lintSprite} from '../../src/game/sprites/validate.ts';
import {buildAtlas} from '../../src/game/sprites/atlas.ts';
import {SPRITES} from '../../src/game/sprites/index.ts';
import assert from 'node:assert/strict';
import {LAYOUTS} from '../../src/game/layouts/index.ts';

const root=new URL('./',import.meta.url);
const results=[];
for(const layout of Object.values(LAYOUTS)){
 const scale=layout.customer[2]/64;
 assert.equal(scale,1.5);
 assert.equal(layout.customer[3],80*scale);
 assert.equal(layout.customer[1]+76*scale,layout.counter[1]);
}
for(const [stem,height,id] of [['full',118,'cliente_generico_completo_prueba'],['counter',80,'cliente_generico_barra_prueba']]){
 const raw=new Uint8ClampedArray(readFileSync(new URL(`${stem}.rgba`,root)));
 const imported=imageToSprite(raw,64,height,{id});
 const def=defineSprite({id,size:[64,height],materials:['ceramica'],colors:imported.colors,pixels:imported.frames[0].join('\n')});
 assert.equal(imported.adjusted,0);
 assert.deepEqual(validateSprite(def),[]);
 assert.deepEqual(lintSprite(def),[]);
 assert.deepEqual(rasterize(resolveSprite(def)),raw);
 const source="import { defineSprite } from '../../src/game/sprites/define.ts';\n\n"+imported.text.replace('  pixels:',"  materials: ['ceramica'],\n  pixels:")+"\n";
 writeFileSync(new URL(`customer-${stem}.ts`,root),source);
 writeFileSync(new URL(`customer-${stem}.json`,root),JSON.stringify(def,null,2)+'\n');
 const atlas=buildAtlas([...Object.values(SPRITES),def]);
 const entry=atlas.entries[id];
 assert.equal(entry.width,64);assert.equal(entry.height,height);
 for(let y=0;y<height;y++){
  const from=((entry.y+y)*atlas.width+entry.x)*4;
  assert.deepEqual(atlas.data.subarray(from,from+64*4),raw.subarray(y*64*4,(y+1)*64*4));
 }
 results.push({id,size:def.size,colors:def.colors,validation:'passed',style:'passed',native_roundtrip:'pixel_exact',atlas_copy:'pixel_exact',layout_fit:'64x80_matches_current_customer_frame_waist_76'});
}
writeFileSync(new URL('engine-checks.json',root),JSON.stringify(results,null,2)+'\n');
console.log(JSON.stringify(results,null,2));
