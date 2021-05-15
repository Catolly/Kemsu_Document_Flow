<template>
  <nav class="app-nav-admin">
    <NuxtLink
    to="/schemas"
    class="nav-link">Обходной лист</NuxtLink>
    <NuxtLink
    to="/users"
    class="nav-link">Пользователи</NuxtLink>
    <NuxtLink
    to="/bypass-sheets"
    class="nav-link">Подписи</NuxtLink>
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
  margin-top: 250px;
  margin-left: 50px;

  .flex(center, normal, column);
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
    color: #000;
  }
  &.nuxt-link-active {
    font-weight: @fw-normal;
    color: #000;
  }
}
</style>
