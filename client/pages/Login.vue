<template>
  <section class="container">
  	<logo class="big" />
    <div id="form-login-wrapper">
      <the-form-login />
    </div>
  </section>
</template>

<script>
import Logo from '~/components/Logo'
import TheFormLogin from '~/components/TheFormLogin'

export default {
	layout: 'empty',
	name: 'Login',
  components: {
  	Logo,
    TheFormLogin,
  }
}
</script>

<style lang="less" scoped>

#form-login-wrapper {
  height: 100vh;
  .flex(center, center);
}
</style>

