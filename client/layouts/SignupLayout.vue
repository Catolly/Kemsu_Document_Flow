<template>
  <div class="container">
    <div id="signup-wrapper">
      <the-form-signup-worker v-if="$route.query.worker"/>
      <the-form-signup-student v-else/>
    </div>
  </div>
</template>

<script>
import TheFormSignupStudent from '~/components/TheFormSignupStudent'
import TheFormSignupWorker from '~/components/TheFormSignupWorker'

export default {
  name: 'SignupLayout',
  components: {
    TheFormSignupStudent,
    TheFormSignupWorker,
  },
}
</script>

<style lang="less">
@import '~/styles/index.less';

#signup-wrapper {
  height: 100vh;
  .flex(center, center);
}

</style>

