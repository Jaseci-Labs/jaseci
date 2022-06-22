import { Config } from '@stencil/core';
import tailwind, { tailwindHMR } from 'stencil-tailwind-plugin';

export const config: Config = {
  namespace: 'components',
  devServer: { reloadStrategy: 'hmr' },
  globalStyle: 'src/global/global.css',
  outputTargets: [
    {
      type: 'dist',
      esmLoaderPath: '../loader',
    },
    {
      type: 'dist-custom-elements',
    },
    {
      type: 'docs-readme',
    },
    {
      type: 'www',
      serviceWorker: null, // disable service workers
      baseUrl: 'http://localhost:3333',
    },
  ],
  plugins: [
    tailwind({
      tailwindConf: {
        plugins: [require('@tailwindcss/typography'), require('daisyui')],
      },
    }),
    tailwindHMR(),
  ],
};
