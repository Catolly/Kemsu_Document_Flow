<template>
	<div class="v-list">
		<slot />
	</div>
</template>

<script>
export default {
	name: 'VList',
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

.v-list {
	width: 80%;
}
</style>