<template>
  <div style="padding-top: 52px; padding-bottom: 125px;">
    <div
        style="background-color: black; color: white; padding: 0 16px; text-align: center; display:flex; align-items:center; justify-content:space-between;">
      <p style="color: white; font-size: 16px;">Sous total du panier</p>
      <p style="color: white; font-size: 16px; font-weight: bold;">{{ cart.total }} XOF</p>
    </div>
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
      <p class="section-title">Mode de paiement</p>
      <div style="display:flex; flex-direction: column;">
        <payment-method @click="checkout.payment.method = 'card'; checkout.payment.payload = null;" :active="checkout.payment.method === 'card'"
                        name="Carte bancaire">
          <div style="margin-top: 16px">
            <stripe-element-card ref="cardRef" @token="checkout.tokenCreated" :hidePostalCode="true" :pk="stripePK" />
          </div>
        </payment-method>
        <payment-method @click="checkout.payment.method = 'momo'; checkout.payment.payload = null;" :active="checkout.payment.method === 'momo'"
                        name="Mobile Money (MTN/Moov)">
          <div style="margin-top: 16px">
            <div class="momo-input">
              <p class="prefix">+229</p>
              <input v-model="checkout.payment.payload" class="phone" placeholder="Numéro Momo/Flooz" type="tel" maxlength="8" />
            </div>
          </div>
        </payment-method>
        <payment-method @click="checkout.payment.method = 'cash'; checkout.payment.payload = null;" :active="checkout.payment.method === 'cash'"
                        name="Paiement à la livraison"></payment-method>
      </div>
      <div class="panel-footer">
        <div
            style="display:flex; align-items: center; justify-content: space-between; padding: 0px 12px;">
          <p style="font-family: inherit; font-size: 16px">Total à payer</p>
          <p style="font-family: inherit; font-weight: bold; font-size: 16px">{{ shippingFee }} XOF</p>
        </div>
        <div style="padding: 0px 12px 16px;">
          <button @click="pay" class="button">
            <loading v-if="checkout.paying"></loading>
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
import PaymentMethod from "./PaymentMethod"
import Loading from "./Loading"
import { StripeElementCard } from '@vue-stripe/vue-stripe';
import {STRIPE_PUBLIC_KEY} from "@/constants";

export default {
  name: "Shipping",
  data() {
    return {
      checkout,
      options: [],
      selectedOptionIndex: 0,
      cart,
      stripePK: STRIPE_PUBLIC_KEY,
    }
  },
  components: {
    ShippingMethod, PaymentMethod, StripeElementCard, Loading
  },
  computed: {

    shippingFee() {
      const option = this.options[this.selectedOptionIndex] || {price: {amount: 0}};
      return this.cart.total + option.price.amount
    }
  },
  created() {
    api.get(`/checkout/${checkout.id}/shipping/`).then(res => {
      this.options = res.data;
    });
    this.checkout.$on("checkout:payment:success", () => {
      this.cart.empty();
      this.$emit("next");
    });
    this.checkout.$on("checkout:payment:failure", () => {
      this.$emit("next");
    });
  },
  methods: {
    pay() {
      if (this.checkout.payment.method === 'card') {
        this.checkout.payWithCard(this.options[this.selectedOptionIndex], this.$refs.cardRef)
      } else if (this.checkout.payment.method === 'momo') {
        this.checkout.payWithMomo(this.options[this.selectedOptionIndex])
      } else if (this.checkout.payment.method === 'cash') {
        this.checkout.payWithCash(this.options[this.selectedOptionIndex])
      }
    }
  }
}
</script>

<style>
.momo-input {
    box-sizing: border-box;
    height: 40px;
    padding: 10px 12px;
    border: 1px solid transparent;
    border-radius: 4px;
    background-color: white;
    box-shadow: 0 1px 3px 0 #e6ebf1;
    -webkit-transition: box-shadow 150ms ease;
    transition: box-shadow 150ms ease;
    display: flex;
    align-items: center;
}
.momo-input .prefix {
  color: #828282;
  font-family: sans-serif;
  padding: 0 8px 0 4px;
}

#stripe-element-form {
  height: 48px;
}

.momo-input .phone {
  border: none;
  appearance: none;
  font-size: 16px;
  padding: 4px 8px;
  outline: none;
  color: #32325d;
}

.momo-input .phone::placeholder {
  color: #bbbbc2;
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
