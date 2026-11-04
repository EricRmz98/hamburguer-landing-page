// Resurrect 64, de Kerrie Lake: https://lospec.com/palette-list/resurrect-64
// Los 64 colores originales, en el orden oficial. Una única paleta para escenas, clientes e interfaz.
export const PALETTE = {
  'negro': '#2e222f',
  'noche': '#3e3546',
  'pizarra': '#625565',
  'tierra': '#966c6c',
  'arena': '#ab947a',
  'gris-violeta': '#694f62',
  'gris-azul': '#7f708a',
  'gris': '#9babb2',
  'gris-claro': '#c7dcd0',
  'blanco': '#ffffff',
  'rojo-oscuro': '#6e2727',
  'rojo-ladrillo': '#b33831',
  'rojo': '#ea4f36',
  'durazno': '#f57d4a',
  'carmesi': '#ae2334',
  'alerta': '#e83b3b',
  'naranja': '#fb6b1d',
  'ambar': '#f79617',
  'amarillo': '#f9c22b',
  'cafe': '#7a3045',
  'oxido': '#9e4539',
  'canela': '#cd683d',
  'piel': '#e6904e',
  'tostado': '#fbb954',
  'oliva-oscuro': '#4c3e24',
  'oliva': '#676633',
  'lima': '#a2a947',
  'lima-claro': '#d5e04b',
  'vainilla': '#fbff86',
  'verde-oscuro': '#165a4c',
  'verde': '#239063',
  'menta': '#1ebc73',
  'verde-claro': '#91db69',
  'pistacho': '#cddf6c',
  'carbon': '#313638',
  'verde-noche': '#374e4a',
  'salvia-oscura': '#547e64',
  'salvia': '#92a984',
  'perla': '#b2ba90',
  'petroleo': '#0b5e65',
  'turquesa-oscuro': '#0b8a8f',
  'turquesa': '#0eaf9b',
  'cian': '#30e1b9',
  'hielo': '#8ff8e2',
  'azul-oscuro': '#323353',
  'azul-noche': '#484a77',
  'azul': '#4d65b4',
  'azul-claro': '#4d9be6',
  'celeste': '#8fd3ff',
  'cafe-oscuro': '#45293f',
  'ciruela': '#6b3e75',
  'violeta': '#905ea9',
  'lavanda': '#a884f3',
  'malva': '#eaaded',
  'vino': '#753c54',
  'magenta': '#a24b6f',
  'rosa-viejo': '#cf657f',
  'rosa': '#ed8099',
  'uva': '#831c5d',
  'frambuesa': '#c32454',
  'rosa-vivo': '#f04f78',
  'coral': '#f68181',
  'piel-clara': '#fca790',
  'crema': '#fdcbb0',
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
  pan: ['cafe', 'oxido', 'canela', 'piel', 'tostado', 'durazno', 'crema'],
  carne: ['negro', 'cafe-oscuro', 'cafe', 'canela', 'piel'],
  'carne-cocinandose': ['cafe-oscuro', 'cafe', 'canela', 'piel', 'piel-clara'],
  'carne-cruda': ['ciruela', 'magenta', 'rosa', 'piel-clara', 'blanco'],
  'carne-quemada': ['negro', 'noche', 'pizarra', 'gris-azul'],
  queso: ['oxido', 'canela', 'naranja', 'ambar', 'amarillo', 'vainilla'],
  lechuga: ['verde-noche', 'verde-oscuro', 'verde', 'verde-claro', 'oliva', 'lima', 'pistacho', 'salvia-oscura'],
  tomate: ['rojo-oscuro', 'rojo', 'coral', 'tostado', 'rosa', 'piel-clara'],
  cebolla: ['ciruela', 'magenta', 'piel-clara', 'blanco'],
  catsup: ['cafe-oscuro', 'rojo-oscuro', 'carmesi', 'alerta', 'rojo-ladrillo', 'rojo', 'rosa', 'coral'],
  mostaza: ['oxido', 'tostado', 'ambar', 'amarillo', 'vainilla'],
  mayonesa: ['arena', 'canela', 'durazno', 'piel-clara', 'crema', 'vainilla', 'blanco'],
  metal: ['negro', 'noche', 'carbon', 'pizarra', 'gris-violeta', 'gris-azul', 'gris', 'gris-claro', 'blanco'],
  madera: ['cafe-oscuro', 'cafe', 'oxido', 'canela', 'piel', 'durazno', 'tierra', 'arena'],
  pared: ['negro', 'noche', 'pizarra', 'gris-azul', 'gris', 'gris-claro', 'crema', 'blanco', 'azul-oscuro'],
  piel: ['cafe', 'canela', 'piel', 'piel-clara', 'crema'],
  etiqueta: ['blanco', 'gris-claro'],
  ceramica: ['gris-azul', 'gris', 'gris-claro', 'blanco', 'arena', 'crema'],
  avisos: ['alerta', 'cian', 'azul', 'blanco'],
  acento: ['oxido', 'naranja', 'ambar', 'amarillo'],
  corazon: ['rojo-oscuro', 'rojo', 'rosa'],
  contorno: ['negro'],
  'pelo-oscuro': ['negro', 'cafe-oscuro', 'cafe'],
  'pelo-claro': ['cafe', 'oxido', 'tostado', 'ambar', 'amarillo'],
  'ropa-azul': ['azul-oscuro', 'azul', 'cian'],
  'ropa-roja': ['rojo-oscuro', 'rojo-ladrillo', 'rojo', 'coral', 'rosa'],
  'ropa-verde': ['verde-oscuro', 'verde', 'verde-claro'],
  'ropa-morada': ['ciruela', 'magenta', 'rosa'],
  'azulejo-rojo': ['noche', 'cafe-oscuro', 'rojo-oscuro', 'rojo-ladrillo', 'carmesi', 'alerta', 'rojo', 'coral'],
} as const satisfies Record<string, readonly ColorName[]>;

export type Material = keyof typeof RAMPS;

export function isMaterial(name: string): name is Material {
  return Object.hasOwn(RAMPS, name);
}
