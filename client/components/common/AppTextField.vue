<template>
  <textarea
    rows="7"
    class="app-text-field"
  />
</template>

<script>
export default {
  name: 'AppTextField',
}
</script>

<style lang="less" scoped>

.app-text-field {
  padding: 32px;

  background: @grey-bright;
  border: 1px solid @grey-light;
  border-radius: 5px;

  resize: none;
}

</style>
