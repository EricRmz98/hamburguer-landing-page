// Valores ajustables del juego. Son los valores iniciales propuestos en el plan;
// el panel de ajuste los modifica en vivo para encontrar los definitivos.

export interface LevelStep {
  upTo: number; // último cliente (en el modo infinito) al que aplica
  tier: number; // tipo de recetas (ver generateRecipe)
  slots: number; // lugares de la plancha
}

export const DEFAULT_CONFIG = {
  timeScale: 1,
  grill: {
    cookTime: 3, // segundos hasta «perfecta»
    rawFraction: 0.4, // parte de cookTime que se ve cruda antes de «cocinándose»
    // Lista durante 2 s en total: perfecta y, al final, el aviso parpadeando; después se quema.
    perfectWindow: 1.2,
    warnTime: 0.8,
    maxSlots: 4,
  },
  lives: 3,
  wrongPenalty: 2, // segundos de paciencia que cuesta un ingrediente equivocado
  betweenCustomers: 0.9,
  maxStackHeight: 100,
  // La dificultad es el tiempo: paciencia = tiempo mínimo posible de la orden × holgura.
  // La holgura baja con cada cliente hasta su mínimo; desde ahí, pura habilidad.
  patience: {
    tapTime: 0.4, // segundos por toque al calcular el tiempo mínimo
    slackStart: 4.5,
    slackGrace: 2, // clientes del inicio con la holgura inicial completa
    slackStep: 0.2,
    slackMin: 1.5,
    scale: 1, // multiplicador global para pruebas
  },
  levels: [
    { upTo: 2, tier: 1, slots: 2 },
    { upTo: 5, tier: 2, slots: 2 },
    { upTo: 9, tier: 3, slots: 3 },
    { upTo: 14, tier: 4, slots: 4 },
  ] as LevelStep[],
  endless: { tier: 5, slots: 4 },
};

export type GameConfig = typeof DEFAULT_CONFIG;
export type GrillConfig = GameConfig['grill'];

export function createConfig(): GameConfig {
  return structuredClone(DEFAULT_CONFIG);
}
