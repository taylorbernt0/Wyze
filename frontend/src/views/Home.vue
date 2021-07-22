<template>
    <div class="home">
        <div>
            <Button
                label="Rainbow"
                @click="bulbPost({ mode: 'rainbow', macs: selectedBulbs })"
            />
            <Button
                label="Strobe"
                @click="bulbPost({ mode: 'strobe', macs: selectedBulbs })"
            />
            <Button
                label="Party"
                @click="bulbPost({ mode: 'party', macs: selectedBulbs })"
            />
            <Button label="Check All" @click="checkAll()" />
            <Button label="Delete Processes" @click="deleteProcess" />
        </div>
        <div>
            #<input v-model="color" />
            <Button
                label="Change Color"
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
    computed: mapGetters("bulbs", ["bulbsList"]),
    data() {
        return {
            selectedBulbs: [],
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
        ...mapActions("bulbs", ["getBulbs", "bulbPost", "deleteProcess"]),
        checked(mac) {
            if (this.selectedBulbs.includes(mac)) {
                this.selectedBulbs = this.selectedBulbs.filter(
                    (a) => a !== mac
                );
            } else this.selectedBulbs.push(mac);
        },
        checkAll() {
            this.bulbsList.forEach((bulb) => {
                this.checked(bulb.mac);
            });
        },
    },
};
</script>
