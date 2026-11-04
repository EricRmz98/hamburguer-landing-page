import { PALETTE, luminance, rgb, type ColorName } from './palette.ts';

// Conversión de una imagen (por ejemplo, un PNG editado en Aseprite) a una definición de texto.
// Cada color se lleva al más cercano de Endesga 64; los pixeles casi transparentes quedan como «.».

const LETTER_ORDER = 'osblhacdefgijkmnpqrtuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&';
const COLORS = Object.keys(PALETTE) as ColorName[];

export function nearestColor(r: number, g: number, b: number): { name: ColorName; exact: boolean } {
  let best = COLORS[0];
  let bestDistance = Infinity;
  for (const name of COLORS) {
    const [pr, pg, pb] = rgb(name);
    const distance = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2;
    if (distance < bestDistance) {
      best = name;
      bestDistance = distance;
    }
  }
  return { name: best, exact: bestDistance === 0 };
}

export interface ImportOptions {
  id: string;
  /** Ancho de cada cuadro si la imagen es una tira horizontal de animación. */
  frameWidth?: number;
  /** Letras preferidas por color (al reimportar un sprite existente, para conservar sus letras). */
  letters?: Partial<Record<ColorName, string>>;
}

export interface ImportResult {
  text: string;
  colors: Record<string, ColorName>;
  frames: string[][];
  /** Pixeles cuyo color no era de la paleta y se ajustó al más cercano. */
  adjusted: number;
  warnings: string[];
}

const camelCase = (id: string) => id.replace(/[_-](\w)/g, (_, c: string) => c.toUpperCase());

export function imageToSprite(data: Uint8ClampedArray, width: number, height: number, options: ImportOptions): ImportResult {
  const warnings: string[] = [];
  let frameWidth = options.frameWidth ?? width;
  if (frameWidth <= 0 || width % frameWidth !== 0) {
    warnings.push(`El ancho ${width} no se divide en cuadros de ${frameWidth}; se importa como un solo cuadro`);
    frameWidth = width;
  }

  let adjusted = 0;
  const names: (ColorName | null)[] = [];
  for (let i = 0; i < width * height; i++) {
    const [r, g, b, a] = data.subarray(i * 4, i * 4 + 4);
    if (a < 128) {
      names.push(null);
      continue;
    }
    const { name, exact } = nearestColor(r, g, b);
    if (!exact) adjusted++;
    names.push(name);
  }
  if (adjusted) warnings.push(`${adjusted} pixeles no eran de Endesga 64 y se ajustaron al color más cercano`);

  // Letras: primero las preferidas; las demás, de oscuro a claro (o = contorno … h = brillo).
  const used = [...new Set(names.filter((n): n is ColorName => n !== null))].sort(
    (a, b) => luminance(rgb(a)) - luminance(rgb(b)),
  );
  const letterOf = new Map<ColorName, string>();
  const taken = new Set<string>();
  for (const name of used) {
    const preferred = options.letters?.[name];
    if (preferred && !taken.has(preferred)) {
      letterOf.set(name, preferred);
      taken.add(preferred);
    }
  }
  for (const name of used) {
    if (letterOf.has(name)) continue;
    const letter = [...LETTER_ORDER].find((l) => !taken.has(l));
    if (!letter) throw new Error('La imagen usa más colores de los que hay letras disponibles');
    letterOf.set(name, letter);
    taken.add(letter);
  }

  const frames: string[][] = [];
  for (let f = 0; f < width / frameWidth; f++) {
    const lines: string[] = [];
    for (let y = 0; y < height; y++) {
      let line = '';
      for (let x = 0; x < frameWidth; x++) {
        const name = names[y * width + f * frameWidth + x];
        line += name ? letterOf.get(name)! : '.';
      }
      lines.push(line);
    }
    frames.push(lines);
  }

  const colors = Object.fromEntries([...letterOf].map(([name, letter]) => [letter, name]));
  const colorText = [...letterOf].map(([name, letter]) => `${letter}: '${name}'`).join(', ');
  const block = (lines: string[], indent: string) => lines.map((l) => indent + l).join('\n');
  const body =
    frames.length === 1
      ? `  pixels: \`\n${block(frames[0], '    ')}\n  \`,`
      : `  frames: [\n${frames.map((f) => `    \`\n${block(f, '      ')}\n    \`,`).join('\n')}\n  ],`;
  const text = [
    `export const ${camelCase(options.id)} = defineSprite({`,
    `  id: '${options.id}',`,
    `  size: [${frameWidth}, ${height}],`,
    `  colors: { ${colorText} },`,
    body,
    `});`,
  ].join('\n');

  return { text, colors, frames, adjusted, warnings };
}
