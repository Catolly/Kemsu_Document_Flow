<template>
	<div class="container">
		<app-sidebar class="app-sidebar" />
		<div class="content-wrapper">
			<Nuxt />
		</div>
	</div>
</template>

<script>
import AppSidebar from '~/components/sidebar/AppSidebar'

export default {
	name: 'default',

  head () {
    return {
      bodyAttrs: {
        class: 'body-reset'
      }
    }
  },

	components: {
		AppSidebar,
	},

	// middleware: 'checkUserIsLoggedIn'
}
</script>

<style lang="less" scoped>
@app-sidebar-width: 250px;

.app-sidebar {
  width: @app-sidebar-width;
}

.content-wrapper {
	margin-left: @app-sidebar-width;
  padding-left: 104px;
  padding-right: 48px;

	height: 100vh;

	background: @white;
}

</style>
