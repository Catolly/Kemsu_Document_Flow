<template>
	<div class="input-wrapper">
		<input
		class="input"
  		:value="value"
  		@input="updateValue($event.target.value)"
  		:type="type"
  		:required="required"
  		:disabled="disabled"
  		placeholder=" "
    >
		<label class="label">{{placeholder}}</label>
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
			default: 'text'
		},
		required: {
			type: Boolean,
			default: false
		},
		disabled: {
			type: Boolean,
			default: false
		}
	},

	methods: {
		updateValue(value) {
      this.$emit('input', value)
		}
	},
}
</script>

<style lang="less" scoped>
@input-background: #FDFDFD;

	position: relative;

  height: 70px;
  width: 100%;


  &.round,
  &.round .app-input {
    border-radius: 100px;
  }
}

.label,
.input {
	transition: .2s ease all;
}

.input {
  position: relative;

  height: inherit;
  width: inherit;
  padding-left: 24px;

  background: @input-background;
  border: 1px solid #F3F3F3;
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
}

.label {
	position: absolute;
  top: 1.2em;
  left: 1.2em;

	color: @text-grey;
	background: linear-gradient(to top, @input-background 50%, transparent 0);
}

.invalid {
	.input {
		border-color: @red;
	}
	.label {
		color: @red;
	}
}

.round {
  border-radius: 25px;
}

</style>
