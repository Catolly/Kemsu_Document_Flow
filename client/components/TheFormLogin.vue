<template>
	<form @submit.prevent="checkForm" id="form"> 
		<h1 id="form-header">Вход</h1>
		<div id="form-inner">
			<v-input
			v-model.trim="form.username"
			placeholder="Ф.И.О. / Email"
			id="username"
      class="username"
			required />
			<v-input
			v-model.trim="form.password"
			placeholder="Пароль"
			id="password"
			type="password"
			required />
			<p class="forgot-password">
				<NuxtLink to="#">Не помню пароль</NuxtLink>
			</p>
			<v-button
			id="login"
			class="login-btn blue big filled fluid">
				Войти
			</v-button>
		</div>
	</form>
</template>

<script>
import VButton from '~/components/VButton'
import VInput from '~/components/VInput'

export default {
  name: 'TheFormLogin',
  components: {
    VButton,
    VInput,
  },
  data() {
    return {
      form: {
        username: '',
        password: '',
      }
    }
  },
  methods: {
    checkForm() {
      // Проверка данных формы
      // ...
      this.login()
    },
    async login() {   
      // // Валидация данных на сервере
      // // ...

      this.$router.push('/')
    },
  },
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

  .login-btn {
    margin-top: 32px;
  }
}

</style>