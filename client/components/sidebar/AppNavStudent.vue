<template>
  <nav class="app-nav-student">
    <NuxtLink
    to="/bypass-sheets"
    class="nav-link">Обходной лист</NuxtLink>
    <NuxtLink
    to="/settings"
    class="nav-link">Настройки</NuxtLink>
    <NuxtLink
    to="/contacts"
    class="nav-link">Контакты</NuxtLink>
  </nav>
</template>

<script>
export default {
  name: 'AppNavStudent'
}
</script>

<style lang="less" scoped>
.app-nav-student {
  display: flex;
  flex-direction: column;
}

.nav-link {
  margin-top: 16px;

  color: @text-grey;
  font-weight: @fw-light;
  font-size: @fz-large;

  &::after {
    display: none;
  }
  &:hover {
    color: @black;
  }
  &.nuxt-link-active {
    font-weight: @fw-normal;
    color: @black;
  }
}
</style>
