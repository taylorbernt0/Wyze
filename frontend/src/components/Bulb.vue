<template>
    <div class="bulb" v-bind:class="{isChecked: isChecked, isOffline: !isOnline}" @click="isOnline ? checked() : ''">
        <div>
          <strong>{{ name }}</strong>
        </div>

        <br>

        <i v-bind:class="{pi:true, 'pi-sun':isOnline}" v-bind:style="{fontSize: '5rem', color: isOnline ? (isOn ? color : 'black') : 'grey'}"></i>

        <br>
        <br>

        <div v-if="isOnline" class="brightness-bar">
          <div class="brightness-bar-inside"></div>
        </div>
    </div>
</template>

<script>
import 'primeicons/primeicons.css';

export default {
    name: "Bulb",
    props: {
        name: String,
        mac: String,
        isChecked: Boolean,
        isOn: Boolean,
        isOnline: Boolean,
        brightness: Number,
        color: String,
        temperature: Number
    },
    methods: {
        checked() {
            this.$emit("checked");
        },
    }
};
</script>

<style scoped lang="scss">
.bulb {
  background: #dfe1e3;
  padding: 15px;
  margin: 10px;
  width: 90%;
  height: 9rem;
  border-radius: 5%;
}
.isOffline{
  background: #646566;
}
.isChecked {
  background: #B0BEC5;
}
.brightness-bar {
  height: 5px;
  width: 100%;
  background-color: #b7c3cd;
}
.brightness-bar-inside {
  height: 5px;
  width: 80%;
  background-color: #465a66;
}
</style>
