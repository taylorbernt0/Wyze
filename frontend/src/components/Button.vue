<template>
    <button class="btn" @click="onClick">
        {{ label }}
    </button>
</template>

<script>
export default {
    name: "Button",
    props: {
        label: String,
    },
    methods: {
        onClick() {
            this.$emit("click");
        },
    },
};
</script>

<style scoped lang="scss">
.btn {
    padding: 10px 15px;
    margin: 10px;
    color: white;
    border-radius: 7px;
    border: none;
    background-color: #00dfe4;

    &:hover {
        cursor: pointer;
        background-color: #3be6e9;
    }

    &:active {
        transform: scale(0.98);
        box-shadow: 3px 2px 22px 1px rgba(0, 0, 0, 0.12);
    }
}
</style>
