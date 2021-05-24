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
            ... $v.email.$dirty
                && $v.email.required
                && !$v.email.email
                ? ['Поле должно быть заполнено по email-маске']
                : [],
          ]"
          @input="reset($v.email)"
          @change="checkField($v.email)"
        />

  			<app-input
    			v-model="$v.password.$model"
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
                ? [`Пароль должен содержать ${minPasswordLength} и более символов`]
                : [],
          ]"
          @input="reset($v.password)"
          @change="checkField($v.password)"
        />
      </div>

			<p class="forgot-password">
				<a @click="dialog = true">Не помню пароль</a>
			</p>

      <div class="btns">
        <p
          v-if="loginError"
          class="error-message"
        >
          Неверный логин или пароль
        </p>

        <p
          v-if="error"
          class="error-message"
        >
          Произошла ошибка
        </p>

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

    <app-dialog :isOpen="dialog" @close="dialog = false">
      <p>
        Для восстановления пароля свяжитесь с администрацией:
        <b>{{adminEmail}}</b>
      </p>
    </app-dialog>
	</form>
</template>

<script>
import { adminEmail } from "~/services/config"
import { errorCode } from "~/services/ApiService"

import { LOGIN } from "~/store/actions.type"

import { required, minLength, email } from "vuelidate/lib/validators"
import { minPasswordLength } from "~/vuelidate/constants"

import AppButton from '~/components/common/AppButton'
import AppInput from '~/components/common/AppInput'
import AppDialog from '~/components/common/AppDialog'

export default {
  name: 'AppFormLogin',

  components: {
    AppButton,
    AppInput,
    AppDialog,
  },

  data:() => ({
    email: '',
    password: '',

    minPasswordLength: minPasswordLength,

    loginError: '',
    error: '',

    dialog: false,
    adminEmail: adminEmail,
  }),

  validations:() => ({
    email: {
      required,
      email,
    },
    password: {
      required,
      minLength: minLength(minPasswordLength),
    },
  }),

  methods: {
    reset($v) {
      if (!$v.required) return

      $v.$reset()
    },

    checkField($v) {
      $v.$model = $v.$model.trim()

      $v.$touch()
    },

    submit() {
      this.$v.$touch()

      if (this.$v.$invalid) return

      this.login()
    },

    login() {
      this.loginError = ''
      this.error = ''
      this.$store
        .dispatch(LOGIN, {
          'email': this.email,
          'password': this.password,
        })
        .then(() => this.$router.push('/'))
        .catch(error => {
          console.error(error)
          if (errorCode(error === '400'))
            this.loginError = error
          else this.error = error
        })
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
