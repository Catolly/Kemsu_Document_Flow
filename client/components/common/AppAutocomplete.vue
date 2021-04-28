<template>
	<div
  	@focusin="focusIn($event)"
  	@keydown.down="onArrowDown"
  	@keydown.tab="onTab"
  	@keydown.up="onArrowUp"
  	@keydown.enter="onEnter"
  	class="app-autocomplete"
  >

    <label>
      <app-input
        @input="$emit('input', $event)"
        @change="$emit('change', $event)"
        :value="value"
        :placeholder="placeholder"
        :class="{'open': isOpen && filteredOptions.length}"
        :type="type"
        :required="required"
        :small="small"
        :disabled="disabled"
        :error-messages="errorMessages"
        :messages="messages"
        autocomplete="off"
        ref="input"
      />

      <div
        :class="{'rotate': isOpen && filteredOptions.length,}"
        class="arrow"
        @click="focusIn($event)"
      />
    </label>

		<div
		v-show="isOpen"
		v-if="filteredOptions.length"
		class="option-list">
			<div
			v-for="(option, i) in filteredOptions"
			:key="option.id"
			@click="selectOption(option)"
			:class="{'active': arrowPosition === i}"
			class="option"
			tabindex="0">
				{{option.value}}
			</div>
		</div>

	</div>
</template>

<script>
import AppInput from '@/components/common/AppInput'

export default {
	name: 'AppAutocomplete',

	data:() => ({
    isOpen: false,
    arrowPosition: -1,
  }),

  components: {
    AppInput,
  },

	props: {
		value: String,

		placeholder: String,

		options: {
      type: Array,
      default: () => [],
    },

    type: {
      type: String,
      default: 'text',
    },

		required: {
			type: Boolean,
			default: false
		},

    small: {
      type: Boolean,
      default: false
    },

		disabled: {
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

  // watch: {
  //   value() {
  //     this.arrowPosition = -1
  //   },
  // },

	methods: {
		updateValue(value) {
			this.$emit('input')
      this.$emit('change')

			//Сбрасываем позицию option'ов
			this.arrowPosition = -1
		},

		focusOut() {
			this.isOpen = false
		},

		focusIn() {
			this.isOpen = true
		},

		handleClickOutside(event) {
			if (!this.$el.contains(event.target)) {
				this.focusOut()
				this.arrowPosition = -1
			}
		},

		onArrowDown() {
			if (this.arrowPosition < this.filteredOptions.length - 1)
				this.arrowPosition++
			else
				this.arrowPosition = 0
		},

		onArrowUp() {
			if (this.arrowPosition > 0)
				this.arrowPosition--
			else
				this.arrowPosition = this.filteredOptions.length - 1
		},

		selectOption(option) {
			this.updateValue(option.value)
			this.$refs.input.focus()
		},

		onEnter(event) {
			if (this.arrowPosition != -1) {
				event.preventDefault()
				this.updateValue(this.filteredOptions[this.arrowPosition].value)
				this.arrowPosition = -1
			}
		},

		onTab(event) {
			if (this.arrowPosition < this.filteredOptions.length - 1) {
				event.preventDefault()
				this.arrowPosition = this.arrowPosition + 1
			}
			else {
				this.arrowPosition = 0
				this.focusOut()
			}
		},
	},

	computed: {
		filteredOptions() {
			if (!this.options) return null
			if (!this.value) return this.options

			return this.options.filter(item =>
				item.value.toLowerCase()
                  .startsWith(this.value.toLowerCase())
				&& item.value.toLowerCase() != this.value.toLowerCase())
		}
	},

	mounted() {
		document.addEventListener('click', this.handleClickOutside)
	},

	destroyed() {
		document.removeEventListener('click', this.handleClickOutside)
	},
}
</script>

<style lang="less" scoped>

.app-autocomplete {
  position: relative;

	height: fit-content;
  width: 100%;

  .arrow {
    .arrow(@app-input-height);
    .app-autocomplete.small {
      .arrow(@app-small-input-height);
    }

    cursor: text;

    &.rotate {
      transform: rotate(180deg);
    }
  }

  .option-list {
    position: absolute;

    top: calc(@app-input-height - 1px);
    .app-autocomplete.small {
      top: calc(@app-small-input-height - 1px);
    }

    z-index: 2; // z-index label'а = 1 и перекрывает при z-index = 1

    width: 100%;

    cursor: pointer;

    box-shadow: 2px 2px 10px rgba(0, 0, 0, .05);

    .option {
      display: flex;
      justify-content: flex-start;
      align-items: center;

      position: relative;
      min-height: 3.5em;
      padding-left: 24px;

      font-size: @fz-large;
      background: @grey-bright;

      border: 1px solid @grey-light;
      border-top: none;
      border-bottom: none;

      &:last-child {
        border-radius: 0 0 10px 10px;
      }

      &:hover {
        background: @grey-medium;
        border-color: transparent;
      }

      &.active,
      &:focus {
        background: @grey-dark;
        border-color: transparent;
      }
    }
  }
}

</style>
