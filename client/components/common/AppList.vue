<template>
  <div
    class="app-list"
    :style="style"
  >
    <slot />
  </div>
</template>

<script>
export default {
  name: 'AppList',

  props: {
    gap: {
      type: Number,
      default: 12,
    },
  },

  computed: {
    gridRowGap() {
      return {'grid-row-gap': `${this.gap}px`}
    },

    style() {
      return [
        this.gridRowGap
      ]
    },
  },
}
</script>

<style scoped>
.app-list {
  display: grid;
}
</style>
