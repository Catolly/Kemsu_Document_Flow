<template>
  <div class="app-message-list">
    <span
      v-for="errorMessage of errorMessages"
      :key="errorMessage"
      class="error-message"
    >
      {{errorMessage}}
    </span>

    <template v-if="!errorMessages.length">
      <span
        v-for="message of messages"
        :key="message"
        class="message"
      >
        {{message}}
      </span>
    </template>
  </div>
</template>

<script>
export default {
  name: 'AppMessageList',

  props: {
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
.app-message-list {
  padding-top: 8px;
  padding-left: 24px;

  display: grid;
  grid-row-gap: 8px;

  font-size: @fz-small;
  font-weight: @fw-light;
}

.message,
.error-message {
  font-size: @fz-small;
  font-weight: @fw-light;
}

.message {
  color: @grey-darkset;
}
</style>
