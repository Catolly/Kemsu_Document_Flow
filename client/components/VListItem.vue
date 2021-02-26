<template>
	<div 
	@click="clickHanler"
	class="v-list-item">
		<slot />
	</div>
</template>

<script>
export default {
	name: 'VListItem',
	methods: {
		clickHanler() {
			this.$emit('click')
		}
	}
}
</script>

<style lang="less" scoped>

.v-list-item {
	width: 100%;

	padding: 38px 50px;
	margin-bottom: 12px;

	background: #FDFDFD;
	border: 2px solid #F3F3F3;
	border-radius: 12px;

	.flex(space-between, center);
	transition: .2s ease all;
	cursor: pointer;

	&:hover {
		background: #F2F2F2;
		border-color: @blue;
	}
}

.green {
	color: @green;
	border-color: @green;
}

.red {
	color: @red;
	border-color: @red;
}

.disabled {
	color: @text-grey;
	border-color: #F3F3F3;
}

</style>