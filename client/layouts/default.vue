<template>
	<div class="container">
		<logo />
		<sidebar-layout />
		<Nuxt />
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

<style scoped>

</style>