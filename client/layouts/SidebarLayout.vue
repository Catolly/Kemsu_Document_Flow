<template>
  <div class="container">
    <logo />

    <!-- Определяем, какие права у юзера -->
    <div class="nav-wrapper">
      <the-sidebar-student />
      <!-- <the-sidebar-worker /> -->
      <!-- <the-sidebar-admin /> -->
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo'
import TheSidebarStudent from '~/components/TheSidebarStudent'
import TheSidebarWorker from '~/components/TheSidebarWorker'
import TheSidebarAdmin from '~/components/TheSidebarAdmin'

export default {
  name: 'SidebarLayout',
  components: {
    Logo,
    TheSidebarStudent,
    TheSidebarWorker,
    TheSidebarAdmin,
  },
}
</script>

<style lang="less" scoped>
.nav-wrapper {
  position: fixed;
  left: 0;
  top: 0;

  height: 100vh;
  width: 250px;
}
</style>

