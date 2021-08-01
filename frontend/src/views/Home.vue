<template>
    <div class="home">
        <div>
            <Button class="primary" label="Check All" @click="checkAll()" />
        </div>
        <div>
            #<input v-model="color" />
            <Button
                label="Change Color"
                class="primary"
                @click="
                    bulbPost({
                        mode: 'color',
                        macs: selectedBulbs,
                        color: color,
                    })
                "
            />
        </div>
        <div>
            <input v-model="temp" />
            <Button
                label="Change Temp"
                class="primary"
                @click="
                    bulbPost({
                        mode: 'temp',
                        macs: selectedBulbs,
                        color: temp,
                    })
                "
            />
        </div>

        <grid-layout :layout.sync="layout"
                 :col-num="5"
                 :row-height="1"
                 :is-draggable="false"
                 :is-resizable="false"
                 :vertical-compact="false"
                 :use-css-transforms="true">
            <grid-item v-for="data in layout"
                       :static="false"
                       :x="data.x"
                       :y="data.y"
                       :w="data.w"
                       :h="data.h"
                       :i="data.i"
                       :key="data.i">
                <Bulb v-if="data.bulb"
                :name="data.bulb.nickname"
                :mac="data.bulb.mac"
                :isChecked="selectedBulbs.includes(data.bulb.mac)"
                :isOn="data.bulb.is_on"
                :isOnline="data.bulb.is_online"
                :brightness="data.bulb.brightness"
                :color="'#' + data.bulb.color"
                :temperature="data.bulb.color_temp"
                @checked="checked(data.bulb.mac)"
                />
            </grid-item>
        </grid-layout>
    </div>
</template>

<script>
import Button from "@/components/Button.vue";
import Bulb from "@/components/Bulb.vue";
import VueGridLayout from 'vue-grid-layout';
import { mapActions, mapGetters } from "vuex";
import 'primevue/resources/themes/saga-blue/theme.css';

export default {
    name: "Home",
    computed: mapGetters("bulbs", ["bulbGroups", "selectedBulbs"]),
    data() {
        return {
            refreshDelay: 10000,
            color: null,
            temp: null,
            layout: [],
        };
    },
    components: {
        Button,
        Bulb,
        GridLayout: VueGridLayout.GridLayout,
        GridItem: VueGridLayout.GridItem
    },
    created() {
        this.refreshBulbs();
        this.timer = setInterval(this.refreshBulbs, this.refreshDelay);
    },
    methods: {
        ...mapActions("bulbs", [
            "getBulbs",
            "bulbPost",
            "deleteProcess",
            "updateSelectedBulbs",
        ]),
        refreshBulbs(){
          this.getBulbs().then(() => this.createGridLayout());
        },
        checked(mac) {
            if (this.selectedBulbs.includes(mac)) {
                this.updateSelectedBulbs(
                    this.selectedBulbs.filter((a) => a !== mac)
                );
            } else this.selectedBulbs.push(mac);
            this.updateSelectedBulbs(this.selectedBulbs);
        },
        checkAll() {
            this.bulbGroups.forEach((bulbGroup) => {
                const groupName = Object.keys(bulbGroup)[0];
                bulbGroup[groupName].forEach(bulb => {
                  this.checked(bulb.mac);
                });
            });
        },
        createGridLayout() {
            let i=0;
            let r=0;
            let max_cols = 5;
            this.layout = [];
            this.bulbGroups.forEach(bulbGroup => {
              const groupName = Object.keys(bulbGroup)[0];
              let c=0;
              bulbGroup[groupName].forEach(bulb => {
                this.layout.push({"x": c, "y": r, "w": 1, "h": 15, "i": i, "bulb": bulb});
                i++;
                c++;
              });
              while(c < max_cols){ // Empty cells to maintain horizontal grid integrity
               this.layout.push({"x": c, "y": r, "w": 1, "h": 15, "i": i, "bulb": null});
               i++;
               c++;
              }
              r++;
            });
        },
    },
    beforeDestroy() {
      clearInterval(this.timer);
    }
};
</script>
