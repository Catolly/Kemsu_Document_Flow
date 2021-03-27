<template>
  <div class="container">
    <logo class="big" />
    <div class="content">
      <the-form-signup-staff v-if="$route.query.staff"/>
      <the-form-signup-student v-else/>
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo'
import VButton from '~/components/VButton'
import TheFormSignupStaff from '~/components/TheFormSignupStaff'
import TheFormSignupStudent from '~/components/TheFormSignupStudent'

export default {
	layout: 'empty',
	name: 'Signup',
  components: {
  	Logo,
    VButton,
    TheFormSignupStaff,
    TheFormSignupStudent,
  }
}
</script>

<style lang="less" scoped>

.container {
  height: 100vh;
  .flex(center, center, column);
}

.content {
  width: 516px;
}

</style>

