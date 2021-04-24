<template>
  <div class="app-search-wrapper">
    <app-input
      :value="value"
      @input="updateValue($event)"
      :type="type"
      :required="required"
      :disabled="disabled"
      :placeholder="placeholder"
      :error-messages="errorMessages"
      :messages="messages"
      :round="round"
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

    errorMessages: {
      type: Array,
      default:() => [],
    },

    messages: {
      type: Array,
      default:() => [],
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

  height: 70px;
  width: 100%;

  .icon-search {
    .absolute();
    top: calc(50% - 12px);
    right: 18px;

    height: 24px;
    width: 24px;

    fill: @grey-darkset;

    cursor: text;
  }

  .app-search {
    position: relative;

    height: inherit;
    width: inherit;
  }
}

</style>
