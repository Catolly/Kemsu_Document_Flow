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
}

.content {
  height: 100%;
  width: 100%;

  overflow-y: auto;

  display: flex;
  justify-content: center;
  align-items: center;
}

.login {
  padding: 48px 0;
  width: 516px;
}
</style>

