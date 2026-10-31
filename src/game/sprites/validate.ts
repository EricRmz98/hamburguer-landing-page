import { TRANSPARENT, resolveSprite, rows, sourceWidth, type Colors, type SpriteDef, type TilemapDef } from './define.ts';
import { RAMPS, isColorName, isMaterial, luminance, rgb } from './palette.ts';

// Validación de las definiciones. Corre en las pruebas y en la página de revisión.

function checkColors(colors: Partial<Colors>, label: string, errors: string[]) {
  for (const [letter, name] of Object.entries(colors)) {
    if (letter.length !== 1) errors.push(`${label}: «${letter}» debe ser una sola letra`);
    if (letter === TRANSPARENT) errors.push(`${label}: «.» está reservado para transparente`);
    if (!name || !isColorName(name)) errors.push(`${label}: el color «${name}» no existe en la paleta`);
  }
}

function checkRows(lines: string[], width: number, colors: Colors, label: string, errors: string[]) {
  lines.forEach((row, y) => {
    if (row.length !== width) errors.push(`${label}, fila ${y}: mide ${row.length}, se esperaba ${width}`);
    const unknown = new Set([...row].filter((ch) => ch !== TRANSPARENT && !(ch in colors)));
    for (const ch of unknown) errors.push(`${label}, fila ${y}: la letra «${ch}» no tiene color`);
  });
}

function checkFrames(sources: readonly string[], height: number, width: number, colors: Colors, label: string, errors: string[]) {
  sources.forEach((source, i) => {
    const name = sources.length > 1 ? `${label}, cuadro ${i + 1}` : label;
    const lines = rows(source);
    if (lines.length !== height) errors.push(`${name}: tiene ${lines.length} filas, se esperaban ${height}`);
    checkRows(lines, width, colors, name, errors);
  });
}

export function validateSprite(def: SpriteDef): string[] {
  const errors: string[] = [];
  const [, height] = def.size;
  const width = sourceWidth(def);

  if (!def.id) errors.push('Falta el id');
  checkColors(def.colors, 'Colores', errors);
  const materials = [...(def.materials ?? []), ...Object.values(def.variants ?? {}).flatMap((v) => v.materials ?? [])];
  for (const material of new Set(materials)) {
    if (!isMaterial(material)) errors.push(`El material «${material}» no existe (ver RAMPS en palette.ts)`);
  }
  if ((def.pixels === undefined) === (def.frames === undefined)) {
    errors.push('Debe definir «pixels» o «frames» (uno de los dos)');
  }
  const base = def.frames ?? (def.pixels !== undefined ? [def.pixels] : []);
  if (def.frames && def.frames.length === 0) errors.push('«frames» está vacío');
  checkFrames(base, height, width, def.colors, 'Base', errors);

  for (const [name, v] of Object.entries(def.variants ?? {})) {
    const label = `Variante «${name}»`;
    if (v.colors) checkColors(v.colors, label, errors);
    const colors = { ...def.colors, ...v.colors } as Colors;
    const own = v.frames ?? (v.pixels !== undefined ? [v.pixels] : undefined);
    if (own) checkFrames(own, height, width, colors, label, errors);
    else if (v.colors) checkFrames(base, height, width, colors, label, errors);
    for (const [index, row] of Object.entries(v.patch ?? {})) {
      const y = Number(index);
      if (!Number.isInteger(y) || y < 0 || y >= height) errors.push(`${label}: el parche de la fila ${index} está fuera del sprite`);
      checkRows([row.trim()], width, colors, `${label}, parche ${index}`, errors);
    }
  }
  return errors;
}

// ── Revisión de estilo ─────────────────────────────────────────────────────
// Avisos, no errores: el sprite se puede dibujar, pero se sale de la guía de estilo.

/**
 * Dentro de un material, el centro de sus tonos claros debe quedar arriba y a la izquierda del de sus
 * tonos oscuros (luz desde arriba a la izquierda). Se revisa por material para que una etiqueta clara
 * abajo o una tapa gris arriba no confundan la comparación.
 */
function lightDirection(frame: string[], colors: Colors, group: Set<string>) {
  const pixels: { x: number; y: number; l: number }[] = [];
  frame.forEach((row, y) =>
    [...row].forEach((letter, x) => {
      const name = colors[letter];
      if (letter !== TRANSPARENT && name && group.has(name)) pixels.push({ x, y, l: luminance(rgb(name)) });
    }),
  );
  if (pixels.length < 6) return null;
  const sorted = pixels.map((p) => p.l).sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)];
  const centroid = (list: typeof pixels) => ({
    x: list.reduce((sum, p) => sum + p.x, 0) / list.length,
    y: list.reduce((sum, p) => sum + p.y, 0) / list.length,
  });
  const light = pixels.filter((p) => p.l > median);
  const dark = pixels.filter((p) => p.l < median);
  if (!light.length || !dark.length) return null;
  const tolerance = { x: Math.max(0.5, (frame[0]?.length ?? 0) * 0.03), y: Math.max(0.5, frame.length * 0.03) };
  const a = centroid(light);
  const b = centroid(dark);
  return { rightIsLighter: a.x > b.x + tolerance.x, bottomIsLighter: a.y > b.y + tolerance.y };
}

export function lintSprite(def: SpriteDef): string[] {
  const warnings: string[] = [];

  const used = new Set<string>();
  const collect = (source: string) => rows(source).forEach((row) => [...row].forEach((ch) => used.add(ch)));
  (def.frames ?? [def.pixels ?? '']).forEach(collect);
  for (const v of Object.values(def.variants ?? {})) {
    (v.frames ?? (v.pixels !== undefined ? [v.pixels] : [])).forEach(collect);
    Object.values(v.patch ?? {}).forEach(collect);
  }
  for (const letter of Object.keys(def.colors)) {
    if (!used.has(letter)) warnings.push(`La letra «${letter}» está declarada pero no se usa`);
  }

  for (const variant of [undefined, ...Object.keys(def.variants ?? {})]) {
    const label = variant ? `Variante «${variant}»` : 'Base';
    const sprite = resolveSprite(def, variant);
    const letters = new Set(sprite.frames.flat().join(''));
    letters.delete(TRANSPARENT);

    const materials = (variant && def.variants?.[variant]?.materials) || def.materials;
    if (materials) {
      const allowed = new Set<string>(materials.flatMap((m) => (isMaterial(m) ? RAMPS[m] : [])));
      for (const letter of letters) {
        const name = sprite.colors[letter];
        if (name && !allowed.has(name)) {
          warnings.push(`${label}: «${name}» (letra ${letter}) no pertenece a ${materials.join(', ')}`);
        }
      }
    }

    // Un color que comparten dos materiales del sprite (p. ej. gris-claro en tapa y etiqueta) es ambiguo:
    // no se sabe a cuál pertenece cada pixel, así que se deja fuera de la comparación.
    const declared = (materials ?? []).filter(isMaterial);
    const shared = new Set<string>(
      declared.flatMap((m) => RAMPS[m]).filter((c, i, all) => all.indexOf(c) !== i),
    );
    if (def.lint?.light === false) continue; // excepción declarada en el sprite, con su motivo
    const groups = declared.length
      ? declared.map((m) => ({ name: m, colors: new Set<string>(RAMPS[m].filter((c) => !shared.has(c))) }))
      : [{ name: 'sprite', colors: new Set<string>(Object.values(sprite.colors)) }];
    for (const group of groups) {
      const result = lightDirection(sprite.frames[0] ?? [], sprite.colors, group.colors);
      if (result?.rightIsLighter) warnings.push(`${label}, ${group.name}: los tonos claros quedan a la derecha; la luz viene de la izquierda`);
      if (result?.bottomIsLighter) warnings.push(`${label}, ${group.name}: los tonos claros quedan abajo; la luz viene de arriba`);
    }
  }
  return warnings;
}

export function validateTilemap(def: TilemapDef, sprites: Record<string, SpriteDef>): string[] {
  const errors: string[] = [];
  for (const [letter, id] of Object.entries(def.tiles)) {
    const tile = sprites[id];
    if (letter.length !== 1) errors.push(`«${letter}» debe ser una sola letra`);
    if (!tile) errors.push(`El tile «${id}» no existe`);
    else if (tile.size[0] !== def.tileSize || tile.size[1] !== def.tileSize) {
      errors.push(`El tile «${id}» mide ${tile.size.join(' × ')}, se esperaba ${def.tileSize} × ${def.tileSize}`);
    }
  }
  const lines = rows(def.map);
  const width = lines[0]?.length ?? 0;
  lines.forEach((row, y) => {
    if (row.length !== width) errors.push(`Mapa, fila ${y}: mide ${row.length}, se esperaba ${width}`);
    for (const ch of new Set(row)) if (!(ch in def.tiles)) errors.push(`Mapa, fila ${y}: la letra «${ch}» no tiene tile`);
  });
  return errors;
}
