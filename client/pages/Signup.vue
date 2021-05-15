<template>
  <div class="container">
    <div class="content">
      <app-form-signup-staff v-if="$route.query.staff"/>
      <app-form-signup-student v-else/>
    </div>
  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppFormSignupStaff from '~/components/auth-forms/AppFormSignupStaff'
import AppFormSignupStudent from '~/components/auth-forms/AppFormSignupStudent'

export default {
	layout: 'empty',
	name: 'signup',
  components: {
    AppButton,
    AppFormSignupStaff,
    AppFormSignupStudent,
  }
}
</script>

<style lang="less" scoped>

.container {
  height: 100vh;

  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  width: 516px;
}

</style>

