<template>
  <div class="container">
    <!-- Перенаправляет на главную страницу роли пользователя -->
    <div
      class="logo"
      @click="$router.push('/')"
    >
      <icon-logo />
    </div>
    <!-- Определяем, какие права у юзера -->
    <div class="nav">
      <!-- <app-nav-student /> -->
      <app-nav-staff />
      <!-- <app-nav-admin /> -->
    </div>
  </div>
</template>

<script>
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
}
</script>

<style scoped>

.logo {
  z-index: 1;
  cursor: pointer;

  position: fixed;
  top: 25px;
  left: 60px;
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

