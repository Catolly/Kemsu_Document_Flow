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
	components: {
		AppSidebar,
	},
	// middleware: 'checkUserIsLoggedIn'
}
</script>

<style lang="less" scoped>
@app-sidebar-width: 250px;

.app-sidebar {
  width: @app-sidebar-width; //Переделать через Vuetify v-col
}

.content-wrapper {
	margin-left: @app-sidebar-width;
	padding: 0 110px;
	height: 100vh;
	background: @background;
}

</style>
