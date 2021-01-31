<template>
  <nav class="nav">
    <NuxtLink 
    to="/"
    exact
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
  name: 'TheNavStudent'
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

.nav {
  margin-top: 250px;
  margin-left: 50px;

  .flex(center, normal, column);
}

.nav-link {
  margin-top: 16px;

  color: @text-grey;
  font-weight: @fw-light;

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