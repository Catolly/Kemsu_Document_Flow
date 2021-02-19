<template>
	<div class="select-wrapper">
		<div 
		@focusin="changeFocus"
		@focusout="changeFocus"
		:id="id"
		:disabled="disabled"
		ref="select"
		class="select"
		tabindex=0>
			<span
			:required="required"
			class="selected">
				{{selected}}
				<div class="arrow" />
			</span>
			<label 
			:class="selected ? 'small' : ''"
			class="label">
				{{title}}
			</label>
			<div 
			v-show="open"
			class="option-wrapper">
				<div
					v-for="option in options"
					:key="option.id"
					@click="select(option)"
					class="option">
					{{option.value}}
				</div> 
			</div>
		</div>
	</div>
</template>

<script>
import VInput from '~/components/VInput'

export default {
	name: 'VSelect',
	components: {
		VInput,
	},
	data() {
		return {
			selected: null,
			open: false,
		}
	},
	props: {
		id: {
			type: String,
			required: true
		},
		title: String,
		options: {
			type: Array,
			required: true
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
		close() {
			this.$refs.select.blur()
		},
		changeFocus() {
			this.open = !this.open
		},
		select(option) {
			this.selected = option.value
			this.close()
		},
 	},
}
</script>

<style lang="less" scoped>

@select-background: #FDFDFD;
@select-border: #F3F3F3;

.select-wrapper {
	width: fit-content;
	position: relative;
}

.select,
.option {
	position: relative;
	width: 500px;

	font-size: @fz-large;
}

.select,
.label {
	cursor: pointer;
}

.select {
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
	.flex(center, normal, column);
	height: 70px;
  width: 100%;
	padding-left: 24px;
}

.selected {
	position: relative;

	background: @select-background;
	border: 1px solid @select-border;
	border-radius: 10px;
}

.option-wrapper {
	position: absolute;
	height: 100%;
	width: 100%;

	z-index: 1;

	box-shadow: 2px 2px 10px rgba(0, 0, 0, .05);
	border-radius: 0 0 10px 10px;
	.option:last-child {
		border-radius: 0 0 10px 10px;
	}
}

.option {
	background: @select-background;
	border: 1px solid @select-border;
	border-top: none;

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

.is-invalid {
	.selected {
		border-color: @red;
	}
	.label {
		color: @red;
	}
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