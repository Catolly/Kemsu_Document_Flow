<template>
  <div class="container">
    <div class="content">
      <app-form-login />
      <NuxtLink
      to="/signup"
      tabindex="-1"
      class="signup-link">
        <app-button
        tabindex="0"
        class="signup-btn blue big fluid">
          Зарегистрироваться
        </app-button>
      </NuxtLink>
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

<style lang="less" scoped>

.container {
  height: 100vh;
  .flex(center, center, column);
}

.content {
  width: 516px;
}

.signup-btn {
  margin-top: 10px;
}

.signup-link:after {
  display: none;
}

</style>

