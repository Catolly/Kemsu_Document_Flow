<template>
	<div
	@click="$emit('click')"
	class="v-list-item-base">
		<slot />
	</div>
</template>

<script>
export default {
	name: 'VListItemBase'
}
</script>

<style lang="less" scoped>

.v-list-item-base {
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

</style>