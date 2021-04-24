<template>
	<div class="app-input-wrapper">
		<input
  		:value="value"
  		@input="updateValue($event.target.value)"
  		:type="type"
  		:required="required"
  		:disabled="disabled"
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

// mixins
.input-label-colors(@color) {
  border-color: @color;
  & + .label {
    color: @color;
  }
}
//

.app-input-wrapper {
  position: relative;

  height: 70px;
  width: 100%;

  border: 1px solid @grey-light;

  &.error {
    .app-input:focus {
      .input-label-colors(@red)
    }
  }

  &.round,
  &.round .app-input {
    border-radius: 100px;
  }

  &,
  .app-input {
    border-radius: 10px;
  }

  .label,
  .app-input {
    transition: .2s ease all;
  }

  .app-input {
    position: relative;

    min-height: 100%;
    min-width: 100%;
    padding-left: 24px;

    border: 1px solid transparent;
    background: @grey-bright;

    &:focus {
      .input-label-colors(@blue)
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

    // 51%, а не 50%, чтобы закрыть border-top родителя
    background: linear-gradient(to top, @grey-bright 51%, transparent 0);

    user-select: none;
    cursor: text;
  }
}




</style>
