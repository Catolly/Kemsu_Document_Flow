<template>
  <div class="container">
    <div id="login-wrapper">
      <the-login-form />
    </div>
  </div>
</template>

<script>
import TheLoginForm from '~/components/TheLoginForm'

export default {
  name: 'LoginLayout.vue',
  components: {
    TheLoginForm,
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

