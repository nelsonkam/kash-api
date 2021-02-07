Vue.config.ignoredElements = [/^sl-/];
var app = new Vue({
    el: "#content",
    delimeters: ["[[", "]]"],
    data: {
        cartOpen: false
    },
    methods: {
        toggleCart() {
            const drawer = document.querySelector('kweek-cart-pane');
            console.log(document.querySelector('kweek-cart-pane'));
            drawer.vueComponent.show()
        }
    }
})
