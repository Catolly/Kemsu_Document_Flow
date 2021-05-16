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
}

.content {
  width: 516px;
  height: 100%;

  display: flex;
  flex-direction: column;
  justify-content: center;
}

.signup {
  padding: 48px 0;
  overflow-y: auto;
}
</style>
