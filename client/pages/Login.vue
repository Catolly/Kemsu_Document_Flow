<template>
  <section id="container">
    <login-layout />
  	<logo class="big" />
  </section>
</template>

<script>
import Logo from '~/components/Logo'
import LoginLayout from '~/layouts/LoginLayout'

export default {
	name: 'Login',
  components: {
  	Logo,
    LoginLayout
  }
}
</script>

<style>

</style>

