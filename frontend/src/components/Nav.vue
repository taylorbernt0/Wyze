<template>
    <nav>
        <span class="title">WYZE</span>
        <span>
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
        </span>
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
    background-color: #949494;
    .title {
        font-size: 24px;
        color: #00dfe4;
    }
}
</style>
