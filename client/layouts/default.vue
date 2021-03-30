<template>
	<div class="container">
		<sidebar />
		<div class="content-wrapper">
			<Nuxt />
		</div>
	</div>
</template>

<script>
import Sidebar from '~/components/common/Sidebar'

export default {
	name: 'default',
	components: {
		Sidebar,
	},
	middleware: 'checkUserIsLoggedIn'
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