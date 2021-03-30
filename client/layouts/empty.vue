<template>
	<div class="container">
		<logo class="big" />
		<Nuxt />
	</div>
</template>

<script>
import Logo from '~/components/common/Logo'

export default {
	name: 'empty',
	components: {
		Logo,
	},
	middleware: 'checkUserIsLoggedOut',
}
</script>

<style lang="less" scoped>

</style>