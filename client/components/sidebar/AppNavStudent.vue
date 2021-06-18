<template>
  <nav class="app-nav-student">
    <nuxt-link
    to="/bypass-sheets"
    class="nav-link">Обходной лист</nuxt-link>
    <nuxt-link
    to="/settings"
    class="nav-link">Настройки</nuxt-link>
    <nuxt-link
    to="/contacts"
    class="nav-link">Контакты</nuxt-link>
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
