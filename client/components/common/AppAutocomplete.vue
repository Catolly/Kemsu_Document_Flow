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
        :loading="loading"
        :disabled="disabled"
        :error-messages="errorMessages"
        :messages="messages"
        autocomplete="off"
        ref="input"
      />

      <div
        v-show="!loading"
        :class="{'rotate': isOpen && filteredOptions.length}"
        class="arrow"
        @click="focusIn($event)"
      />
    </label>

		<div
		v-show="isOpen && filteredOptions.length"
		class="option-list">
      <template v-for="(option, index) in options">
  			<div
        v-show="filteredOptions.includes(option)"
  			:key="index"
  			@click="selectOption(option)"
  			:class="{'active': arrowPosition === index}"
  			class="option"
  			tabindex="0">
  				{{option.value}}
  			</div>
      </template>
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
		value: String | Number,

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

    loading: {
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

  watch: {
    value() {
			//Сбрасываем позицию option'ов
      this.arrowPosition = -1
    },
  },

	methods: {
		updateValue(value) {
			this.$emit('input', value)
      this.$emit('change', value)
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
				String(item.value)
          .toLowerCase()
          .includes(
            String(this.value).toLowerCase()
          )
				&& String(item.value).toLowerCase() != String(this.value).toLowerCase()
      )
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

    max-height: 280px; // 4 default option min
    overflow-y: auto;

    cursor: pointer;

    box-shadow: 2px 2px 10px rgba(0, 0, 0, .05);
    border-radius: 0 0 10px 10px;

    .option {
      display: flex;
      justify-content: flex-start;
      align-items: center;

      position: relative;
      min-height: 3.5em;
      width: 100%;
      padding: .5em 24px;
      line-height: 125%;

      font-size: @fz-large;
      background: @grey-bright;

      border: 1px solid @grey-light;
      border-top: none;
      border-bottom: none;

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
