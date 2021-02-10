import Vue from 'vue'
import App from './App'
import vueCountryRegionSelect from 'vue-country-region-select'
Vue.config.productionTip = false
Vue.config.ignoredElements = [/^sl-/];
Vue.use(vueCountryRegionSelect)
new Vue({
  render: h => h(App),
}).$mount('#app')


