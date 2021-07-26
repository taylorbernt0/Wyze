import axios from "axios";

export default {
    namespaced: true,
    state: {
        bulbGroups: [],
        selectedBulbs: [],
    },
    getters: {
        bulbGroups(state) {
            return state.bulbGroups;
        },
        selectedBulbs(state) {
            return state.selectedBulbs;
        },
    },
    actions: {
        async bulbPost(_, { mode, macs, color }) {
            console.log(color);
            let payload = {
                mode: mode,
                macs: JSON.stringify(macs),
                color: color,
            };
            const response = await axios.post("/bulbs", payload);
            console.log(response)
            return response;
        },

        async getBulbs({ commit }) {
            const response = await axios.get("/bulbs", {
                params: { data: "bulbs" },
            });

            let bulbs = Object.keys(response.data).map(
                (key) => response.data[key]
            );
            bulbs = bulbs.sort((a, b) => a.nickname.localeCompare(b.nickname));
            let bulbGroups = [];
            let lastBulbGroup = '';
            bulbs.forEach(bulb => {
               let bulbGroupSplit = bulb['nickname'].split(' ');
               if(!isNaN(bulbGroupSplit[bulbGroupSplit.length - 1]))
                   bulbGroupSplit.pop();
               let bulbGroup = bulbGroupSplit.join(' ');
               if(bulbGroup !== lastBulbGroup){
                   lastBulbGroup = bulbGroup;
                   let newGroupObj = {};
                   newGroupObj[bulbGroup] = [bulb];
                   bulbGroups.push(newGroupObj);
               }else{
                   bulbGroups[bulbGroups.length - 1][bulbGroup].push(bulb);
               }
            });
            console.log(bulbGroups);
            commit("setBulbs", bulbGroups);
        },

        async updateSelectedBulbs({ commit }, selectedBulbs) {
            commit("setSelectedBulbs", selectedBulbs);
        },

        async deleteProcess() {
            const response = await axios.delete("/bulbs");
            return response.data;
        },
    },

    mutations: {
        setBulbs(state, bulbGroups) {
            state.bulbGroups = bulbGroups;
        },
        setSelectedBulbs(state, selectedBulbs) {
            state.selectedBulbs = selectedBulbs;
        },
    },
};
