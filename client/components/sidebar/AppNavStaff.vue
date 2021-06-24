<template>
  <nav class="app-nav-staff">
    <nuxt-link
    to="/bypass-sheets"
    class="nav-link">Подписи</nuxt-link>
    <nuxt-link
    to="/settings"
    class="nav-link">Настройки</nuxt-link>
    <nuxt-link
    to="/contacts"
    class="nav-link">Контакты</nuxt-link>
    <nuxt-link
    v-if="extended"
    to="/deadlines"
    class="nav-link">Сроки</nuxt-link>
    <nuxt-link
    v-if="extended"
    to="/status"
    class="nav-link">Статус</nuxt-link>
  </nav>
</template>

<script>
export default {
  name: 'AppNavStaff',

  props: {
    extended: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style lang="less" scoped>
.app-nav-staff {
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
