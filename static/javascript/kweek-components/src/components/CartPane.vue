<template>
  <div v-show="open" class="pane-container">
    <div class="overlay"></div>
    <transition name="slide">
      <div v-show="open" class="pane">
        <div style="padding: 0; height: 100%">
          <div class="pane-header-container">
            <div class="pane-header">
              <p style="font-family: inherit; font-size: 20px; font-weight: 600; margin: 0;">Votre panier</p>
              <button @click="open = false" style="appearance: none; border: none; padding: 4px; background: none;">
                <svg style="width: 24px; height: 24px" xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                     fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                  <path
                      d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"></path>
                </svg>
              </button>
            </div>
          </div>
          <div v-if="!cart.id" style="display:flex; justify-content: center; align-items: center; height: 100%;">
            <p style="color: #4444; text-align: center; font-family: inherit; font-size: 16px; font-weight: 600;">Les
              produits que vous ajouterez à votre panier s'afficheront ici.</p>
          </div>
          <div v-else>
            <div style="padding-top: 54px;">
              <div v-for="item in cart.items"
                   style="display:flex; align-items: center; border-bottom: 1px #e5e7eb solid; padding: 12px 16px;">
                <img :src="item.product.images[0].url"
                     style="height: 64px; width: 64px; background-color: #4444; border-radius: 6px;" alt="">
                <div style="padding-left: 16px">
                  <p style="font-size: 16px; font-family: inherit; margin: 6px 0; font-weight: 600">{{
                      item.product.name
                    }}</p>
                  <p style="margin:12px 0;">{{ item.product.price }} {{ item.product.currency_iso }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </transition>
  </div>
</template>

<script>
import cart from '../cart'

export default {
  props: ['trigger'],
  data() {
    return {
      open: false,
      cart
    }
  },
  mounted() {
    document.querySelector(this.trigger).addEventListener("click", () => {
      this.open = true;
    })
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

.pane-open {
  transform: translate(0px, 0px);
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
