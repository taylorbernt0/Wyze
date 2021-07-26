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
        <div v-for="bulb in bulbsList" :key="bulb.mac">
            <Bulb
                :name="bulb.nickname"
                :mac="bulb.mac"
                :isChecked="selectedBulbs.includes(bulb.mac)"
                :isOnline="bulb.is_online"
                :brightness="bulb.brightness"
                :color="'#' + bulb.color"
                :temperature="bulb.color_temp"
                @checked="checked(bulb.mac)"
            />
        </div>
    </div>
</template>

<script>
import Button from "@/components/Button.vue";
import Bulb from "@/components/Bulb.vue";
import { mapActions, mapGetters } from "vuex";

export default {
    name: "Home",
    computed: mapGetters("bulbs", ["bulbsList", "selectedBulbs"]),
    data() {
        return {
            color: null,
            temp: null,
        };
    },
    components: {
        Button,
        Bulb,
    },
    created() {
        this.getBulbs();
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
    },
};
</script>
