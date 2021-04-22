<template>
	<div class="container">
		<icon-logo class="big" />
		<Nuxt />
	</div>
</template>

<script>
import IconLogo from '~/components/icons/IconLogo'

export default {
	name: 'empty',

  head () {
    return {
      bodyAttrs: {
        class: 'body-reset'
      }
    }
  },

	components: {
		IconLogo,
	},

	// middleware: 'checkUserIsLoggedOut',
}
</script>

<style lang="less" scoped>

</style>
