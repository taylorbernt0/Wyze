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
        margin: 4.5em 0.5em;
    }

    *, *::after, *::before {
      -webkit-user-select: none;
      -webkit-user-drag: none;
      -webkit-app-region: no-drag;
      cursor: default;
    }
}
</style>
