<template>
	<div class="container">
		<div class="v-select-wrapper">
			<select 
			@change="forceBlur"
			ref='select'
			class="v-select">
				<option>Скидка на столовую</option>
				<option>Отчисление</option>
			</select>
			<div class="arrow"></div>
			<label class="label">Причина</label>
		</div>
	</div>
</template>

<script>

export default {
	name: 'VSelect',
	data() {
		return {

		}
	},
	methods: {
		forceBlur() {
			this.$refs.select.blur()
		}
	}
}
</script>

<style lang="less" scoped>

@select-background: #FDFDFD;

.container,
.v-select-wrapper {
	width: fit-content;
	position: relative;
}

.v-select {
	position: relative;
	height: 70px;
	width: 500px;
	padding-left: 32px;

	font-size: @fz-large;

	background: @select-background;
  border: 1px solid #F3F3F3;
  border-radius: 10px;

  appearance: none;
  --webkit-appearance: none;
  --moz-appearance: none;

  &:focus + .arrow {
  	transform: rotate(180deg);
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

.label {
	position: absolute;
	top: -0.875em;
	left: 1.5em;
	padding: 0.25em 0.5em; 

	font-size: @fz-small; 
	color: @text-grey;
	background: linear-gradient(to top, @select-background 50%, transparent 0);
}

</style>