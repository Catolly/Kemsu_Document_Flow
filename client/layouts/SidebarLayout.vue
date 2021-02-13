<template>
  <div class="container">
    <!-- Определяем, какие права у юзера -->
    <div class="nav-wrapper">
      <the-nav-student />
      <!-- <the-nav-worker /> -->
      <!-- <the-nav-admin /> -->
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo'
import TheNavStudent from '~/components/TheNavStudent'
import TheNavWorker from '~/components/TheNavWorker'
import TheNavAdmin from '~/components/TheNavAdmin'

export default {
  name: 'SidebarLayout',
  components: {
    Logo,
    TheNavStudent,
    TheNavWorker,
    TheNavAdmin,
  },
}
</script>

<style lang="less" scoped>

.nav-wrapper {
  position: fixed;
  left: 0;
  top: 0;

  height: 100vh;
  width: @sidebar-width;

  box-shadow: 10px 4px 120px rgba(0, 0, 0, 0.04);
}
</style>

