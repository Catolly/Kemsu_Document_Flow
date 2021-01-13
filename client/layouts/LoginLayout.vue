<template>
  <div class="container">
    <div id="login-wrapper">
      <the-form-login />
    </div>
  </div>
</template>

<script>
import TheFormLogin from '~/components/TheFormLogin'

export default {
  name: 'LoginLayout.vue',
  components: {
    TheFormLogin,
  },
}
</script>

<style lang="less">
@import '~/styles/index.less';

#login-wrapper {
  height: 100vh;
  .flex(center, center);
}

</style>

