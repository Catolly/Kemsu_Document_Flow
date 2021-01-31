<template>
	<form @submit.prevent="checkForm()" id="form"> 
    <h1 id="form-header">Регистрация</h1>
    <div id="form-inner">
      <v-input
      v-model.trim="form.username"
      :class="$v.form.username.$error ? 'is-invalid' : ''"
      id="username"
      type="text"
      placeholder="Ф.И.О."
      required />
      <v-input
      v-model.trim="form.email"
      :class="$v.form.email.$error ? 'is-invalid' : ''"
      id="email"
      type="email"
      placeholder="Email"
      required />
      <v-input
      v-model.trim="form.password"
      :class="$v.form.password.$error ? 'is-invalid' : ''"
      id="password"
      type="password"
      placeholder="Пароль"
      required />
      <div class="buttons">
        <v-button
        id="signup"
        class="btn blue big filled fluid">
          Зарегистрироваться
        </v-button>
        <v-button
        id="login"
        class="btn blue big fluid">
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
  name: 'TheFormSingupStudent',
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

#form {
	width: 516px;
}

#form-header {
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

.btn {
  margin-top: 10px;

  &:first-child {
    margin-top: 32px;
  }
}

p {
  margin-top: 18px;
}
</style>