<template>
  <app-button
    blue
    semi-round
    class="app-chips"
    @click="$emit('click')"
  >
    <slot />
  </app-button>
</template>

<script>
import AppButton from '~/components/common/AppButton'


export default {
  name: 'AppChips',

  components: {
    AppButton,
  },
}
</script>

<style lang="less" scoped>

.app-chips {
  transition: .1s;

  padding: 12px 24px;

  height: fit-content;
  font-size: @fz-small;
  text-align: left;
  word-break: break-all;
}

</style>
