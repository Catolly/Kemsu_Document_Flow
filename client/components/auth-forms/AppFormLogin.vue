<template>
	<form @submit.prevent="checkForm" class="form">

		<h1 class="header">Вход</h1>

		<div class="body">
      <div class="inputs">
  			<app-input
    			v-model.trim="form.email"
    			placeholder="Email"
          type="email"
    			required
        />

          <!-- :error-messages="['Ошибка 1', 'Ошибка 2']" -->
  			<app-input
    			v-model.trim="form.password"
    			placeholder="Пароль"
    			type="password"
    			required
        />
      </div>

			<p class="forgot-password">
				<NuxtLink to="#">Не помню пароль</NuxtLink>
			</p>

      <div class="btns">
  			<app-button
          class="login-btn blue big filled fluid"
         >
  				Войти
  			</app-button>

        <NuxtLink to="/signup" tabindex="-1" class="clear">
          <app-button class="to-register-btn blue big fluid">
            Зарегистрироваться
          </app-button>
        </NuxtLink>
      </div>
		</div>

	</form>
</template>

<script>
import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'

export default {
  name: 'AppFormLogin',

  components: {
    AppButton,
    AppInput,
  },

  data:() => ({
    form: {
      email: '',
      password: '',
    },
  }),

  methods: {
    checkForm() {
      // Проверка данных формы
      // ...
      this.login()
    },

    async login() {
      // Отправка данных на сервер
      // ...

      this.$router.push('/')
    },
  },
}
</script>

<style lang="less" scoped>

.form {
  .header {
    text-align: center;
  }

  .body {
    margin-top: 48px;

    .inputs,
    .btns {
      display: grid;
    }

    .inputs {
      grid-row-gap: 16px;
    }

    .forgot-password {
      margin-top: 8px;
    }

    .btns {
      margin-top: 32px;

      grid-row-gap: 8px;
    }
  }
}

</style>
