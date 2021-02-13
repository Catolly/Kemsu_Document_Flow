<template>
  <section class="container">
    <logo class="big" />
    <div id="form-signup-wrapper">
      <the-form-signup-worker v-if="$route.query.worker"/>
      <the-form-signup-student v-else/>
    </div>
  </section>
</template>

<script>
import Logo from '~/components/Logo'
import TheFormSignupWorker from '~/components/TheFormSignupWorker'
import TheFormSignupStudent from '~/components/TheFormSignupStudent'

export default {
	layout: 'empty',
	name: 'Signup',
  components: {
  	Logo,
    TheFormSignupWorker,
    TheFormSignupStudent,
  }
}
</script>

<style lang="less" scoped>

#form-signup-wrapper {
  height: 100vh;
  .flex(center, center);
}
</style>

