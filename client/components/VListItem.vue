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
	height: 105px;
	width: 100%;

	padding: 0 50px;
	margin-bottom: 12px;

	background: #FDFDFD;
	border: 1px solid #F3F3F3;
	border-radius: 12px;

	.flex(space-between, center);
	transition: .2s ease all;
	cursor: pointer;

	&:hover {
		background: #FAFAFA;
		border-color: @blue;
	}
}
</style>