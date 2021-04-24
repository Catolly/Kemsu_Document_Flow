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
  			class="login-btn blue big filled fluid">
  				Войти
  			</app-button>

        <app-button
        class="to-register-btn blue big fluid">
          Зарегистрироваться
        </app-button>
      </div>
		</div>

	</form>
</template>

<script>
// import { mapMutations } from 'vuex'

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
    // ...mapMutations([
    //   'updateTokens'
    // ]),

    checkForm() {
      // Проверка данных формы
      // ...
      this.login()
    },

    async login() {
      // // Валидация данных на сервере
      // // ...
      // const tokens = await new Promise((res, rej) => {
      //   setTimeout(() => res({
      //     accessToken: 'logged',
      //     refreshToken: 'logged',
      //     expiresIn: Date.now() + 1800e3,
      //   }), 500)
      // })
      // this.updateTokens(tokens)

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
