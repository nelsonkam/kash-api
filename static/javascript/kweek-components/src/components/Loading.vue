<template>
  <div class="loading rotate" :style="styles" ></div>
</template>

<script>
export default {
name: "Loading",
  props: ['color'],
  data() {
    return {
      styles: {borderRadius: '100%', borderColor: '#FFFFFF40', borderBottomColor: "#FFFFFF"}
    }
  },
  created() {
    console.log(this.color, this.styles.borderColor)
  }
}
</script>

<style scoped>
.loading {
  height: 18px; width: 18px; border-width: 3px; border-style: solid;
}
@keyframes rotate {
  0% {
    transform: rotate(0deg)
  }

  100% {
    transform: rotate(360deg)
  }
}

.rotate {
  animation: rotate .9s ease 0s infinite normal forwards;
}
</style>
