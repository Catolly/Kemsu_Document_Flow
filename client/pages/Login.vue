<template>
  <section id="container">
    <login-layout></login-layout>
  	<logo class="big"></logo>
  </section>
</template>

<script>
import logo from '~/components/logo'
import LoginLayout from '~/layouts/LoginLayout'

export default {
	name: 'Login',
  components: {
  	logo,
    LoginLayout
  }
}
</script>

<style>

</style>

