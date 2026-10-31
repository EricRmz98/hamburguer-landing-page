// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// Páginas solo para desarrollo: existen con `astro dev` y no entran en la compilación.
const paginasDeDesarrollo = {
  name: 'paginas-de-desarrollo',
  hooks: {
    /** @param {{ command: string, injectRoute: (route: { pattern: string, entrypoint: string }) => void }} options */
    'astro:config:setup': ({ command, injectRoute }) => {
      if (command === 'dev') injectRoute({ pattern: '/sprites', entrypoint: './src/dev/sprites.astro' });
    },
  },
};

// https://astro.build/config
export default defineConfig({
  integrations: [paginasDeDesarrollo],
  vite: {
    plugins: [tailwindcss()]
  }
});
