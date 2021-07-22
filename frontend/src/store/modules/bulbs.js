import axios from "axios";

export default {
    namespaced: true,
    state: {
        bulbs: [],
    },
    getters: {
        bulbsList(state) {
            return state.bulbs;
        },
    },
    actions: {
        async bulbPost(_, { mode, macs, color }) {
            console.log(color);
            let payload = {
                mode: mode,
                macs: JSON.stringify(macs),
                color: color
            };
            const response = await axios.post("/bulbs", payload);
            return response;
        },

        async getBulbs({ commit }) {
            const response = await axios.get("/bulbs", {
                params: { data: "bulbs" },
            });

            let bulbs = Object.keys(response.data).map(
                (key) => response.data[key]
            );
            commit(
                "setBulbs",
                bulbs.sort((a, b) => a.nickname.localeCompare(b.nickname))
            );
        },

        async deleteProcess() {
            const response = await axios.delete("/bulbs");
            return response.data;
        },
    },

    mutations: {
        setBulbs(state, bulbs) {
            state.bulbs = bulbs;
        },
    },
};
