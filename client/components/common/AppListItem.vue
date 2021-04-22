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
@item-background-color: #FDFDFD;
@item-border-color: #F3F3F3;

.app-list-item,
.app-list-item.simple:hover {
  background: @item-background-color;
  border-color: @item-border-color;
}

.app-list-item.simple {
  cursor: auto;
}

.app-list-item {
	width: 100%;
	padding: 40px 48px;

	background: @item-background-color;
	border: 2px solid @item-border-color;
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
