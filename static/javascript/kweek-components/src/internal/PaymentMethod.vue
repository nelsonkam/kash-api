<template>
  <div @click="$emit('click')" class="container" :style="{'border-color': active ? 'black' : '#e5e7eb'}">
    <div class="radio-container">
      <div v-if="active" class="radio-active"></div>
    </div>
    <p style="margin: 0; font-size: 16px;">{{ name }}</p>
  </div>
</template>

<script>
export default {
name: "PaymentMethod",
  props: ['active', 'name'],

}
</script>

<style scoped>
.radio-container {
  border: 2px black solid;
  height: 18px;
  width: 18px;
  border-radius: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
}
.radio-active {
  height: 14px;
  width: 14px;
  background-color: black;
  border-radius: 16px;
}
.container {
  appearance: none;
  border-width: 1px;
  border-style: solid;
  border-radius: 4px;
  padding: 12px 12px;
  flex-grow: 1;
  margin: 8px 0;
  font-size: 16px;
  display: flex;
  align-items: center;
}
</style>
