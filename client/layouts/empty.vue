<template>
	<div class="container">
		<Nuxt />
	</div>
</template>

<script>
export default {
	name: 'empty',
	middleware: 'checkUserIsLoggedOut'
}
</script>

<style lang="less" scoped>

</style>