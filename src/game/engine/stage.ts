import type { BinId, SalsaId } from '../game/ingredients.ts';

/** [x, y, ancho, alto] en pixeles lógicos del escenario. */
export type Rect = readonly [number, number, number, number];

export interface Layout {
  name: 'horizontal' | 'vertical';
  w: number;
  h: number;
  hud: Rect;
  pause: Rect; // botón independiente, en coordenadas del escenario
  ticket: Rect;
  customer: Rect;
  customerBubble: Rect;
  counter: Rect; // barra: superficie de trabajo completa; el cliente se recarga en su borde superior
  plate: Rect;
  bubble: Rect;
  bottles: Record<SalsaId, Rect>;
  grill: Rect;
  slots: readonly Rect[];
  charola: Rect;
  tocino: Rect;
  bins: Record<BinId, Rect>;
}

/** Elige la disposición y la mayor escala entera que cabe en el espacio disponible. */
export function fitStage(width: number, height: number, layouts: { horizontal: Layout; vertical: Layout }) {
  const layout = width < 640 && height > width ? layouts.vertical : layouts.horizontal;
  const scale = Math.max(1, Math.floor(Math.min(width / layout.w, height / layout.h)));
  return { layout, scale };
}
