<template>
  <label
    :class="{'checked': value}"
    class="app-radio-wrapper"
    tabindex="0"
  >
    <input
      :checked="value"
      type="radio"
      class="app-radio"
      @change="$emit('input', $event.target.checked)"
    >
  </label>
</template>

<script>
export default {
  name: 'AppRadio',

  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style lang="less" scoped>
.app-radio-wrapper {
  display: inline-flex;
  justify-content: center;

  position: relative;
  user-select: none;
  cursor: pointer;

  height: 36px;
  width: 36px;
  border-radius: 100%;
  border: 1px solid @grey-light;

  &:not(.checked):hover {
    background: @grey-light;
  }
  &.checked {
    border-color: @blue;

    &:after {
      .absolute();

      top: calc(50% - 5px);
      left: calc(50% - 5px);

      height: 10px;
      width: 10px;

      background: @blue;
      border-radius: 100%;
    }
  }
}

.app-radio {
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
