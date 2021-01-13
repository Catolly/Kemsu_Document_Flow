<template>
  <div class="container">
    <div id="signup-wrapper">
      <the-signup-form />
    </div>
  </div>
</template>

<script>
import TheSignupForm from '~/components/TheSignupForm'
import { required, minLength, email } from 'vuelidate/lib/validators'

export default {
  name: 'SignupLayout.vue',
  components: {
    TheSignupForm,
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

