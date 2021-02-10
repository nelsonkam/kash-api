<template>
  <div style="padding-top: 52px; padding-bottom: 125px;">
    <div style="padding: 16px">
      <div style="border: 1px #e5e7eb solid; border-radius: 4px;">
        <div
            style="display: flex; padding: 12px 16px; align-items:center;justify-content:space-between; border-bottom: 1px #e5e7eb solid;">
          <p style="font-size: 16px; margin: 0; font-family: inherit; color: #828282;">Nom</p>
          <p style="font-size: 16px; margin: 0; font-family: inherit;">{{ checkout.info.name }}</p>
        </div>
        <div
            style="display: flex; padding: 12px 16px; align-items:center;justify-content:space-between; border-bottom: 1px #e5e7eb solid;">
          <p style="font-size: 16px; margin: 0; font-family: inherit; color: #828282;">Contact</p>
          <p style="font-size: 16px; margin: 0; font-family: inherit;">{{ checkout.info.contact }}</p>
        </div>
        <div
            style="display: flex; padding: 12px 16px; align-items:center;justify-content:space-between; border-bottom: 1px #e5e7eb solid;">
          <p style="font-size: 16px; margin: 0; font-family: inherit; color: #828282;">Pays/Ville</p>
          <p style="font-size: 16px; margin: 0; font-family: inherit;">{{ checkout.info.city }},
            {{ checkout.info.country }}</p>
        </div>
        <div
            style="display: flex; padding: 12px 16px; align-items:center;justify-content:space-between; border-bottom: 1px #e5e7eb solid;">
          <p style="font-size: 16px; margin: 0; font-family: inherit; color: #828282;">Adresse</p>
          <p style="font-size: 16px; margin: 0; font-family: inherit;">{{ checkout.info.address }}</p>
        </div>
        <div
            style="display: flex; padding: 12px 16px; align-items:center;justify-content:space-between; border-bottom: 1px #e5e7eb solid;">
          <p style="font-size: 16px; margin: 0; font-family: inherit; color: #828282;">Mode de paiement</p>
          <p style="font-size: 16px; margin: 0; font-family: inherit;">{{ paymentMethod }}</p>
        </div>
        <button
            @click="$emit('back')"
            class="edit-btn">
          Modifier ces informations
        </button>
      </div>
      <p class="section-title">Option de livraison</p>
      <div style="display:flex; flex-direction: column;">
        <shipping-method @click="selectedOptionIndex = index" :key="index" v-for="(option, index) in options"
                         :name="option.name" :eta="option.eta"
                         :price="option.price.amount" :logo="option.logo"
                         :active="selectedOptionIndex === index"></shipping-method>
      </div>
      <div class="panel-footer">
        <div
            style="display:flex; align-items: center; justify-content: space-between; padding: 0px 12px;">
          <p style="font-family: inherit; font-size: 16px">Total à payer</p>
          <p style="font-family: inherit; font-weight: bold; font-size: 16px">{{ shippingFee }} XOF</p>
        </div>
        <div style="padding: 0px 12px 16px;">
          <button class="button">
            <loading v-if="checkout.loading"></loading>
            <span v-else>Payer votre commande</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import checkout from "@/checkout";
import api from "@/api";
import cart from '../cart';
import ShippingMethod from "./ShippingMethod"

export default {
  name: "Shipping",
  data() {
    return {checkout, options: [], selectedOptionIndex: 0, cart}
  },
  components: {
    ShippingMethod
  },
  computed: {
    paymentMethod() {
      const map = {
        card: "Carte bancaire",
        momo: "Mobile money",
        cash: "Paiement à la livraison"
      }
      return map[this.checkout.info.payment_mode]
    },
    shippingFee() {
      const option = this.options[this.selectedOptionIndex] || {price: {amount: 0}};
      return this.cart.total + option.price.amount
    }
  },
  created() {
    api.get(`/checkout/${checkout.id}/shipping/`).then(res => {
      this.options = res.data;
    })
  }
}
</script>

<style scoped>
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.button {
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
  width: 100%;
}


.panel-footer {
  position: fixed;
  bottom: 0;
  right: 0;
  width: 520px;
  max-width: 100vw;
  background-color: white;
  border-top: 1px rgb(196, 196, 196) solid;
}

.edit-btn {
  display: flex;
  padding: 12px 16px;
  align-items: center;
  justify-content: center;
  background-color: black;
  color: white;
  border-bottom-right-radius: 4px;
  border-bottom-left-radius: 4px;
  font-weight: bold;
  border: none;
  width: 100%;
  font-size: 16px;
  font-family: inherit;
}

.section-title {
  font-size: 1.3rem;
  color: #828282;
  font-weight: 500;
  margin: 20px 0 8px;
}
</style>
