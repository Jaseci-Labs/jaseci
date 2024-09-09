/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{ts,tsx,html}'],
  theme: {
    extend: {},
  },
  daisyui: {
    themes: [
      {
        grass: {
          'primary': '#30A46C',
          'secondary': '#F5D90A',
          'accent': '#92CEAC',
          'neutral': '#18794E',
          'base-100': '#FBFEFC',
          'info': '#68DDFD',
          'success': '#70E1C8',
          'warning': '#F76808',
          'error': '#E93D82',
        },
      },
    ],
  },
  plugins: [require('@tailwindcss/typography'), require('daisyui')],
};
