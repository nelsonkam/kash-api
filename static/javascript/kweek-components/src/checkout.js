import Vue from 'vue'
import api from "@/api";
import cart from './cart';
export default new Vue({
    data: {
        id: null,
        info: {},
        errors: {},
        loading: false
    },
    created() {
        this.info = JSON.parse(localStorage.getItem("__kwk-checkout__")) || {
            name: '',
            contact: '',
            country: '',
            city: '',
            address: '',
            payment_mode: 'card',
        };
    },
    methods: {
        createCheckout: function () {
            this.loading = true;
            const errors = {};
            const checkout = JSON.parse(JSON.stringify(this.info));
            Object.keys(checkout).forEach(key => {
                if (!checkout[key]) {
                    errors[key] = "Ce champs est requis";
                }
            });
            if (Object.keys(errors).length > 0) {
                this.errors = errors;
                this.loading = false;
                return Promise.reject(errors)
            } else {
                return api.post("/checkout/", {...checkout, cart_uid: cart.id}).then(res => {
                    localStorage.setItem("__kwk-checkout__", JSON.stringify(checkout));
                    this.id = res.data.uid;
                }).finally(_ => {
                    this.loading = false;
                })
            }
        }
    }
})
