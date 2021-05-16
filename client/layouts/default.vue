<template>
	<div v-if="isAuthenticated" class="container">
		<app-sidebar class="app-sidebar"/>
		<div class="content-wrapper">
			<Nuxt class="content" />
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex"
import { CHECK_AUTH } from '~/store/actions.type'

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

  computed: {
    ...mapGetters(['isAuthenticated']),
  },

  beforeMount() {
    this.$store.dispatch(CHECK_AUTH)
      .then(() => {
        if (!this.isAuthenticated) this.$router.push('/login')
      })
  },
}
</script>

<style lang="less" scoped>
@app-sidebar-width: 250px;

.app-sidebar {
  width: @app-sidebar-width;
}

.content-wrapper {
	margin-left: @app-sidebar-width;

	height: fit-content;

	background: @white;
}

.content {
  min-height: 100vh;
  padding-left: 96px;
  padding-right: 48px;
  padding-bottom: 60px;
}

</style>
