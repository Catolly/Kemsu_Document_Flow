<template>
	<div class="container">
		<input 
		:id="id"
		:value="value"
		@input="updateValue($event.target.value)"
		:type="type"
		:required="required"
		class="input"
		placeholder=" ">
		<label 
		:for="id"
		class="label">
			{{placeholder}}
		</label>
	</div>
</template>

<script>
export default {
	name: 'VInput',
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
		required: {
			type: Boolean,
			default: false
		}
	},
	methods: {
		updateValue(value) {
			this.$emit('input', value)
		}
	}
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

.container {
	position: relative;
	margin-top: 18px;
}

.label,
.input {
	transition: .2s ease all;
}

.input {
  background: @input-background;
  border: 1px solid @input-border;
  border-radius: 10px;

  padding-left: 24px;
  width: 100%;

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
	
	color: @label-color;
	background: linear-gradient(to top, @input-background 50%, transparent 0);
}

.is-invalid {
	.input {
		border-color: @red;
	}
	.label {
		color: @red;
	}
}

</style>