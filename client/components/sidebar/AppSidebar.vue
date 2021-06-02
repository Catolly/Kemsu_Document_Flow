<template>
  <div class="container">
    <div class="content">
      <div class="logo" @click="$router.push('/')">
        <icon-logo />
        <h3 class="logo-title">Mydoc</h3>
      </div>

      <app-nav-student v-if="Role.isStudent" />
      <app-nav-staff v-if="Role.isStaff" />
      <app-nav-admin v-if="Role.isAdmin" />

      <div class="links">
        <span>
          Возникли проблемы?
          <br>
          <a class="clear" target="_blank" :href="telegramHelpUrl">
            Напишите нам
          </a>
        </span>
        <NuxtLink class="clear" to="/about">
          Сделано в [IT Биржа]
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { ROLE_IS } from '~/store/actions.type'

import { telegramHelpUrl } from '~/services/config'

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
    ...mapGetters(['Role']),

    telegramHelpUrl() {
      return telegramHelpUrl
    },
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

  padding: 2.5em;
  padding-top: 1.5em;
  padding-right: 0;
}

.logo {
  align-self: flex-start;

  cursor: pointer;

  display: flex;
  align-items: flex-end;
  gap: .5em;
}

.logo-title {
  font-size: @fz-large;
  margin-bottom: .25em;
}

.links {
  align-self: flex-end;

  display: flex;
  flex-direction: column;
  gap: .5em;

  * {
    font-size: @fz-small;
    color: @grey-darkset;
  }
}
</style>

