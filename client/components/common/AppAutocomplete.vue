<template>
	<div
	@focusin="focusIn($event)"
	@keydown.down="onArrowDown"
	@keydown.tab="onTab"
	@keydown.up="onArrowUp"
	@keydown.enter="onEnter"
	class="app-input-wrapper">
		<input
		:id="id"
		@input="updateValue($event.target.value)"
		:value="value"
		:type="type"
		:required="required"
		:disabled="disabled"
		:autocomplete="autocomplete"
		:class="{'open': isOpen && filteredOptions.length }"
		ref="input"
		class="app-input"
		placeholder=" ">
		<label
		:for="id"
		class="label">
			{{placeholder}}
		</label>
		<div
		v-show="isOpen"
		v-if="filteredOptions.length"
		class="app-autocomplete">
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
export default {
	name: 'AppAutocomplete',
	data() {
		return {
			isOpen: false,
			arrowPosition: -1,
		}
	},
	props: {
		value: String,
		id: {
			type: String,
			required: true
		},
		placeholder: String,
		type: {
			type: String,
			default: 'text'
		},
		options: Array,
		required: {
			type: Boolean,
			default: false
		},
		disabled: {
			type: Boolean,
			default: false
		},
		autocomplete: {
			type: String,
			default: 'on'
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
		focusIn(event) {
			this.isOpen = true
		},
		handleClickOutside(event) {
			if (!this.$el.contains(event.target)) {
				this.isOpen = false
				this.arrowPosition = -1
			}
		},
		onArrowDown(event) {
			if (this.arrowPosition < this.filteredOptions.length - 1)
				this.arrowPosition++
			else
				this.arrowPosition = 0
		},
		onArrowUp(event) {
			if (this.arrowPosition > 0)
				this.arrowPosition--
			else
				this.arrowPosition = this.filteredOptions.length - 1
		},
		onOptionClick(option) {
			this.updateValue(option.value)
			this.isOpen = false
			this.$refs['input'].focus()
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
		}
	},
	computed: {
		filteredOptions() {
			if (!this.options) return null
			if (!this.value) return this.options

			return this.options.filter(item =>
				item.value.toLowerCase().startsWith(
					this.value.toLowerCase()
					)
				&& item.value.toLowerCase() != this.value.toLowerCase()
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

@input-background: #FDFDFD;
@input-border: #F3F3F3;

.app-input-wrapper {
	margin-top: 18px;
	position: relative;
	height: 70px;
  width: 100%;
}

.label,
.app-input {
	transition: .2s ease all;
}

.app-input {
	position: relative;
  padding-left: 24px;
  height: 70px;
  width: 100%;

  background: @input-background;
  border: 1px solid @input-border;
  border-radius: 10px;

  &:focus {
  	border-color: @blue;
  }
  &:focus + .label {
  	color: @blue;
  }
  &:focus + .label,
  &:not(:placeholder-shown) + .label {
	  font-size: @fz-small;
	  top: -0.875em;
	  left: 1.5em;
	  padding: 0.25em 0.5em;
  }
  &.open:focus {
  	border-radius: 10px 10px 0 0;
  }
}

.label {
	position: absolute;
  top: 1.2em;
  left: 1.2em;

	color: @text-grey;
	background: linear-gradient(to top, @input-background 50%, transparent 0);
}

.app-autocomplete {
	position: absolute;
	top: calc(100% - 1px);
	z-index: 1;
	height: inherit;
	width: inherit;

	cursor: pointer;

	box-shadow: 2px 2px 10px rgba(0, 0, 0, .05);
	border-radius: 0 0 10px 10px;

	.option {
		.flex(center, normal, column);
		position: relative;
		min-height: 70px;
		padding: 23px 0;
		width: 100%;

		font-size: @fz-large;
		background: @input-background;
		border: 1px solid @input-border;
		border-top: none;
		border-bottom: none;

		padding-left: 24px;

		&:hover {
			background: #F2F2F2;
			border-color: transparent;
		}
		&.active,
		&:focus {
			background: #DFDFDF;
			border-color: transparent;
		}
	}

	.option:last-child {
		border-radius: 0 0 10px 10px;
	}
}

</style>
