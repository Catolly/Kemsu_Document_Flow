<template>
  <div
    :class="classObj"
    class="app-text-field-wrapper"
  >
    <textarea
      class="app-text-field"
      :rows="rows"
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
    rows: {
      type: Number,
      default: 7,
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

  computed: {
    classObj() {
      return {
        'error': !!this.errorMessages.length,
      }
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
