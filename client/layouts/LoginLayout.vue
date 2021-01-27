<template>
  <div class="container">
    <Nuxt />
    <div id="form-login-wrapper">
      <the-form-login />
    </div>
  </div>
</template>

<script>
import TheFormLogin from '~/components/TheFormLogin'

export default {
  name: 'LoginLayout',
  components: {
    TheFormLogin,
  },
}
</script>

<style lang="less">
@import '~/styles/index.less';

#form-login-wrapper {
  height: 100vh;
  .flex(center, center);
}

</style>

