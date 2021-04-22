<template>
  <span
    class="app-chips"
    @click="$emit('click')"
  >
    <slot />
  </span>
</template>

<script>
export default {
  name: 'AppChips'
}
</script>

<style lang="less" scoped>

.app-chips {
  display: inline-block;
  box-sizing: border-box;

  padding: 12px 24px;
  width: fit-content;

  font-size: @fz-small;
  color: @blue;
  border: 1px solid @blue;
  border-radius: 100px;
}

</style>
