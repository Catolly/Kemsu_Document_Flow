<template>
	<div class="container">
		<icon-logo class="logo big" />
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

.logo {
  position: fixed;
  top: 25px;
  left: 60px;
}

</style>
