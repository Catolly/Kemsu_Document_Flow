<template>
  <div class="container">
    <div class="content">
      <app-form-signup-staff v-if="$route.query.staff" class="signup"/>
      <app-form-signup-student v-else class="signup"/>
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
  middleware: 'unauthenticated',
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
}

.content {
  height: 100%;
  width: 100%;

  overflow-y: auto;

  display: flex;
  justify-content: center;
  align-items: center;
}

.signup {
  padding: 48px 0;
  width: 516px;
}
</style>
