<template>
  <div class="container">
    <div class="content">
      <app-form-login class="login" />
    </div>
  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppFormLogin from '~/components/auth-forms/AppFormLogin'

export default {
	layout: 'empty',

	name: 'login',

  middleware: 'unauthenticated',

  components: {
    AppButton,
    AppFormLogin,
  },
}
</script>

<style scoped>
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

.login {
  padding: 48px 0;
  overflow-y: auto;
}
</style>

