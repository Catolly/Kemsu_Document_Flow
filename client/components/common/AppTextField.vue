<template>
  <div
    class="app-text-field-wrapper"
  >
    <textarea
      class="app-text-field"
      :rows="rows"
    />
  </div>
</template>

<script>
export default {
  name: 'AppTextField',
  props: {
    rows: {
      type: Number,
      default: 7,
    },
  },
}
</script>

<style lang="less" scoped>

.app-text-field-wrapper {
  width: 100%;

  &.error {
    .app-text-field,
    .app-text-field:focus {
      border-color: @red;
    }
  }

  .app-text-field {
    padding: 32px;

    width: inherit;

    background: @grey-bright;
    border: 1px solid @grey-light;
    border-radius: 5px;

    transition: .2s ease all;

    resize: none;

    &:focus {
      border-color: @blue;
    }
  }
}


</style>
