import { library } from '@fortawesome/fontawesome-svg-core'
import { faCircleInfo, faEdit, faMoon, faSun } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Inkline, components } from '@inkline/inkline'
import '@inkline/inkline/css/index.scss'
import '@inkline/inkline/css/utilities.scss'
import { createApp } from 'vue'

import App from './App.vue'
import './css/variables/index.scss'
import router from './router'
import pinia from './stores'
import './style.css'

library.add(faSun, faMoon, faCircleInfo, faEdit)

createApp(App)
  .use(Inkline, { colorMode: 'system', locale: 'es', components })
  .use(router)
  .use(pinia)
  .component('FontAwesomeIcon', FontAwesomeIcon)
  .mount('#app')
