<template>
	<div :class="classObj" class="app-select-wrapper">
		<div
  		@focusin="open"
  		@focusout="close"
      :tabindex="isDisabled ? -1 : 0"
      ref="appSelect"
  		:class="{
        'is-open': isOpen,
        'disabled': isDisabled,
      }"
      class="app-select"
    >
			<span :class="{'disabled': isDisabled}" class="selected">
  			{{value}}
				<div :class="{'disabled': isDisabled}" class="arrow" />
			</span>

			<label
        v-if="placeholder"
  			:class="{
          'small': value,
          'disabled': isDisabled,
        }"
  			class="label"
      >
				{{placeholder}}
			</label>

			<div v-show="isOpen" class="option-wrapper">
				<div
				  v-for="(option, index) in options"
				  :key="index"
				  @click="select(option)"
				  class="option"
        >
					{{option}}
				</div>
			</div>
		</div>

    <app-message-list
      v-if="errorMessages.length || messages.length"
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
	name: 'AppSelect',

  components: {
    AppMessageList
  },

	data() {
		return {
			isOpen: false,
		}
	},

	props: {
		value: {
      type: [String, Number],
      default: '',
    },

		placeholder: String,

		options: {
			type: Array,
			required: true,
		},

		disabled: {
			type: Boolean,
			default: false
		},

    small: {
      type: Boolean,
      default: false
    },

    error: {
      type: Boolean,
      default: false
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
    isDisabled() {
      return this.disabled || !this.options.length
    },

    classObj() {
      return {
        'error': !!this.errorMessages.length,
        'small': !!this.small,
      }
    },
  },

	methods: {
		unfocus() {
			this.$refs.appSelect.blur()
		},

		close() {
			this.isOpen = false
		},

    open() {
      if (this.isDisabled) return
      this.isOpen = true
    },

		select(option) {
      if (this.isDisabled) return
			this.$emit('input', option)
			this.unfocus()
		},

    focus() {
      if (this.isDisabled) return
      this.$refs.appSelect.focus()
    },
	},
}
</script>

<style lang="less" scoped>
.app-select-wrapper {
	position: relative;
  font-size: @fz-large;

  height: 70px;

  &.small {
    height: 50px;
  }

  &.error {
    .app-select,
    .app-select:focus {
      .selected {
        .focused(@red);
      }
    }
  }

  .option {
    width: inherit;
  }

  .app-select,
  .label {
    cursor: pointer;
  }

  .disabled {
    cursor: default;
  }

  .app-select {
    position: relative;

    &.is-open {
      .selected {
        border-color: @blue;
        border-radius: 10px 10px 0 0;
      }
      .label {
        color: @blue;
      }
      .arrow {
        transform: rotate(180deg);
      }
    }

    &.is-open .label,
    .label.small {
      font-size: @fz-small;
      top: -0.875em;
      left: 1.5em;
      padding: 0.25em 0.5em;
    }
  }

  .selected,
  .label {
    transition: .2s ease all;
  }

  &.small {
    .selected,
    .option {
      height: 50px;
    }
  }

  .selected,
  .option {
    display: flex;
    flex-direction: column;
    justify-content: center;

    height: @app-input-height;
    width: 100%;
    padding: 24px;
    padding-right: 48px;
  }

  .selected {
    position: relative;

    user-select: none;

    background: @grey-bright;
    border: 1px solid @grey-light;
    border-radius: 10px;

    &.disabled {
      background: @grey-medium;
    }
  }

  .option-wrapper {
    position: absolute;
    top: calc(100% - 1px);

    height: inherit;
    width: 100%;

    max-height: 16em;
    overflow-y: auto;

    z-index: 2; // z-index: 1 не перекрывает label app-input

    box-shadow: 2px 2px 10px rgba(0, 0, 0, .05);
    border-radius: 0 0 10px 10px;
    .option:last-child {
      border-radius: 0 0 10px 10px;
    }
  }

  .option {
    user-select: none;

    background: @grey-bright;
    border: 1px solid @grey-light;

    &:hover {
      background: @grey-medium;
      border: 1px solid @grey-dark;
    }
  }

  .label {
    position: absolute;
    top: 1.2em;
    left: 1.2em;

    user-select: none;

    color: @grey-darkset;
    background: linear-gradient(to top, @grey-bright 50%, transparent 0);

    &.disabled {
      background: @grey-medium;
    }
  }

  .arrow {
    .arrow();
    cursor: pointer;
    &.disabled {
      cursor: default;
    }
  }
}
</style>
