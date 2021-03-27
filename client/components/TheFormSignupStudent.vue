<template>
	<form @submit.prevent="checkForm" id="form"> 
    <h1 id="form-header">Регистрация</h1>
    <div id="form-inner">
      <v-input
      v-model.trim="form.username"
      id="username"
      class="username"
      type="text"
      placeholder="Ф.И.О."
      required />
      <v-input
      v-model.trim="form.email"
      id="email"
      class="email"
      type="email"
      placeholder="Email"
      required />
      <v-input
      v-model.trim="form.password"
      id="password"
      class="password"
      type="password"
      placeholder="Пароль"
      required />
      <v-button
      id="signup"
      class="signup-btn blue big filled fluid">
        Зарегистрироваться
      </v-button>
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
  </form>
</template>

<script>
import VButton from '~/components/VButton'
import VInput from '~/components/VInput'

export default {
  name: 'TheFormSingupStudent',
  components: {
    VButton,
    VInput,
  },
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
      }
    }
  },
  },
  methods: {
    checkForm() {
      // Проверка данных формы
      // ...
      this.signup()
    },
    async signup() {

      this.$router.push('/')
    },
  }
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

#form {
  width: 516px;
}

#form-header {
  text-align: center;
}

#form-inner {
  margin-top: 48px;

  .username {
    width: 100%;
  }

  .forgot-password {
    margin-top: 8px;
  }

  .signup-btn {
    margin-top: 32px;
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
}
</style>