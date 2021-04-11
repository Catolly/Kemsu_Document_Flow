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
		<label @click="focus" class="label">{{placeholder}}</label>
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
		},
    focus() {
      this.$refs.appInput.focus()
    }
	},
}
</script>

<style lang="less" scoped>
@input-background: #FDFDFD;

.label,
.app-input {
	transition: .2s ease all;
}

.app-input, // need to not hide parent corners
.app-input-wrapper {
  border-radius: 10px;
}

.app-input-wrapper {
	position: relative;

  height: 70px;
  width: 100%;

  border: 1px solid #F3F3F3;
  background: @input-background;

  &.round,
  &.round .app-input {
    border-radius: 100px;
  }
}

.app-input {
  position: relative;

  min-height: 100%;
  min-width: 100%;
  padding-left: 24px;

  border: 1px solid transparent;

  &:focus {
  	border-color: @blue;
    & + .label {
    	color: @blue;
    }
  }

  // fix placeholder on input top border
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
  top: calc(50% - .6em); // fix on input center
  left: 1.2em;

	color: @text-grey;
	background: linear-gradient(to top, @input-background 50%, transparent 0);

  user-select: none;
}

</style>
