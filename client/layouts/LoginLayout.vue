<template>
  <div id="container">
    <div id="login-wrapper">
      <login-form />
    </div>
  </div>
</template>

<script>
import LoginForm from '~/components/LoginForm'

export default {
  name: 'LoginLayout.vue',
  components: {
    LoginForm,
  },
}
</script>

<style lang="less">
@import '~/styles/index.less';

#container {
  position: relative;
}

#login-wrapper {
  height: 100vh;
  .flex(center, center);
}

input {
  height: 70px;
}

</style>

