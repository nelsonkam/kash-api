<template>
  <div @click="$emit('click')" class="container" :style="{'border-color': active ? 'black' : '#e5e7eb'}">
    <div class="radio-container">
      <div v-if="active" class="radio-active"></div>
    </div>
    <div style="display:flex; justify-content: space-between;align-items: center; flex-grow: 1">
      <div>
        <p style="font-size: 16px;margin: 0 0 8px; font-weight: bold;">{{ name }}</p>
        <div style="display:flex;align-items:center;">
          <p style="margin: 0; font-size: 15px;padding-right: 8px;">{{ price }} XOF</p>
          <p style="margin: 0; font-size: 15px;color: #828282">({{ eta }})</p>
        </div>
      </div>
      <div>
        <img :src="logo" style="border-radius: 8px; height: 48px;width: 48px;">
      </div>
    </div>
  </div>
</template>

<script>
export default {
name: "ShippingMethod",
  props: ['active', 'name', 'eta', 'price','logo'],

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
  margin-top: 4px;
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
  padding: 8px 12px;
  flex-grow: 1;
  margin: 8px 0;
  font-size: 16px;
  display: flex;
  align-items: flex-start;
}
</style>
