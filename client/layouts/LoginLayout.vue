<template>
  <div id="container">
    <div id="login-wrapper">
      <form-layout>
        <login-form></login-form>
      </form-layout>
    </div>
  </div>
</template>

<script>
import FormLayout from '~/layouts/FormLayout'
import LoginForm from '~/components/LoginForm'

export default {
  name: 'LoginLayout.vue',
  components: {
    FormLayout,
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

