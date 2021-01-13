<template>
  <div class="container">
    <div id="signup-wrapper">
      <the-form-signup-student>
    </div>
  </div>
</template>

<script>
import TheFormSignupStudent from '~/components/TheFormSignupStudent'

export default {
  name: 'SignupLayout.vue',
  components: {
    TheFormSignupStudent,
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

