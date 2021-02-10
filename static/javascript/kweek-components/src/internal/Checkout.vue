<template>
  <div style="padding-top: 52px; padding-bottom: 125px;">
    <div
        style="background-color: black; color: white; padding: 0 16px; text-align: center; display:flex; align-items:center; justify-content:space-between;">
      <p style="color: white; font-size: 16px;">Sous total du panier</p>
      <p style="color: white; font-size: 16px; font-weight: bold;">{{ cart.total }} XOF</p>
    </div>
    <div style="padding: 0px 16px 0;">
      <p class="section-title">Vos coordonnées</p>
      <div style="display:flex; flex-direction: column;">
        <k-input :error="checkout.errors.name" v-model="checkout.info.name" type="text" placeholder="Nom et prénoms"/>
        <k-input :error="checkout.errors.contact" v-model="checkout.info.contact" type="text"
                 placeholder="Numéro de téléphone ou e-mail"/>
      </div>
      <p class="section-title">Adresse de livraison</p>
      <div style="display:flex; flex-direction: column;">
        <div class="input-container">
          <country-select placeholder="Choisissez un pays" className="input" v-model="checkout.info.country"
                          :country="checkout.info.country" topCountry="US"/>
          <p v-if="checkout.errors.country" style="margin: 4px 0 0; color: red; font-size: 14px; font-family: inherit;">
            {{ checkout.errors.country }}</p>
        </div>
        <k-input v-model="checkout.info.city" :error="checkout.errors.city" type="text" placeholder="Ville"/>
        <k-input v-model="checkout.info.address" :error="checkout.errors.address" type="text"
                 placeholder="Adresse de livraison"/>
      </div>
      <p class="section-title">Mode de paiement</p>
      <div style="display:flex; flex-direction: column;">
        <payment-method @click="checkout.info.payment_mode = 'card'" :active="checkout.info.payment_mode === 'card'"
                        name="Carte bancaire"></payment-method>
        <payment-method @click="checkout.info.payment_mode = 'momo'" :active="checkout.info.payment_mode === 'momo'"
                        name="Mobile Money"></payment-method>
        <payment-method @click="checkout.info.payment_mode = 'cash'" :active="checkout.info.payment_mode === 'cash'"
                        name="Paiement à la livraison"></payment-method>
      </div>
      <div class="panel-footer">
        <div
            style="display:flex; align-items: center; justify-content: space-between; padding: 0px 12px;">
          <p style="font-family: inherit; font-size: 16px">Sous total</p>
          <p style="font-family: inherit; font-weight: bold; font-size: 16px">{{ cart.total }} XOF</p>
        </div>
        <div style="padding: 0px 12px 16px;">
          <button @click="next" class="button">
            <loading v-if="checkout.loading"></loading>
            <span v-else>Payer votre commande</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PaymentMethod from "@/internal/PaymentMethod";
import KInput from "@/internal/KInput";
import cart from '../cart';
import checkout from '../checkout';
import Loading from "./Loading";

export default {
  name: "Checkout",
  data() {
    return {
      checkout,
      errors: {},
      cart
    }
  },
  components: {
    PaymentMethod, KInput, Loading
  },
  methods: {
    next() {
      this.checkout.createCheckout().then(() => {
        this.$emit("next");
      })
    }
  }
}
</script>

<style scoped>

.panel-footer {
  position: fixed;
  bottom: 0;
  right: 0;
  width: 520px;
  max-width: 100vw;
  background-color: white;
  border-top: 1px rgb(196, 196, 196) solid;
}

.section-title {
  font-size: 1.3rem;
  color: #828282;
  font-weight: 500;
  margin: 20px 0 8px;
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

.input {
  appearance: none;
  border: 1px #e5e7eb solid;
  border-radius: 4px;
  padding: 10px 12px;
  font-size: 16px;
}

.input-container {
  margin: 8px 0;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>
