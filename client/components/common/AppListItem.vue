<template>
	<div
	@click="$emit('click')"
	class="app-list-item">
		<slot />
	</div>
</template>

<script>
export default {
	name: 'AppListItem'
}
</script>

<style lang="less" scoped>

.app-list-item {
	width: 100%;

	padding: 38px 50px;

	background: #FDFDFD;
	border: 2px solid #F3F3F3;
	border-radius: 12px;

	.flex(space-between, center);
	transition: .2s ease all;
  transition: margin 0s;
	cursor: pointer;

	&:hover {
		background: #F2F2F2;
		border-color: @blue;
	}
}

</style>
