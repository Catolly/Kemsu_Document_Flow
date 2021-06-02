<template>
  <nav class="app-nav-admin">
    <NuxtLink
    to="/schemas"
    class="nav-link">Обходной лист</NuxtLink>
    <NuxtLink
    to="/users"
    class="nav-link">Пользователи</NuxtLink>
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
  name: 'AppNavAdmin'
}
</script>

<style lang="less" scoped>
.app-nav-admin {
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
