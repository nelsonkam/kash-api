import Vue from 'vue'
import App from './App'
import kkiapay from "kkiapay"
import vueCountryRegionSelect from 'vue-country-region-select'
Vue.use(vueCountryRegionSelect)
Vue.config.productionTip = false
Vue.config.ignoredElements = [/^sl-/];
new Vue({
  render: h => h(App),
}).$mount('#app')


window.pay = () => {
  const k = kkiapay("e586fb90ee0411ea8d5dd1fcfc73e3a8")
  k.debit("22998801811", 100).then(res => {
    console.log(res)
  }).catch(err => {
    console.log(err)
  })
}
