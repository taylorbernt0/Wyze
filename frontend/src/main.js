import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import PrimeVue from 'primevue/config';

Vue.config.productionTip = false;

Vue.use(PrimeVue);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
