<template>
  <div class="icon-edit">
    <icon-base
      :height="height"
      :width="width"
    >
      <path d="M15.7895 0.729492L13.2484 3.27061L17.4589 7.48114L20 4.94002L15.7895 0.729492ZM11.6591 4.85984L0 16.519V20.7295H4.21053L15.8697 9.07036L11.6591 4.85984Z" fill=""/>
    </icon-base>
  </div>
</template>

<script>
import IconBase from '~/components/icons/IconBase'

export default {
  name: 'IconEdit',

  components: {
    IconBase,
  },

  props: {
    height: {
      type: Number,
      default: 21,
    },
    width: {
      type: Number,
      default: 20,
    },
  },
}
</script>
