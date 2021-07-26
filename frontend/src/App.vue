<template>
    <div id="app">
        <Nav />
        <div class="body">
            <router-view />
        </div>
    </div>
</template>

<script>
import Nav from "@/components/Nav.vue";

export default {
    components: {
        Nav,
    },
};
</script>

<style lang="scss">
body {
    padding: 0;
    margin: 0;
}

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;

    .body {
        margins: 0.5em;
    }
}
</style>
