<template>
  <div
    :class="{'error': error || !!errorMessages.length}"
    class="app-text-field-wrapper"
  >
    <textarea
      :value="value"
      :rows="rows"
      class="app-text-field"
      @input="$emit('input', $event.target.value)"
    />

    <app-message-list
      :error-messages="errorMessages"
      :messages="messages"
      class="message-list"
      ref="AppMessageList"
    />
  </div>
</template>

<script>
import AppMessageList from '~/components/common/AppMessageList'

export default {
  name: 'AppTextField',

  components: {
    AppMessageList
  },

  props: {
    value: {
      type: String,
      default: '',
    },

    rows: {
      type: Number,
      default: 8,
    },

    error: {
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
}

.app-text-field {
  padding: 32px;

  width: inherit;

  font-size: @fz-large;
  font-weight: @fw-light;
  line-height: 160%;

  background: @grey-bright;
  border: 1px solid @grey-light;
  border-radius: 5px;

  transition: .2s ease all;

  resize: none;

  &:focus {
    border-color: @blue;
  }
}
</style>
