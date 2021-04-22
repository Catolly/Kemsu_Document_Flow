<template>
	<div class="app-wrapper">

		<div
  		@focusin="open"
  		@focusout="close"
  		:disabled="disabled"
  		ref="appSelect"
  		tabindex=0
  		class="app-select"
    >

			<span class="selected">
  			{{selected}}
				<div class="arrow" />
			</span>

			<label
  			:class="{'small': selected}"
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

	</div>
</template>

<script>
export default {
	name: 'AppSelect',

	data() {
		return {
			isOpen: false,
		}
	},

	props: {
		selected: {
      type: String,
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
			this.$emit('select', option)
			this.unfocus()
		},

    focus() {
      this.$refs.appSelect.focus()
    },
	},
}
</script>

<style lang="less" scoped>

@select-background: #FDFDFD;
@select-border: #F3F3F3;

.app-select {
	position: relative;
  font-size: @fz-large;
}

.option {
  width: inherit;
}

.app-select,
.label {
	cursor: pointer;
}

.app-select {
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

	min-height: 70px;
	width: 100%;
	padding: 24px;
  padding-right: 48px;
}

.selected {
	position: relative;

  user-select: none;

	background: @select-background;
	border: 1px solid @select-border;
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

	background: @select-background;
	border: 1px solid @select-border;

	&:hover {
		background: #F2F2F2;
		border: 1px solid #D2D2D2;
	}
}

.label {
	position: absolute;
	top: 1.2em;
	left: 1.2em;

	color: @text-grey;
	background: linear-gradient(to top, @select-background 50%, transparent 0);
}

.arrow {
	.absolute();
	@size: 8px;

	top: 50% - .5*@size;
	right: 32px;

	width: 0;
	height: 0;

	border-top: @size solid #262626;
	border-left: .5*@size solid transparent;
	border-right: .5*@size solid transparent;
}

</style>
