// Almacenamiento del récord, del tutorial y de las pistas vistas. Si localStorage no está
// disponible (navegación privada, previsualizaciones), el juego sigue funcionando sin guardar.

export interface Store {
  get<T>(key: string, fallback: T): T;
  set(key: string, value: unknown): void;
}

export function localStore(prefix = 'hamburguesas:'): Store {
  return {
    get(key, fallback) {
      try {
        const raw = localStorage.getItem(prefix + key);
        return raw === null ? fallback : JSON.parse(raw);
      } catch {
        return fallback;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(prefix + key, JSON.stringify(value));
      } catch {
        // Sin almacenamiento: se pierde el dato, no la partida.
      }
    },
  };
}

export function memoryStore(): Store {
  const data = new Map<string, unknown>();
  return {
    get: (key, fallback) => (data.has(key) ? (data.get(key) as typeof fallback) : fallback),
    set: (key, value) => void data.set(key, value),
  };
}
