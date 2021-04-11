<template>
  <div class="app-list">
    <slot />
  </div>
</template>

<script>
export default {
  name: 'AppList',
}
</script>

<style scoped>
.app-list	 > *:not(:first-child) {
  margin-top: 12px;
}
</style>
