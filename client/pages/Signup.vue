<template>
  <section class="container">
    <signup-layout />
  	<logo class="big" />
  </section>
</template>

<script>
import Logo from '~/components/Logo'
import SignupLayout from '~/layouts/SignupLayout'

export default {
	name: 'Signup',
  components: {
  	Logo,
    SignupLayout
  }
}
</script>

<style>

</style>

