<template>
  <div class="container">
    <logo />
    <!-- Определяем, какие права у юзера -->
    <div class="nav-wrapper">
      <nav-student />
      <!-- <nav-staff /> -->
      <!-- <nav-admin /> -->
    </div>
  </div>
</template>

<script>
import Logo from '~/components/common/Logo'
import NavStudent from '~/components/common/NavStudent'
import NavStaff from '~/components/common/NavStaff'
import NavAdmin from '~/components/common/NavAdmin'

export default {
  name: 'Sidebar',
  components: {
    Logo,
    NavStudent,
    NavStaff,
    NavAdmin,
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

