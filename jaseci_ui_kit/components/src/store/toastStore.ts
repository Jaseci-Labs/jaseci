import { createStore } from '@stencil/store';

export const toastStore = createStore({
  hidden: true,
  config: {
    message: 'Hey there!',
    timeout: 2000,
  },
});
