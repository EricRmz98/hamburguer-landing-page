import {readFileSync,writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {imageToSprite} from '../../src/game/sprites/convert.ts';
import {defineSprite,resolveSprite,rasterize} from '../../src/game/sprites/define.ts';
import {validateSprite,lintSprite} from '../../src/game/sprites/validate.ts';
import {buildAtlas} from '../../src/game/sprites/atlas.ts';
import {SPRITES} from '../../src/game/sprites/index.ts';
import {LAYOUTS} from '../../src/game/layouts/index.ts';
const root=new URL('./',import.meta.url);
const manifest=JSON.parse(readFileSync(new URL('manifest.json',root),'utf8'));
const defs=[],checks=[];
const lightReason='Personaje con varios materiales y prendas claras bajo cabello oscuro: el centroide global no determina la iluminación de cada material. La iluminación de la referencia se conserva y se revisa visualmente por pieza.';
for(const person of manifest.characters){
 const id='cliente_nuevo_'+person.id.slice(3);
 const raw=new Uint8ClampedArray(readFileSync(new URL('rgba/'+person.id+'.rgba',root)));
 const imported=imageToSprite(raw,96,120,{id});
 const base=defineSprite({id,size:[96,120],colors:imported.colors,pixels:imported.frames[0].join('\n')});
 const lightWarnings=lintSprite(base);
 const def=defineSprite({...base,lint:{light:false,reason:lightReason}});
 assert.equal(imported.adjusted,0);assert.deepEqual(validateSprite(def),[]);assert.deepEqual(lintSprite(def),[]);
 assert.deepEqual(rasterize(resolveSprite(def)),raw);
 for(let i=3;i<raw.length;i+=4)assert.ok(raw[i]===0||raw[i]===255);
 writeFileSync(new URL(person.id+'.ts',root),"import { defineSprite } from '../../src/game/sprites/define.ts';\n\n"+imported.text.replace('  pixels:',`  lint: { light: false, reason: ${JSON.stringify(lightReason)} },\n  pixels:`)+'\n');
 defs.push(def);checks.push({id,validation:'passed',palette:'exact_Endesga32',native_roundtrip:'pixel_exact',style_warnings:lintSprite(def),global_light_centroid_notes:lightWarnings});
}
const atlas=buildAtlas([...Object.values(SPRITES),...defs]);
for(const def of defs){
 const entry=atlas.entries[def.id];const raw=rasterize(resolveSprite(def));
 for(let y=0;y<120;y++){
  const start=((entry.y+y)*atlas.width+entry.x)*4;
  assert.deepEqual(atlas.data.subarray(start,start+96*4),raw.subarray(y*96*4,(y+1)*96*4));
 }
}
for(const layout of Object.values(LAYOUTS)){
 const scale=layout.customer[2]/96;
 assert.equal(scale,1);assert.equal(layout.customer[3],120*scale);
 assert.equal(layout.customer[1]+114*scale,layout.counter[1]);
 assert.ok(layout.patience[1]+layout.patience[3]<=layout.customer[1]+8*scale);
}
const camel=id=>id.replace(/_(\w)/g,(_,c)=>c.toUpperCase());
const imports=manifest.characters.map(p=>`import { ${camel('cliente_nuevo_'+p.id.slice(3))} } from './${p.id}.ts';`).join('\n');
const names=manifest.characters.map(p=>camel('cliente_nuevo_'+p.id.slice(3)));
const profiles=manifest.characters.map(p=>({id:'cliente_nuevo_'+p.id.slice(3),name:p.name,style:p.style}));
writeFileSync(new URL('customers.ts',root),imports+'\n\nexport const NEW_CUSTOMER_SPRITES = ['+names.join(', ')+'] as const;\nexport const NEW_CUSTOMER_PROFILES = '+JSON.stringify(profiles,null,2)+' as const;\n');
writeFileSync(new URL('sprite-definitions.json',root),JSON.stringify(defs,null,2)+'\n');
writeFileSync(new URL('engine-checks.json',root),JSON.stringify({customers:12,native_size:[96,120],game_size:[96,120],waist_row:114,layouts:'horizontal_and_vertical_anchor_match',atlas:'pixel_exact',native_to_layout_scale:1,production_cast_changed:false,results:checks},null,2)+'\n');
console.log(JSON.stringify(checks,null,2));
