import Vue from 'vue'
import axios from "axios"

const baseURL = process.env.NODE_ENV === "production" ? "https://prod.kweek.africa/store/" : "http://localhost:8000/store/";


const api = axios.create({
    baseURL,
});


export default new Vue({
    data: {
        id: null,
        product_ids: [],
        total: 0,
        items: []
    },
    watch: {
        id() {
            localStorage.setItem("__kwk-cart__", JSON.stringify({id: this.id, product_ids: this.product_ids}))
        },
        product_ids() {
            localStorage.setItem("__kwk-cart__", JSON.stringify({id: this.id, product_ids: this.product_ids}))
        }
    },
    created() {
      const data =JSON.parse(localStorage.getItem("__kwk-cart__"))  ;
      this.id = data.id;
      this.product_ids = data.product_ids;
      if (this.id) {
          api.get(`/cart/${this.id}`).then(res => {
              this.items = res.data.items;
              this.total = res.data.total;
          });
      }
    },
    methods: {
        addToCart(product_id, quantity) {
            this.product_ids.push({product_id, quantity});
            if (!this.id) {
                return api.post("/cart/", {cart_items: JSON.parse(JSON.stringify(this.product_ids))}).then(res => {
                    this.id = res.data.uid;
                    this.items = res.data.items;
                    this.total = res.data.total;
                })
            } else {
                return api.put(`/cart/${this.id}/`, {id: this.id, cart_items: JSON.parse(JSON.stringify(this.product_ids))}).then(res => {
                    this.items = res.data.items;
                    this.total = res.data.total;
                })
            }
        }
    }
})
