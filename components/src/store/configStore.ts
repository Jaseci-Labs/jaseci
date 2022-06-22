import { createStore } from '@stencil/store';

export const configStore = createStore({
  config: {
    theme: 'winter',
    css: {},
  },
});

export const getTheme = () => {
  return configStore.state.config.theme;
};
