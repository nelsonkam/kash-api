<template>
  <div style="display: flex; align-items:center;justify-content:center; flex: 1; height: 100%">
    <div v-if="status === 'success'" style="display:flex; flex-direction: column; align-items:center;">
      <div>
        <svg
            width="64"
            height="64"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
          <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M12 23C5.92487 23 1 18.0751 1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23ZM12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21ZM15.2929 8.29289L10 13.5858L7.70711 11.2929L6.29289 12.7071L10 16.4142L16.7071 9.70711L15.2929 8.29289Z"
              fill="green"
          />
        </svg>
      </div>
      <p style="color: #828282; text-transform:uppercase;font-size: 18px; margin-top: 16px; margin-bottom: 8px;">
        Nº {{ checkout.reference }}
      </p>
      <p style="font-weight: bold; font-size: 24px; margin-top: 4px; margin-bottom: 8px;">Commande confirmée</p>
      <p style="color: #828282; text-align: center; max-width: 350px;font-size: 16px">
        Nous vous tiendrons informer du statut de votre commande par SMS ou
        e-mail. Pour référence, veuillez noter le numéro de commande:
        <span class="font-bold text-black"
              style="font-weight: bold; color: black; font-family: inherit;font-size: 16px">
            {{ checkout.reference }}
          </span>
      </p>
      <button @click="navigateHome" class="button" style="margin-top: 16px">Retourner à la page d'accueil</button>
    </div>
    <div v-if="status === 'failure'" style="display:flex; flex-direction: column; align-items:center;">
      <div>
        <svg
            width="64"
            height="64"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
          <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M12 23C5.92487 23 1 18.0751 1 12C1 5.92487 5.92487 1 12 1C18.0751 1 23 5.92487 23 12C23 18.0751 18.0751 23 12 23ZM12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21ZM8.70711 16.7071L12 13.4142L15.2929 16.7071L16.7071 15.2929L13.4142 12L16.7071 8.70711L15.2929 7.29289L12 10.5858L8.70711 7.29289L7.29289 8.70711L10.5858 12L7.29289 15.2929L8.70711 16.7071Z"
              fill="red"
          />
        </svg>
      </div>
      <p style="font-weight: bold; font-size: 24px; margin-top: 4px; margin-bottom: 8px;">Commande annulée</p>
      <p style="color: #828282; text-align: center; max-width: 350px;font-size: 16px;">
        Votre commande n'a pas été prise en compte en raison d'un échec lors du paiement de votre commande.
      </p>
      <button @click="$emit('back')" class="button" style="margin-top: 16px">Réessayer</button>
    </div>
    <loading v-if="loading" />
  </div>
</template>

<script>
import checkout from "@/checkout";
import Loading from "@/internal/Loading";
import api from "@/api";
export default {
  name: "OrderCompleted",
  data() {
    return {
      checkout,
      loading: false,
      status: null
    }
  },
  components: {
    Loading
  },
  mounted() {
    this.loading = true;
    api.get(`/checkout/${this.checkout.id}/`).then(res => {
      this.loading = false;
      this.status = res.data.paid ? 'success' : 'failure';
    })
  },
  methods: {
    navigateHome() {
      window.location.href = "/";
    }
  }
}
</script>

<style scoped>

</style>
