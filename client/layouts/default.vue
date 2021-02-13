<template>
	<div class="container">
		<logo />
		<sidebar-layout />
		<div class="content-wrapper">
			<Nuxt />
		</div>
	</div>
</template>

<script>
import SidebarLayout from '~/layouts/SidebarLayout'
import Logo from '~/components/Logo'

export default {
	components: {
		SidebarLayout,
		Logo,
	},
}
</script>

<style lang="less" scoped>

.content-wrapper {
	margin-left: @sidebar-width;
	padding: 0 110px;
	height: 100vh;
	background: @background;
}

</style>