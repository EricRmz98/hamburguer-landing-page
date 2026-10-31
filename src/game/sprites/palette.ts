// Endesga 32, de ENDESGA (https://lospec.com/palette-list/endesga-32), en el orden de Lospec.
// Es la única fuente de colores de los sprites: las definiciones usan estos nombres, nunca hex sueltos.

export const PALETTE = {
  oxido: '#be4a2f',
  tostado: '#d77643',
  crema: '#ead4aa',
  durazno: '#e4a672',
  canela: '#b86f50',
  cafe: '#733e39',
  'cafe-oscuro': '#3e2731',
  'rojo-oscuro': '#a22633',
  rojo: '#e43b44',
  naranja: '#f77622',
  ambar: '#feae34',
  amarillo: '#fee761',
  'verde-claro': '#63c74d',
  verde: '#3e8948',
  'verde-oscuro': '#265c42',
  'verde-noche': '#193c3e',
  'azul-oscuro': '#124e89',
  azul: '#0099db',
  cian: '#2ce8f5',
  blanco: '#ffffff',
  'gris-claro': '#c0cbdc',
  gris: '#8b9bb4',
  'gris-azul': '#5a6988',
  pizarra: '#3a4466',
  noche: '#262b44',
  negro: '#181425',
  alerta: '#ff0044',
  ciruela: '#68386c',
  magenta: '#b55088',
  rosa: '#f6757a',
  'piel-clara': '#e8b796',
  piel: '#c28569',
} as const;

export type ColorName = keyof typeof PALETTE;

export function isColorName(name: string): name is ColorName {
  return Object.hasOwn(PALETTE, name);
}

export function rgb(name: ColorName): [number, number, number] {
  const hex = PALETTE[name];
  return [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16)) as [number, number, number];
}

/** Luminancia relativa aproximada (0 a 1), para ordenar tonos y revisar la dirección de la luz. */
export function luminance([r, g, b]: readonly number[]): number {
  return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
}

// Rampas por material, de oscuro a claro (ver ASSETS.md, «Estilo y paleta»).
// Un sprite declara sus materiales y la revisión de estilo avisa si usa colores de fuera.
export const RAMPS = {
  pan: ['cafe', 'canela', 'durazno', 'crema'],
  carne: ['negro', 'cafe-oscuro', 'cafe', 'canela', 'piel'],
  'carne-cocinandose': ['cafe-oscuro', 'cafe', 'canela', 'piel', 'piel-clara'],
  'carne-cruda': ['ciruela', 'magenta', 'rosa', 'piel-clara', 'blanco'],
  'carne-quemada': ['negro', 'noche', 'pizarra', 'gris-azul'],
  queso: ['oxido', 'naranja', 'ambar', 'amarillo'],
  lechuga: ['verde-noche', 'verde-oscuro', 'verde', 'verde-claro'],
  tomate: ['rojo-oscuro', 'rojo', 'rosa'],
  cebolla: ['ciruela', 'magenta', 'piel-clara', 'blanco'],
  catsup: ['cafe-oscuro', 'rojo-oscuro', 'rojo', 'rosa'],
  mostaza: ['oxido', 'tostado', 'ambar', 'amarillo'],
  mayonesa: ['canela', 'durazno', 'crema', 'blanco'],
  metal: ['negro', 'noche', 'pizarra', 'gris-azul', 'gris', 'gris-claro'],
  madera: ['cafe-oscuro', 'cafe', 'canela', 'piel'],
  pared: ['negro', 'noche', 'pizarra', 'azul-oscuro'],
  piel: ['cafe', 'canela', 'piel', 'piel-clara', 'crema'],
  etiqueta: ['blanco', 'gris-claro'],
  ceramica: ['gris-azul', 'gris', 'gris-claro', 'blanco'],
  avisos: ['alerta', 'cian', 'azul', 'blanco'],
  acento: ['oxido', 'naranja', 'ambar', 'amarillo'],
  corazon: ['rojo-oscuro', 'rojo', 'rosa'],
  contorno: ['negro'],
  'pelo-oscuro': ['negro', 'cafe-oscuro', 'cafe'],
  'pelo-claro': ['cafe', 'oxido', 'tostado', 'ambar', 'amarillo'],
  'ropa-azul': ['azul-oscuro', 'azul', 'cian'],
  'ropa-roja': ['rojo-oscuro', 'rojo', 'rosa'],
  'ropa-verde': ['verde-oscuro', 'verde', 'verde-claro'],
  'ropa-morada': ['ciruela', 'magenta', 'rosa'],
} as const satisfies Record<string, readonly ColorName[]>;

export type Material = keyof typeof RAMPS;

export function isMaterial(name: string): name is Material {
  return Object.hasOwn(RAMPS, name);
}
