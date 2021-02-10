<template>
  <div id="container">
    <div id="qty-container">
      <p id="label" style="margin-right: 12px">Quantité</p>
      <div id="counter">
        <button @click="quantity = quantity > 1 ? quantity - 1 : 1" class="counter-btn" id="decrement">-</button>
        <div id="value" style="margin: 0 8px; font-size: 18px;">{{quantity}}</div>
        <button @click="quantity++" class="counter-btn" id="increment">+</button>
      </div>
    </div>
    <div>
      <button @click="addToCart" id="add-to-cart">
      <loading v-if="loading"></loading>
        <span v-else>Ajouter au panier</span>
      </button>
    </div>
  </div>
</template>

<script>
import cart from "../cart";
import Loading from "../internal/Loading"
export default {
  props: ['productId'],
  data() {
    return {
      quantity: 1,
      loading: false
    }
  },
  components: {
    Loading
  },
  created() {
    console.log(this.productId)
  },
  methods: {
    addToCart() {
      this.loading = true
      cart.addToCart(this.productId, this.quantity).finally(() => {
        this.loading = false;
      })
    }
  }
}
</script>

<style>
#container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}
#qty-container {
  display: flex;
  align-items: center;
}
#label {
  font-size: 18px;
  font-weight: 500;
  font-family: inherit;
}
#counter {
  display: flex;
  align-items: center;
}
.counter-btn {
  appearance: none;
  background-color: black;
  color: white;
  border-radius: 100%;
  height: 28px;
  width: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  outline: none;
  border: none;
}

#add-to-cart {
  appearance: none;
  background-color: black;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  border: none;
  font-weight: 600;
  font-size: 16px;
  font-family: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 150px;
}
</style>
