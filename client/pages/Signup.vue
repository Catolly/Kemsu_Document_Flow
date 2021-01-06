<template>
  <section id="container">
    <signup-layout></signup-layout>
  	<logo class="big"></logo>
  </section>
</template>

<script>
import logo from '~/components/logo'
import SignupLayout from '~/layouts/SignupLayout'

export default {
	name: 'Signup',
  components: {
  	logo,
    SignupLayout
  }
}
</script>

<style>

</style>

