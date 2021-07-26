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
                 :row-height="layout.length / 5"
                 :is-draggable="true"
                 :is-resizable="false"
                 :vertical-compact="true"
                 :use-css-transforms="true">
            <grid-item v-for="data in layout"
                       :static="false"
                       :x="data.x"
                       :y="data.y"
                       :w="data.w"
                       :h="data.h"
                       :i="data.i"
                       :key="data.bulb.mac">
                <Bulb
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

export default {
    name: "Home",
    computed: mapGetters("bulbs", ["bulbsList", "selectedBulbs"]),
    data() {
        return {
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
        this.getBulbs().then(()=> this.createGridLayout());
    },
    methods: {
        ...mapActions("bulbs", [
            "getBulbs",
            "bulbPost",
            "deleteProcess",
            "updateSelectedBulbs",
        ]),
        checked(mac) {
            if (this.selectedBulbs.includes(mac)) {
                this.updateSelectedBulbs(
                    this.selectedBulbs.filter((a) => a !== mac)
                );
            } else this.selectedBulbs.push(mac);
            this.updateSelectedBulbs(this.selectedBulbs);
        },
        checkAll() {
            this.bulbsList.forEach((bulb) => {
                this.checked(bulb.mac);
            });
        },
        createGridLayout() {
            let i=0;
            this.bulbsList.forEach(bulb => {
              this.layout.push({"x": i%5, "y": Math.round(i/5), "w": 1, "h": 15, "i": i, "bulb": bulb});
              i++;
            });
        },
    },
};
</script>
