<template>
	<div
    class="app-select-wrapper"
    :class="classObj"
  >
		<div
  		@focusin="open"
  		@focusout="close"
      ref="appSelect"
      tabindex=0
  		class="app-select"
    >
			<span class="selected">
  			{{value}}
				<div class="arrow" />
			</span>

			<label
  			:class="{'small': value}"
  			class="label"
      >
				{{placeholder}}
			</label>

			<div
			 v-show="isOpen"
			 class="option-wrapper"
      >
				<div
				  v-for="option in options"
				  :key="option"
				  @click="select(option)"
				  class="option"
        >
					{{option}}
				</div>
			</div>

		</div>

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
    classObj() {
      return {
        'error': !!this.errorMessages.length,
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
      this.isOpen = true
    },

		select(option) {
			this.$emit('input', option)
			this.unfocus()
		},

    focus() {
      this.$refs.appSelect.focus()
    },
	},
}
</script>

<style lang="less" scoped>

.app-select-wrapper {
	position: relative;
  font-size: @fz-large;

  height: inherit;

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

  .app-select {
    position: relative;

    &:focus .selected {
      border-color: @blue;
      border-radius: 10px 10px 0 0;
    }

    &:focus .label {
      color: @blue;
    }
    &:focus .label,
    .label.small {
      font-size: @fz-small;
      top: -0.875em;
      left: 1.5em;
      padding: 0.25em 0.5em;
    }

    &:focus .arrow {
      transform: rotate(180deg);
    }
  }

  .selected,
  .label {
    transition: .2s ease all;
  }

  .selected,
  .option {
    display: flex;
    flex-direction: column;
    justify-content: center;

    min-height: @app-input-height;
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
  }

  .option-wrapper {
    position: absolute;
    top: calc(100% - 1px);
    height: inherit;
    width: 100%;

    z-index: 1;

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

    color: @grey-darkset;
    background: linear-gradient(to top, @grey-bright 50%, transparent 0);
  }

  .arrow {
    .arrow();

    cursor: pointer;
  }
}

</style>
