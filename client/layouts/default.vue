<template>
	<div class="container">
		<sidebar />
		<div class="content-wrapper">
			<Nuxt />
		</div>
	</div>
</template>

<script>
import Sidebar from '~/components/Sidebar'
import Logo from '~/components/Logo'

export default {
	name: 'default',
	components: {
		Sidebar,
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