<template>
  <div class="container">
    <logo class="big" />
    <div class="content">
      <the-form-signup-worker v-if="$route.query.worker"/>
      <the-form-signup-student v-else/>
      <NuxtLink 
      to="/login"
      class="login-link">
        <v-button
        class="login-btn blue big fluid">
          Войти
        </v-button>
      </NuxtLink>
      <p class="signup-problem">
        Кто-то зарегистрировался под вашим именем? Обратитесь к <NuxtLink to="#">администрации</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo'
import VButton from '~/components/VButton'
import TheFormSignupWorker from '~/components/TheFormSignupWorker'
import TheFormSignupStudent from '~/components/TheFormSignupStudent'

export default {
	layout: 'empty',
	name: 'Signup',
  components: {
  	Logo,
    VButton,
    TheFormSignupWorker,
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

.login-btn {
  margin-top: 10px;
}

.login-link:after {
  display: none;
}

.signup-problem {
  margin-top: 16px;
}

</style>

