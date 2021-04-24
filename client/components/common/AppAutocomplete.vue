<template>
	<div
  	@focusin="focusIn($event)"
  	@keydown.down="onArrowDown"
  	@keydown.tab="onTab"
  	@keydown.up="onArrowUp"
  	@keydown.enter="onEnter"
  	class="app-autocomplete"
  >

    <app-input
      @input="updateValue($event)"
      :value="value"
      :placeholder="placeholder"
      autocomplete="off"
      required
      ref="input"
      :class="{'open': isOpen && filteredOptions.length}"
    />


		<div
		v-show="isOpen"
		v-if="filteredOptions.length"
		class="option-list">
			<div
			v-for="(option, i) in filteredOptions"
			:key="option.id"
			@click="onOptionClick(option)"
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

		required: {
			type: Boolean,
			default: false
		},

		disabled: {
			type: Boolean,
			default: false
		},
	},

	methods: {
		updateValue(value) {
			this.$emit('input', value)

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
				this.isOpen = false
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

		onOptionClick(option) {
			this.updateValue(option.value)
			this.isOpen = false
			this.$refs.input.focus()
		},

		onEnter(event) {
			if (this.arrowPosition != -1) {
				event.preventDefault()
				this.updateValue(this.filteredOptions[this.arrowPosition].value)
				this.arrowPosition = -1
				this.isOpen = false
			}
		},

		onTab(event) {
			if (this.arrowPosition < this.filteredOptions.length - 1) {
				event.preventDefault()
				this.arrowPosition = this.arrowPosition + 1
			}
			else {
				this.arrowPosition = 0
				this.isOpen = false
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



  .option-list {
    position: absolute;
    top: calc(100% - 1px);
    z-index: 2; // z-index label'а = 1 и перекрывает при z-index = 1

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
