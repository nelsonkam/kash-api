<template>
  <div v-show="open" class="pane-container">
    <div class="overlay"></div>
    <transition name="slide">
      <div v-show="open" class="pane">
        <div style="padding: 0; height: 100%">
          <div class="pane-header-container">
            <div class="pane-header">
              <div style="display:flex; align-items:center;">
                <button v-if="currentStep > 0 && currentStep < 3" @click="currentStep--" style="padding: 4px; margin-right: 8px;background: none;border: none;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M6.41424 13L12.7071 19.2929L11.2929 20.7071L2.58582 12L11.2929 3.29291L12.7071 4.70712L6.41424 11H21V13H6.41424Z" fill="black"></path></svg></button>
                <p style="font-family: inherit; font-size: 20px; font-weight: 600; margin: 0;">{{ title }}</p>
              </div>
              <button @click="open = false" style="appearance: none; border: none; padding: 4px; background: none;">
                <svg style="width: 24px; height: 24px" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                     fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                  <path
                      d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"></path>
                </svg>
              </button>
            </div>
          </div>
          <cart @next="currentStep++" v-if="currentStep === 0" />
          <checkout @next="currentStep++" v-if="currentStep === 1" />
          <shipping @back="currentStep--" @next="currentStep++" v-if="currentStep === 2" />
          <order-completed @back="currentStep--" v-if="currentStep === 3" />
        </div>
      </div>

    </transition>
  </div>
</template>

<script>
import cart from '../cart'
import Cart from "../internal/Cart"
import Checkout from "../internal/Checkout"
import Shipping from "../internal/Shipping"
import OrderCompleted from "../internal/OrderCompleted"
export default {
  props: ['trigger'],
  data() {
    return {
      open: false,
      cart,
      currentStep: 0,
    }
  },
  components: {
    Cart, Checkout, Shipping, OrderCompleted
  },
  computed: {
    title() {
      const titles = ["Votre panier","Ma commande","Livraison & Paiement", "Confirmation"]
      return titles[this.currentStep];
    }
  },
  mounted() {
    document.querySelector(this.trigger).addEventListener("click", () => {
      this.open = true;
    });
  },
  methods: {
    show() {
      this.open = true;
    }
  }
}
</script>

<style scoped>
.pane-container {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  width: 100vw;
  height: 100vh;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  background-color: black;
  opacity: .3;
  width: 100vw;
  height: 100vh;
}

.pane {
  position: absolute;
  top: 0;
  right: 0;
  background-color: white;
  height: 100vh;
  overflow: scroll;
  width: 520px;
  max-width: 100vw;
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

.pane-open {
  transform: translate(0px, 0px);
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

.pane-header-container {
  position: fixed;
  width: 520px;
  max-width: 100vw;
}

.pane-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0px 8px 12px;
  border-bottom: 1px rgb(196, 196, 196) solid;
  background-color: white;
}

.slide-enter-active, .slide-leave-active {
  transition: transform .2s ease;
}

.slide-enter, .slide-leave-to {
  transform: translate(100%, 0px);
}

.slide-leave, .slide-enter-to {
  transform: translate(0px, 0px);
}


</style>
