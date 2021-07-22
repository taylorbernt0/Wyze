<template>
    <div class="bulb" :style="'background-color: ' + color">
        <input :checked="isChecked" type="checkbox" @click="checked" />
        <div>
            {{ name }}
        </div>
        <div>
            {{ mac }}
        </div>
        <div>
            online: {{ isOnline }}
        </div>
    </div>
</template>

<script>
export default {
    name: "Bulb",
    props: {
        name: String,
        mac: String,
        isChecked: Boolean,
        isOnline: Boolean,
        color: String
    },
    methods: {
        checked() {
            this.$emit("checked");
        },
    },
};
</script>

<style scoped lang="scss">
.bulb {
    background: #dadada;
    padding: 15px;
    margin: 10px;
}
</style>
