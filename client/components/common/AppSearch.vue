<template>
  <div class="app-search-wrapper">
    <app-input
      :value="value"
      @input="updateValue($event)"
      :type="type"
      :required="required"
      :disabled="disabled"
      :placeholder="placeholder"
      :round="round"
      :small="small"
      class="app-search"
    />

    <icon-search
      v-show="!value"
      class="icon-search"
    />
  </div>
</template>

<script>
import IconSearch from '~/components/icons/IconSearch'
import AppInput from '~/components/common/AppInput'

export default {
  name: 'AppSearch',

  components: {
    IconSearch,
    AppInput,
  },

  props: {
    value: String,

    placeholder: String,

    type: {
      type: String,
      default: 'text',
    },

    required: {
      type: Boolean,
      default: false,
    },

    disabled: {
      type: Boolean,
      default: false,
    },

    round: {
      type: Boolean,
      default: false,
    },

    small: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    updateValue(value) {
      this.$emit('input', value)
    },
  },
}
</script>

<style lang="less" scoped>

.app-search-wrapper {
  position: relative;

  height: fit-content;
  width: 100%;

  .app-search {
    position: relative;
  }

  .icon-search {
    .absolute();
    top: calc(50% - 12px);
    right: 18px;

    height: 24px;
    width: 24px;

    fill: @grey-darkset;

    cursor: text;
  }
}

</style>
