import { INGREDIENTS, SALSAS, VERDURAS, stackHeight, type IngredientId } from './ingredients.ts';

// Una receta es una pila de abajo hacia arriba que cumple la gramática del plan:
//   hamburguesa  = pan_base  sección  [ pan_medio  sección ]  pan_tapa
//   sección      = bloque_carne+  verdura*  salsa*
//   bloque_carne = carne  [ queso ]

export interface Recipe {
  name: string;
  stack: readonly IngredientId[];
}

export const CATALOG = {
  clasica: { name: 'Clásica', stack: ['pan_base', 'carne', 'queso', 'lechuga', 'tomate', 'catsup', 'pan_tapa'] },
  sencilla: { name: 'Sencilla', stack: ['pan_base', 'carne', 'catsup', 'mostaza', 'pan_tapa'] },
  doble: {
    name: 'Doble',
    stack: ['pan_base', 'carne', 'queso', 'carne', 'queso', 'cebolla', 'mostaza', 'pan_tapa'],
  },
  triple: {
    name: 'Triple',
    stack: ['pan_base', 'carne', 'queso', 'carne', 'carne', 'queso', 'lechuga', 'catsup', 'pan_tapa'],
  },
  cuadruple: {
    name: 'La torre',
    stack: [
      'pan_base',
      'carne', 'queso', 'carne', 'queso', 'carne', 'queso', 'carne', 'queso',
      'cebolla', 'mostaza', 'pan_tapa',
    ],
  },
  tresPanes: {
    name: 'Tres panes',
    stack: [
      'pan_base', 'carne', 'queso', 'lechuga',
      'pan_medio', 'carne', 'queso', 'tomate', 'mayonesa',
      'pan_tapa',
    ],
  },
} as const satisfies Record<string, Recipe>;

const MAX_CARNES = 4;
const MAX_SALSAS_PER_SECTION = 2;

const isVerdura = (id: IngredientId) => INGREDIENTS[id].kind === 'verdura';
const isSalsa = (id: IngredientId) => INGREDIENTS[id].kind === 'salsa';

/** Devuelve la lista de errores; una receta válida devuelve una lista vacía. */
export function validateRecipe(stack: readonly IngredientId[], maxHeight = Infinity): string[] {
  const errors: string[] = [];
  if (stack[0] !== 'pan_base') errors.push('Debe empezar con pan_base');
  if (stack[stack.length - 1] !== 'pan_tapa') errors.push('Debe terminar con pan_tapa');
  if (stack.filter((id) => id === 'pan_base').length !== 1) errors.push('Debe tener exactamente un pan_base');
  if (stack.filter((id) => id === 'pan_tapa').length !== 1) errors.push('Debe tener exactamente un pan_tapa');
  if (stack.filter((id) => id === 'pan_medio').length > 1) errors.push('Solo puede haber un pan_medio');
  if (errors.length) return errors;

  const inner = stack.slice(1, -1);
  const sections: IngredientId[][] = [[]];
  for (const id of inner) {
    if (id === 'pan_medio') sections.push([]);
    else sections[sections.length - 1].push(id);
  }

  let carnes = 0;
  sections.forEach((section, s) => {
    let i = 0;
    let sectionCarnes = 0;
    while (section[i] === 'carne') {
      sectionCarnes++;
      i++;
      if (section[i] === 'queso') i++;
    }
    if (sectionCarnes === 0) errors.push(`La sección ${s + 1} no tiene carne`);
    carnes += sectionCarnes;

    const verduras = new Set<IngredientId>();
    while (i < section.length && isVerdura(section[i])) {
      if (verduras.has(section[i])) errors.push(`${section[i]} repetido en la sección ${s + 1}`);
      verduras.add(section[i]);
      i++;
    }
    const salsas = new Set<IngredientId>();
    while (i < section.length && isSalsa(section[i])) {
      if (salsas.has(section[i])) errors.push(`${section[i]} repetido en la sección ${s + 1}`);
      salsas.add(section[i]);
      i++;
    }
    if (salsas.size > MAX_SALSAS_PER_SECTION) errors.push(`Más de ${MAX_SALSAS_PER_SECTION} salsas en la sección ${s + 1}`);
    if (i < section.length) errors.push(`${section[i]} fuera de orden en la sección ${s + 1}`);
  });

  if (carnes > MAX_CARNES) errors.push(`Más de ${MAX_CARNES} carnes`);
  if (stackHeight(stack) > maxHeight) errors.push(`Altura ${stackHeight(stack)} mayor que ${maxHeight}`);
  return errors;
}

type Rng = () => number;

const randInt = (min: number, max: number, rng: Rng) => min + Math.floor(rng() * (max - min + 1));
const pick = <T>(items: readonly T[], rng: Rng): T => items[Math.floor(rng() * items.length)];

function sample<T>(items: readonly T[], count: number, rng: Rng): T[] {
  const pool = [...items];
  const out: T[] = [];
  while (out.length < count && pool.length) out.push(pool.splice(Math.floor(rng() * pool.length), 1)[0]);
  return out;
}

interface SectionShape {
  carnes: number;
  queso: number; // probabilidad de queso sobre cada carne
  verduras: [number, number];
  salsas: [number, number];
}

function buildSection(shape: SectionShape, rng: Rng): IngredientId[] {
  const out: IngredientId[] = [];
  for (let i = 0; i < shape.carnes; i++) {
    out.push('carne');
    if (rng() < shape.queso) out.push('queso');
  }
  out.push(...sample(VERDURAS, randInt(...shape.verduras, rng), rng));
  out.push(...sample(SALSAS, randInt(...shape.salsas, rng), rng));
  return out;
}

function shapesForTier(tier: number, rng: Rng): SectionShape[] {
  switch (tier) {
    case 1:
      return [{ carnes: 1, queso: 0.6, verduras: [0, 2], salsas: [1, 2] }];
    case 2:
      return [{ carnes: 2, queso: 0.7, verduras: [1, 3], salsas: [1, 2] }];
    case 3:
      return [{ carnes: 3, queso: 0.6, verduras: [1, 2], salsas: [1, 2] }];
    case 4:
      return rng() < 0.5
        ? [{ carnes: 4, queso: 0.7, verduras: [0, 2], salsas: [1, 1] }]
        : [
            { carnes: randInt(1, 2, rng), queso: 0.6, verduras: [1, 2], salsas: [0, 1] },
            { carnes: randInt(1, 2, rng), queso: 0.6, verduras: [1, 2], salsas: [1, 1] },
          ];
    default:
      return shapesForTier(pick([2, 3, 4], rng), rng);
  }
}

function nameFor(stack: readonly IngredientId[]): string {
  if (stack.includes('pan_medio')) return 'Tres panes';
  const carnes = stack.filter((id) => id === 'carne').length;
  if (carnes === 1) return stack.includes('queso') ? 'Con queso' : 'Sencilla';
  return ['', '', 'Doble', 'Triple', 'La torre'][carnes];
}

/** Genera una receta válida para el nivel indicado (1 a 4; 5 o más mezcla los niveles 2 a 4). */
export function generateRecipe(tier: number, maxHeight: number, rng: Rng = Math.random): Recipe {
  if (tier === 1 && rng() < 0.3) return pick([CATALOG.clasica, CATALOG.sencilla], rng);
  for (let attempt = 0; attempt < 50; attempt++) {
    const sections = shapesForTier(tier, rng).map((shape) => buildSection(shape, rng));
    const stack: IngredientId[] = ['pan_base', ...sections.flatMap((s, i) => (i ? ['pan_medio' as const, ...s] : s)), 'pan_tapa'];
    if (validateRecipe(stack, maxHeight).length === 0) return { name: nameFor(stack), stack };
  }
  return CATALOG.clasica;
}
