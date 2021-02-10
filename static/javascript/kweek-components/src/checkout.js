import Vue from 'vue'
import api from "@/api";
import cart from './cart';
import kkiapay from "kkiapay"
import {KKIAPAY_API_KEY} from "@/constants";
export default new Vue({
    data: {
        id: null,
        reference: null,
        info: {},
        errors: {},
        loading: false,
        payment: {
            method: 'card',
            payload: null
        },
        shipping: null,
        paying: false
    },
    created() {
        this.info = JSON.parse(localStorage.getItem("__kwk-checkout__")) || {
            name: '',
            contact: '',
            country: '',
            city: '',
            address: '',
        };
    },
    methods: {
        createCheckout() {
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
                    this.reference = res.data.ref_id;
                }).finally(_ => {
                    this.loading = false;
                })
            }
        },
        tokenCreated(token) {
            this.paying = true;
            this.payment.payload = token;
            this.payRequest();
        },
        payRequest() {
            const payment = JSON.parse(JSON.stringify(this.payment));
            const shipping = JSON.parse(JSON.stringify(this.shipping));
            return api.post(`/checkout/${this.id}/pay/`, {payment,shipping}).then(res => {
                this.paying = false;
                this.$emit("checkout:payment:success");
            }).catch(_ => {
                this.paying = false;
                this.$emit("checkout:payment:failure");
            })
        },
        payWithCard(shippingOption, cardRef) {
            this.shipping = shippingOption;
            cardRef.submit();
        },
        payWithMomo(shippingOption) {
            this.paying = true;
            this.shipping = shippingOption;
            const k = kkiapay(KKIAPAY_API_KEY);
            const total = cart.total + this.shipping.price.amount;
            k.debit(`229${this.payment.payload}`, total).then(res => {
                this.paying = false;
                this.payment.method = res.transactionId;
                return this.payRequest();
            }).catch(err => {
                this.paying = false;
                this.$emit("checkout:payment:failure");
            })
        },
        payWithCash(shippingOption) {
            this.paying = true;
            this.shipping = shippingOption;
            return this.payRequest();
        }
    }
})
