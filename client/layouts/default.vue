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
@import '~/styles/index.less';

.content-wrapper {
	margin-left: @sidebar-width;
}
</style>