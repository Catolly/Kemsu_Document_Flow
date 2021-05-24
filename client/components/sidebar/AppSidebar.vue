<template>
  <div class="container">
    <div class="content">
      <div class="logo" @click="$router.push('/')">
        <icon-logo />
        <h3 class="logo-title">Mydoc</h3>
      </div>

      <app-nav-student class="nav" v-if="Role.isStudent" />
      <app-nav-staff class="nav" v-if="Role.isStaff" />
      <app-nav-admin class="nav" v-if="Role.isAdmin" />

      <NuxtLink class="about-link clear" to="/about">
        Сделано в [IT Биржа]
      </NuxtLink>
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
.content {
  position: fixed;
  left: 0;
  top: 0;

  height: 100vh;
  width: inherit;

  box-shadow: 10px 4px 120px rgba(0, 0, 0, 0.04);

  display: grid;
  grid-template-rows: minmax(auto-fit, 250px) 1fr 1fr;

  padding: 3em;
  padding-top: 1.5em;
  padding-right: 0;
}

.logo {
  align-self: flex-start;

  top: 1.5em;
  left: 3.5em;

  cursor: pointer;

  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.logo-title {
  font-size: @fz-large;
  margin-bottom: 4px;
}

.nav {

}

.about-link {
  align-self: flex-end;

  font-size: @fz-small;
  color: @grey-darkset;
}
</style>

