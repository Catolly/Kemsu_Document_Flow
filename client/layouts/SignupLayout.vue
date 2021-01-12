<template>
  <div id="container">
    <div id="signup-wrapper">
      <signup-form />
    </div>
  </div>
</template>

<script>
import SignupForm from '~/components/SignupForm'
import { required, minLength, email } from 'vuelidate/lib/validators'

export default {
  name: 'SignupLayout.vue',
  components: {
    SignupForm,
  },
}
</script>

<style lang="less">
@import '~/styles/index.less';

#container {
  position: relative;
}

#signup-wrapper {
  height: 100vh;
  .flex(center, center);
}

</style>

