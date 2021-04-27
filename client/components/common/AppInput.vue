<template>
	<div
    :class="classObj"
    class="app-input-wrapper"
    ref="appInputWrapper"
  >
    <div class="app-input-field">
  		<input
    		:value="value"
    		@input="updateValue($event.target.value)"
    		:type="type"
    		:required="required"
    		:disabled="disabled"
        :error-messages="errorMessages"
        :messages="messages"
    		class="app-input"
    		placeholder=" "
        ref="appInput"
      >

      <label
        class="label"
        @click="focus"
      >
        {{placeholder}}
      </label>
    </div>

    <div class="messages">
      <span
        v-for="message of errorMessages"
        :key="message"
        class="error-message"
      >
        {{message}}
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
  </div>
</template>

<script>
export default {
  name: 'AppInput',

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
        'round': this.round,
        'small': this.small,
        'error': !!this.errorMessages.length,
      }
    },
  },

  methods: {
    updateValue(value) {
      this.$emit('input', value.trim())
    },

    focus() {
      this.$refs.appInput.focus()
    },
  },
}
</script>

<style lang="less" scoped>

.app-input-wrapper {
  position: relative;

  height: fit-content;
  width: 100%;

  &.small .app-input-field {
    height: 50px;
  }

  &.error {
    .app-input,
    .app-input:focus {
      .focused(@red);
    }
  }

  &.round,
  &.round .app-input {
    border-radius: 100px;
  }

  &.open .app-input { // Для поддержки AppAutocomplete
    border-radius: 10px 10px 0 0;
  }

  &,
  .app-input {
    border-radius: 10px;
  }

  .label,
  .app-input {
    transition: .2s ease all;
  }

  .app-input-field {
    position: relative;

    height: 70px;
    width: inherit;
  }

  .app-input {
    position: relative;

    height: inherit;
    width: inherit;
    padding-left: 24px;
    padding-right: 48px;

    border: 1px solid @grey-light;
    background: @grey-bright;

    &:focus {
      .focused(@blue);
    }

    // Фиксирует плейсхолдер на верхней левой границе при фокусе
    &:focus,
    &:not(:placeholder-shown) {
      & + .label {
        font-size: @fz-small;
        top: -0.875em;
        left: 1.5em;
        padding: 0.25em 0.5em;
      }
    }
  }

  .label {
    position: absolute;
    top: calc(50% - .6em); // Фиксирует label по центру input'а
    left: 1.2em;
    z-index: 1;

    color: @grey-darkset;

    background: linear-gradient(to top, @grey-bright 50%, transparent 0);

    user-select: none;
    cursor: text;
  }
}

</style>
