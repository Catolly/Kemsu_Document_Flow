<template>
  <div class="container">
    <div class="content">
      <app-form-login />
    </div>
  </div>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppFormLogin from '~/components/auth-forms/AppFormLogin'

export default {
	layout: 'empty',

	name: 'login',

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
  align-items: center;
}

.content {
  width: 516px;
}

</style>

