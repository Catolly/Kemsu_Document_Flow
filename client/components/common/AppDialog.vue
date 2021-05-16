<template>
  <app-modal v-if="isOpen" class="modal">
    <div class="app-dialog">
      <slot class="content" />

      <app-button
        icon
        square
        red
        class="close-btn"
        @click="$emit('close')"
      >
        <icon-close />
      </app-button>
    </div>
  </app-modal>
</template>

<script>
import AppModal from '~/components/common/AppModal'
import AppButton from '~/components/common/AppButton'
import IconClose from '~/components/icons/IconClose'

export default {
  name: 'AppDialog',

  components: {
    AppModal,
    AppButton,
    IconClose,
  },

  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style lang="less" scoped>
.app-dialog {
  position: relative;
  width: 550px;
  min-width: 350px;

  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>
