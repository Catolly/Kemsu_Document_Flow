<template>
	<form @submit.prevent="submit" class="form">

		<h1 class="header">Вход</h1>

		<div class="body">
      <div class="inputs">
  			<app-input
    			v-model.trim="$v.email.$model"
    			placeholder="Email"
          :errorMessages="[
            ... $v.email.$dirty
                && !$v.email.required
                ? ['Поле должно быть заполнено']
                : [],
          ]"
          @input="checkField($v.email)"
        />
  			<app-input
    			v-model.trim="$v.password.$model"
    			placeholder="Пароль"
    			type="password"
          :errorMessages="[
            ... $v.password.$dirty
                && !$v.password.required
                ? ['Поле должно быть заполнено']
                : [],
            ... $v.password.$dirty &&
                $v.password.required
                && !$v.password.minLength
                ? ['Пароль должен содержать 7 и более символов']
                : [],
          ]"
          @input="checkField($v.password)"
        />
      </div>

			<p class="forgot-password">
				<NuxtLink to="#">Не помню пароль</NuxtLink>
			</p>

      <div class="btns">
  			<app-button
          class="login-btn blue big filled fluid"
          :disabled="$v.$invalid"
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
import { required, minLength, email } from "vuelidate/lib/validators"
import _ from 'lodash'

import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'

export default {
  name: 'AppFormLogin',

  components: {
    AppButton,
    AppInput,
  },

  data:() => ({
    email: '',
    password: '',
  }),

  validations:() => ({
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(7),
    },
  }),

  methods: {
    checkField($v) {
      if (!$v.required) return

      $v.$reset()
      this.delayTouch($v)
    },

    delayTouch: _.debounce($v => {
      $v.$touch()
    }, 2e3),

    submit() {
      this.$v.$touch()

      if (this.$v.$invalid) return

      this.login()
    },

    async login() {
      // Отправка данных на сервер
      // ...

      // this.$router.push('/')
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
