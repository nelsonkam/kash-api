import Vue from 'vue'
import App from './App'
Vue.config.productionTip = false
Vue.config.ignoredElements = [/^sl-/];

new Vue({
  render: h => h(App),
}).$mount('#app')


