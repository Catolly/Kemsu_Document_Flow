<template>
  <label
    class="app-checkbox-wrapper"
    :class="{'checked': value}"
  >
    <input
      :checked="value"
      type="checkbox"
      class="app-checkbox"
      @change="toggle($event.target.checked)"
    >
    <icon-check-mark
      v-if="value"
      class="check-mark"
    />
  </label>
</template>

<script>
import IconCheckMark from '~/components/icons/IconCheckMark'

export default {
  name: 'AppCheckbox',

  components: {
    IconCheckMark,
  },

  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    toggle(value) {
      this.$emit('input', value)
    },
  },
}
</script>

<style lang="less" scoped>
.app-checkbox-wrapper {
  display: inline-flex;
  justify-content: center;

  position: relative;
  user-select: none;
  cursor: pointer;

  height: 36px;
  width: 36px;
  border-radius: 3px;
  border: 1px solid #E0E0E0;

  &:hover {
    background: #F8F8F8;
  }
  &.checked {
    border: none;
    background: @green;

    &:hover {
      background: @green-hover;
    }
  }
}

.app-checkbox {
  position: absolute;
  z-index: -1;
  opacity: 0;
}

.check-mark {
  align-self: center;

  width: 24px;
  height: 16px;
}
</style>
