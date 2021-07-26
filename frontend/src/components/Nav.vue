<template>
    <nav>
        <div class="title"><img src="../assets/WyzeLogo.svg" alt="" /></div>
        <div class="button-group">
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
            <Button label="Delete Processes" @click="deleteProcess" />
        </div>
    </nav>
</template>

<script>
import Button from "@/components/Button.vue";
import { mapActions, mapGetters } from "vuex";

export default {
    name: "Home",
    computed: mapGetters("bulbs", ["selectedBulbs"]),
    components: {
        Button,
    },
    methods: {
        ...mapActions("bulbs", ["getBulbs", "bulbPost", "deleteProcess"]),
    },
};
</script>

<style scoped lang="scss">
nav {
    padding: 0.25em 0.5em;
    display: flex;
    align-items: center;
    background-color: #212529;
    .title {
        width: 8em;
        color: #ffffff;
        text-align: center;
    }

    .button-group {
        margin-left: auto;
    }
}
</style>
