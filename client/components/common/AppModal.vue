<template>
  <div class="app-modal-background">
    <div class="app-modal">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppModal',
}
</script>

<style lang="less" scoped>

.app-modal-background {
  display: flex;
  justify-content: center;
  align-items: center;

  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;

  height: 100vh;
  width: 100vw;
  padding: 32px 64px;

  background: fade(@black, 70%);

  .app-modal {
    width: fit-content;
    height: fit-content;
    max-height: 100%;
    padding: 48px 64px;

    background: @white;
    box-shadow: 0 2px 10px fade(@black, 40%);
    border-radius: 10px;

    overflow-y: auto;
  }
}

</style>
