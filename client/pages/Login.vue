<template>
  <div class="container">
    <div class="content">
      <form-login />
      <NuxtLink 
      to="/signup"
      tabindex="-1"
      class="signup-link">
        <v-button
        tabindex="0"
        class="signup-btn blue big fluid">
          Зарегистрироваться
        </v-button>
      </NuxtLink>
    </div>
  </div>
</template>

<script>
import VButton from '~/components/common/VButton'
import FormLogin from '~/components/common/FormLogin'

export default {
	layout: 'empty',
	name: 'Login',
  components: {
    VButton,
    FormLogin,
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

