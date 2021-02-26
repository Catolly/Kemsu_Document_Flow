<template>
  <div class="container">
  	<logo class="big" />
    <div class="content">
      <the-form-login />
      <NuxtLink 
      to="/signup"
      class="signup-link">
        <v-button
        class="signup-btn blue big fluid">
          Зарегистрироваться
        </v-button>
      </NuxtLink>
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo'
import VButton from '~/components/VButton'
import TheFormLogin from '~/components/TheFormLogin'

export default {
	layout: 'empty',
	name: 'Login',
  components: {
  	Logo,
    VButton,
    TheFormLogin,
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

.signup-btn {
  margin-top: 10px;
}

.signup-link:after {
  display: none;
}

</style>

