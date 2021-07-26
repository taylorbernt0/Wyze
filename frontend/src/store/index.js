import Vue from "vue";
import Vuex from "vuex";
import bulbs from "./modules/bulbs";
import axios from "axios"
import PrimeVue from 'primevue/config';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';

Vue.use(Vuex);
Vue.use(PrimeVue);

Vue.component('Accordion', Accordion);
Vue.component('AccordionTab', AccordionTab);

export default new Vuex.Store({
    state: {},
    mutations: {},
    actions: {},
    modules: {
        bulbs,
    },
});
//'http://192.168.1.133:5000';
axios.defaults.baseURL = 'http://localhost:5000';
axios.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            //place your reentry code
        }
        return error.response;
    }
);
