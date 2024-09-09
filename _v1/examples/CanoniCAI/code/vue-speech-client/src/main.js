import { createApp } from 'vue'
import jaseci from './jaseci-api'

import App from './App.vue'

import './assets/main.css'

createApp(App)
  .mixin(jaseci).mount('#app')
