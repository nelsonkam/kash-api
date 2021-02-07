<template>
  <div>
    <cart-btn product-id="238" />
    <button id="opener">Open cart</button>
  <cart-pane trigger="#opener" />
  </div>
</template>

<script>
import CartBtn from './components/CartBtn.vue'
import CartPane from './components/CartPane.vue'
export default {
  name: "App.vue",
  components: {CartBtn, CartPane}
}
</script>

<style scoped>

</style>
