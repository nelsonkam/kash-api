<template>
  <div class="input-container">
    <input :value="value" @input="$emit('input', $event.target.value)" class="input" :type="type"
           :placeholder="placeholder">
    <p v-if="error" style="margin: 4px 0 0; color: red; font-size: 14px; font-family: inherit;">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: "KInput",
  props: ['placeholder', 'value', 'type', 'error'],
}
</script>

<style>
.input {
  appearance: none;
  border: 1px #e5e7eb solid;
  border-radius: 4px;
  padding: 10px 12px;
  font-size: 16px;
}

.input-container {
  margin: 8px 0;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
</style>
