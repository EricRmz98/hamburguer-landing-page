// Endesga 64, de ENDESGA: https://lospec.com/palette-list/endesga-64
// Los 64 colores oficiales; escenas, clientes e interfaz comparten esta paleta.
export const PALETTE = {
  'alerta': '#ff0040',
  'negro': '#131313',
  'carbon': '#1b1b1b',
  'grafito': '#272727',
  'gris-oscuro': '#3d3d3d',
  'gris-neutro': '#5d5d5d',
  'gris-medio': '#858585',
  'plata': '#b4b4b4',
  'blanco': '#ffffff',
  'gris-claro': '#c7cfdd',
  'gris': '#92a1b9',
  'gris-azul': '#657392',
  'pizarra': '#424c6e',
  'noche': '#2a2f4e',
  'azul-tinta': '#1a1932',
  'tinta': '#0e071b',
  'cafe-negro': '#1c121c',
  'cafe-oscuro': '#391f21',
  'cafe': '#5d2c28',
  'oxido': '#8a4836',
  'canela': '#bf6f4a',
  'piel': '#e69c69',
  'piel-clara': '#f6ca9f',
  'crema': '#f9e6cf',
  'tostado': '#edab50',
  'durazno': '#e07438',
  'naranja-oscuro': '#c64524',
  'tierra': '#8e251d',
  'naranja': '#ff5000',
  'ambar-oscuro': '#ed7614',
  'ambar': '#ffa214',
  'amarillo': '#ffc825',
  'vainilla': '#ffeb57',
  'pistacho': '#d3fc7e',
  'lima': '#99e65f',
  'verde-claro': '#5ac54f',
  'verde': '#33984b',
  'verde-oscuro': '#1e6f50',
  'verde-noche': '#134c4c',
  'petroleo': '#0c2e44',
  'azul-oscuro': '#00396d',
  'azul': '#0069aa',
  'azul-claro': '#0098dc',
  'cian': '#00cdf9',
  'cian-claro': '#0cf1ff',
  'hielo': '#94fdff',
  'rosa-palido': '#fdd2ed',
  'malva': '#f389f5',
  'magenta-neon': '#db3ffd',
  'violeta': '#7a09fa',
  'ultravioleta': '#3003d9',
  'indigo': '#0c0293',
  'azul-profundo': '#03193f',
  'ciruela-oscura': '#3b1443',
  'ciruela': '#622461',
  'magenta': '#93388f',
  'lila': '#ca52c9',
  'rosa-viejo': '#c85086',
  'rosa': '#f68187',
  'coral': '#f5555d',
  'rojo': '#ea323c',
  'rojo-ladrillo': '#c42430',
  'carmesi': '#891e2b',
  'rojo-oscuro': '#571c27',
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
  'carne-cruda': ['rojo-oscuro', 'rosa-viejo', 'rosa', 'piel-clara', 'blanco'],
  'carne-quemada': ['negro', 'noche', 'pizarra', 'gris-azul'],
  queso: ['oxido', 'canela', 'naranja', 'ambar', 'amarillo', 'vainilla'],
  lechuga: ['verde-noche', 'verde-oscuro', 'verde', 'verde-claro', 'verde-oscuro', 'lima', 'pistacho', 'verde-oscuro'],
  tomate: ['rojo-oscuro', 'rojo', 'coral', 'tostado', 'rosa', 'piel-clara'],
  cebolla: ['ciruela', 'magenta', 'piel-clara', 'blanco'],
  catsup: ['cafe-oscuro', 'rojo-oscuro', 'carmesi', 'alerta', 'rojo-ladrillo', 'rojo', 'rosa', 'coral'],
  mostaza: ['oxido', 'tostado', 'ambar', 'amarillo', 'vainilla'],
  mayonesa: ['plata', 'canela', 'durazno', 'piel-clara', 'crema', 'vainilla', 'blanco'],
  metal: ['negro', 'noche', 'carbon', 'pizarra', 'gris-oscuro', 'gris-azul', 'gris', 'gris-claro', 'blanco'],
  madera: ['cafe-oscuro', 'cafe', 'oxido', 'canela', 'piel', 'durazno', 'tierra', 'plata'],
  pared: ['negro', 'noche', 'pizarra', 'gris-azul', 'gris', 'gris-claro', 'crema', 'blanco', 'azul-oscuro'],
  piel: ['cafe', 'canela', 'piel', 'piel-clara', 'crema'],
  etiqueta: ['blanco', 'gris-claro'],
  ceramica: ['gris-azul', 'gris', 'gris-claro', 'blanco', 'plata', 'crema'],
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
  interior: ['negro', 'carbon', 'grafito', 'gris-oscuro', 'gris-neutro', 'gris-medio', 'plata', 'blanco', 'gris-claro', 'gris', 'gris-azul', 'pizarra', 'noche', 'azul-tinta', 'tinta', 'cafe-negro', 'cafe-oscuro', 'cafe', 'oxido', 'rojo-oscuro', 'carmesi', 'rojo-ladrillo', 'rojo', 'coral', 'crema', 'tostado', 'verde-noche', 'verde-oscuro', 'verde', 'verde-claro'],
  'azulejo-rojo': ['gris-claro', 'gris-azul', 'noche', 'cafe-oscuro', 'rojo-oscuro', 'rojo-ladrillo', 'carmesi', 'alerta', 'rojo', 'coral'],
} as const satisfies Record<string, readonly ColorName[]>;

export type Material = keyof typeof RAMPS;

export function isMaterial(name: string): name is Material {
  return Object.hasOwn(RAMPS, name);
}
