import { createClock } from './engine/clock.ts';
import { createConfig } from './game/config.ts';
import { Game } from './game/session.ts';
import { localStore } from './game/storage.ts';
import { GreyboxView } from './view/greybox.ts';

export function mountMiniGame(root: HTMLElement) {
  const config = createConfig();
  const game = new Game(config, localStore());
  const view = new GreyboxView(root, game);
  const clock = createClock((dt) => {
    game.update(dt * config.timeScale);
    view.sync();
  });

  // Fuera de vista o con la pestaña oculta, el juego se detiene y no consume recursos.
  // Una partida en curso queda en pausa: al volver, el jugador decide cuándo seguir.
  let visible = false;
  const leave = (reason: string) => {
    game.pause();
    view.sync();
    clock.pause(reason);
  };
  new IntersectionObserver(
    (entries) => {
      visible = entries[entries.length - 1].isIntersecting;
      if (visible) clock.resume('vista');
      else leave('vista');
    },
    { threshold: 0.25 },
  ).observe(root);
  document.addEventListener('visibilitychange', () => (document.hidden ? leave('pestaña') : clock.resume('pestaña')));

  // P o Esc pausan y reanudan mientras la sección está a la vista.
  document.addEventListener('keydown', (event) => {
    if (!visible || !game.playing || event.repeat) return;
    if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return;
    if (event.key !== 'Escape' && event.key.toLowerCase() !== 'p') return;
    event.preventDefault();
    if (game.paused) game.resume();
    else game.pause();
    view.sync();
  });

  if (import.meta.env.DEV || new URLSearchParams(location.search).has('ajustes')) {
    import('./view/debug.ts').then(({ mountDebug }) => mountDebug(game, view));
  }
}
