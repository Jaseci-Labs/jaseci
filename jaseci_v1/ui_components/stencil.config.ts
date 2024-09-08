import { Config } from '@stencil/core';
import tailwind, { tailwindHMR } from 'stencil-tailwind-plugin';
import { blue, blueDark, plumDark, violetDark, slateDark, indigoDark, yellowDark, redDark, grassDark, slate, indigo, grass, yellow, red, plum, violet } from '@radix-ui/colors';

// @ts-ignore
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
      type: 'dist',
      esmLoaderPath: '../loader',
      buildDir: '../../jaseci_ui_kit/jaseci_ui_kit/static/build',
    },
    {
      type: 'dist',
      esmLoaderPath: '../loader',
      buildDir: '../../jaseci_studio/public/ui_kit',
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
        content: [],
        plugins: [require('@tailwindcss/typography'), require('daisyui')],
        daisyui: {
          styled: true,
          base: true,
          utils: true,
          logs: true,
          rtl: false,
          prefix: '',
          darkTheme: 'dark',
          themes: [
            'corporate',
            'garden',
            'pastel',
            {
              greenheart: {
                // green9
                'primary': '#30A46C',
                'secondary': '#F5D90A',
                'accent': '#92CEAC',
                'neutral': '#18794E',
                'base-100': '#FBFDFC',
                'base-200': '#F8FAF9',
                'info': '#68DDFD',
                'success': '#70E1C8',
                'warning': '#F76808',
                'error': '#E93D82',
                // green3
                'neutral-content': '#E9F9EE',
                '--card-border': '#D7DCDA',
              },
              nexus: {
                // blue9
                'primary': '#0090FF',
                // plum9
                'secondary': '#AB4ABA',
                // violet9
                'accent': '#3451B2',
                // blue11
                'neutral': '#006ADC',
                // slate1
                'base-100': '#FBFCFD',
                // slate2
                'base-200': '#F8F9FA',
                // indigo9
                'info': '#3E63DD',
                // grass9
                'success': '#46A758',
                // yellow9
                'warning': '#F5D90A',
                // red9
                'error': '#E5484D',
                // blue3
                'neutral-content': '#EDF6FF',
                // slate7
                '--card-border': '#D7DBDF',
              },
              slate: {
                // blue9
                'primary': slate.slate9,
                // plum9
                'secondary': plum.plum9,
                // violet9
                'accent': violet.violet9,
                // blue11
                'neutral': slate.slate11,
                // slate1
                'base-100': blue.blue1,
                // slate2
                'base-200': blue.blue2,
                // indigo9
                'info': indigo.indigo9,
                // grass9
                'success': grass.grass9,
                // yellow9
                'warning': yellow.yellow9,
                // red9
                'error': red.red9,
                // slate3
                'neutral-content': slate.slate3,
                // slate3
                'primary-content': slate.slate3,
                // slate7
                '--card-border': blue.blue7,
              },
              slateDark: {
                // blue9
                'primary': slateDark.slate9,
                // plum9
                'secondary': plumDark.plum9,
                // violet9
                'accent': violetDark.violet9,
                // blue11
                'neutral': slateDark.slate11,
                // slate1
                'base-100': blueDark.blue1,
                // slate2
                'base-200': blueDark.blue2,
                // indigo9
                'info': indigoDark.indigo9,
                // grass9
                'success': grassDark.grass9,
                // yellow9
                'warning': yellowDark.yellow9,
                // red9
                'error': redDark.red9,
                // slate3
                'neutral-content': slateDark.slate3,
                // slate3
                'primary-content': slateDark.slate3,
                // slate7
                '--card-border': blueDark.blue7,
              },
              nexusDark: {
                // blue9
                'primary': blueDark.blue9,
                // plum9
                //
                'secondary': plumDark.plum9,
                // violet9
                'accent': violetDark.violet9,
                // blue11
                'neutral': blueDark.blue11,
                // slate1
                'base-100': slateDark.slate1,
                // slate2
                'base-200': slateDark.slate2,
                // indigo9
                'info': indigoDark.indigo9,
                // grass9
                'success': grassDark.grass9,
                // yellow9
                'warning': yellowDark.yellow9,
                // red9
                'error': redDark.red9,
                // blue3
                'neutral-content': blueDark.blue3,
                // slate7
                '--card-border': slateDark.slate7,
              },
            },
          ],
        },
      },
    }),
    tailwindHMR(),
  ],
};
