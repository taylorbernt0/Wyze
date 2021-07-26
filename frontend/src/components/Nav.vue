<template>
    <nav>
        <div class="content">
            <div class="title"><img src="../assets/WyzeLogo.svg" alt="" /></div>
            <div class="button-group">
                <Button
                    label="Rainbow"
                    class="primary-alt"
                    @click="bulbPost({ mode: 'rainbow', macs: selectedBulbs })"
                />
                <Button
                    label="Strobe"
                    class="primary-alt"
                    @click="bulbPost({ mode: 'strobe', macs: selectedBulbs })"
                />
                <Button
                    label="Party"
                    class="primary-alt"
                    @click="bulbPost({ mode: 'party', macs: selectedBulbs })"
                />
                <Button
                    label="Delete Processes"
                    class="primary-alt"
                    @click="deleteProcess"
                />
            </div>
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
    position: fixed;
    top: 0;
    z-index: 1;
    width: 100%;
    background-color: #212529;

    .content {
        margin: 0.25em 0.5em;
        display: flex;
        align-items: center;

        .title {
            width: 8em;
            color: #ffffff;
            text-align: center;
        }

        .button-group {
            margin-left: auto;
        }
    }
}
</style>
