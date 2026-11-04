import {SPRITES} from '../../src/game/sprites/index.ts';
import {PALETTE} from '../../src/game/sprites/palette.ts';
import {LAYOUTS} from '../../src/game/layouts/index.ts';
import {CUSTOMER_PROFILES} from '../../src/game/sprites/people.ts';
import {resolveSprite} from '../../src/game/sprites/define.ts';
import {writeFileSync} from 'node:fs';
const sprites=[];
for(const def of Object.values(SPRITES))for(const variant of [undefined,...Object.keys(def.variants??{})]){
 const r=resolveSprite(def,variant);
 sprites.push({key:def.id+(variant?':'+variant:''),width:r.width,height:r.height,frames:r.frames,colors:r.colors});
}
writeFileSync(new URL('native-assets.json',import.meta.url),JSON.stringify({palette:PALETTE,layouts:LAYOUTS,customers:CUSTOMER_PROFILES,sprites}));
console.log('30 native definitions and their variants exported for visual review.');
