<template>
	<form @submit="checkForm()" id="signup-form"> 
    <h1>Регистрация</h1>
    <div id="form-inner">
      <v-input
      v-model.trim="form.username"
      :class="$v.form.username.$error ? 'is-invalid' : ''"
      id="username"
      type="text"
      placeholder="Ф.И.О."
      required></v-input>
      <v-input
      v-model.trim="form.email"
      :class="$v.form.email.$error ? 'is-invalid' : ''"
      id="email"
      type="email"
      placeholder="Email"
      required></v-input>
      <v-input
      v-model.trim="form.password"
      :class="$v.form.password.$error ? 'is-invalid' : ''"
      id="password"
      type="password"
      placeholder="Пароль"
      required></v-input>
      <div class="buttons">
        <v-button
        id="signup"
        class="blue big filled">
          Зарегистрироваться
        </v-button>
        <v-button
        id="login"
        class="blue big">
          Войти
        </v-button>
      </div>
    </div>
    <p>Кто-то зарегистрировался под вашим именем? Обратитесь к <NuxtLink to="#">администрации</NuxtLink></p>
  </form>
</template>

<script>
import VInput from '~/components/VInput'
import VButton from '~/components/VButton'
import { required, minLength, email } from 'vuelidate/lib/validators'

export default {
  name: 'TheSignupForm.vue',
  components: {
    VInput,
    VButton,
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
  validations: {
    form: {
      username: { required, minLength: minLength(5) },
      email: { required, email },
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
    },
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