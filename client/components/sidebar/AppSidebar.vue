<template>
  <div class="container">
    <div
      class="logo"
      @click="$router.push('/')"
    >
      <icon-logo />
      <h3 class="logo-title">Mydoc</h3>
    </div>

    <div class="nav">
      <app-nav-student v-if="Role.isStudent" />
      <app-nav-staff v-if="Role.isStaff" />
      <app-nav-admin v-if="Role.isAdmin" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { ROLE_IS } from '~/store/actions.type'

import IconLogo from '~/components/icons/IconLogo'
import AppNavStudent from '~/components/sidebar/AppNavStudent'
import AppNavStaff from '~/components/sidebar/AppNavStaff'
import AppNavAdmin from '~/components/sidebar/AppNavAdmin'

export default {
  name: 'AppSidebar',

  components: {
    IconLogo,
    AppNavStudent,
    AppNavStaff,
    AppNavAdmin,
  },

  async beforeMount() {
    try {
      await Promise.all([
        this.$store.dispatch(ROLE_IS, this.Role.Student),
        this.$store.dispatch(ROLE_IS, this.Role.Staff),
        this.$store.dispatch(ROLE_IS, this.Role.Admin),
      ])
    } catch (error) {
      console.error(error)
    }
  },

  computed: {
    ...mapGetters(['Role'])
  },
}
</script>

<style lang="less" scoped>

.logo {
  z-index: 1;
  cursor: pointer;

  position: fixed;
  top: 25px;
  left: 60px;

  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.logo-title {
  font-size: @fz-large;
  margin-bottom: 4px;
}

.nav {
  position: fixed;
  left: 0;
  top: 0;

  height: 100vh;
  width: inherit;

  box-shadow: 10px 4px 120px rgba(0, 0, 0, 0.04);
}

</style>

