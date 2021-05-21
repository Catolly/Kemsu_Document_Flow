<template>
	<div v-if="!isAuthenticated" class="empty container">
		<div class="logo">
      <icon-logo class="big" />
      <h3 class="logo-title">Mydoc</h3>
    </div>
		<Nuxt />
	</div>
</template>

<script>
import { mapGetters } from "vuex"
import { CHECK_AUTH } from '~/store/actions.type'

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

  computed: {
    ...mapGetters(['isAuthenticated']),
  },

	beforeMount() {
    this.$store.dispatch(CHECK_AUTH)
      .then(() => {
        if (this.isAuthenticated) this.$router.push('/')
      })
  },
}
</script>

<style lang="less" scoped>
.logo {
  position: fixed;
  top: 25px;
  left: 60px;

  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.logo-title {
  margin-bottom: 4px;
}
</style>
