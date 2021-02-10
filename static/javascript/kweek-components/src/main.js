import Vue from 'vue'
import CartBtn from './components/CartBtn.vue'
import CartPane from './components/CartPane.vue'
import vueCountryRegionSelect from 'vue-country-region-select'
Vue.config.ignoredElements = [/^sl-/];
Vue.use(vueCountryRegionSelect)
export default {
  CartBtn,
  CartPane
}
