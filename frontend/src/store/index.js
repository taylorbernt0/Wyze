import Vue from "vue";
import Vuex from "vuex";
import bulbs from "./modules/bulbs";
import axios from "axios"

Vue.use(Vuex);

export default new Vuex.Store({
    state: {},
    mutations: {},
    actions: {},
    modules: {
        bulbs,
    },
});

axios.defaults.baseURL = 'http://192.168.1.133:5000';
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
