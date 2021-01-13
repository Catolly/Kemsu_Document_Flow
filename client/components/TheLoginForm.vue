<template>
	<form @submit="checkForm()" id="login-form"> 
		<h1>Вход</h1>
		<div id="form-inner">
			<v-input
			v-model.trim="form.username"
			:class="$v.form.username.$error ? 'is-invalid' : ''"
			id="username"
			type="text"
			placeholder="Ф.И.О."
			required></v-input>
			<v-input
			v-model.trim="form.password"
			:class="$v.form.password.$error ? 'is-invalid' : ''"
			id="password"
			type="password"
			placeholder="Пароль"
			required></v-input>
			<p>
				<NuxtLink to="#">Не помню пароль</NuxtLink>
			</p>
			<div class="buttons">
				<v-button
				id="login"
				class="blue big filled">
					Войти
				</v-button>
				<v-button
				id="signup"
				class="blue big">
					Зарегистрироваться
				</v-button>
			</div>
		</div>
	</form>
</template>

<script>
import VInput from '~/components/VInput'
import VButton from '~/components/VButton'
import { required, minLength, email } from 'vuelidate/lib/validators'

export default {
  name: 'TheLoginForm.vue',
  components: {
    VInput,
    VButton,
  },
  data() {
    return {
      form: {
        username: '',
        password: '',
      }
    }
  },
  validations: {
    form: {
      username: { required },
      password: { required },
    },
  },
  methods: {
    checkForm() {
      this.$v.form.$touch()
      if (!this.$v.form.$error) {
        this.send()
      }
    },
    send() {
      /*Sending form data to server*/
    }
  }
}
</script>

<style lang="less" scoped>
@import '~/styles/index.less';

#container {
  position: relative;
}

form {
	width: 516px;
}

h1 {
  text-align: center;
}

#form-inner {
  margin-top: 48px;

  & p {
    margin-top: 8px;
  }
}

input {
  font-size: @fz-large;
  line-height: 160%;
}

button {
  margin-top: 10px;

  &:first-child {
    margin-top: 32px;
  }
}

p {
  margin-top: 18px;
}
</style>