<template>
  <nav class="app-nav-admin">
    <nuxt-link
    to="/schemas"
    class="nav-link">Обходной лист</nuxt-link>
    <nuxt-link
    to="/users"
    class="nav-link">Пользователи</nuxt-link>
    <nuxt-link
    to="/settings"
    class="nav-link">Настройки</nuxt-link>
    <nuxt-link
    to="/contacts"
    class="nav-link">Контакты</nuxt-link>
    <nuxt-link
    to="/status"
    class="nav-link">Статус</nuxt-link>
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
